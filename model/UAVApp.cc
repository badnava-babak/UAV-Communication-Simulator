//
// Created by b502b586 on 11/8/21.
//

#include <iostream>
#include <fstream>
#include <string>
#include <stdio.h>
#include <stdlib.h>
#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/applications-module.h"
#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/mobility-module.h"
#include "ns3/wifi-module.h"
#include "ns3/flow-monitor-helper.h"
#include "ns3/internet-module.h"
#include "ns3/core-module.h"
#include "ns3/csma-module.h"
#include "ns3/applications-module.h"
#include "ns3/internet-module.h"
#include "ns3/network-module.h"
#include <mavsdk/mavsdk.h>
#include <mavsdk/plugins/action/action.h>
#include <mavsdk/plugins/telemetry/telemetry.h>
#include <iostream>
#include <future>
#include <memory>
#include <thread>


#include "UAVApp.h"
#include "ns3/telemetry-message.pb.h"
#include "ns3/control-message.pb.h"
#include <mavsdk/plugins/mission_raw/mission_raw.h>


using namespace ns3;
using namespace mavsdk;
using std::chrono::seconds;
using std::chrono::milliseconds;
using std::this_thread::sleep_for;

NS_LOG_COMPONENT_DEFINE ("UAVApp");


std::shared_ptr<System> get_system(Mavsdk &mavsdk) {
    std::cout << "Waiting to discover system...\n";
    auto prom = std::promise<std::shared_ptr<System>>{};
    auto fut = prom.get_future();

    // We wait for new systems to be discovered, once we find one that has an
    // autopilot, we decide to use it.
    mavsdk.subscribe_on_new_system([&mavsdk, &prom]() {
        auto system = mavsdk.systems().back();

        if (system->has_autopilot()) {
            std::cout << "Discovered autopilot\n";

            // Unsubscribe again as we only want to find one system.
            mavsdk.subscribe_on_new_system(nullptr);
            prom.set_value(system);
        }
    });

    // We usually receive heartbeats at 1Hz, therefore we should find a
    // system after around 3 seconds max, surely.
    if (fut.wait_for(seconds(5)) == std::future_status::timeout) {
        std::cerr << "No autopilot found.\n";
        return {};
    }

    // Get discovered system now.
    return fut.get();
}

MissionRaw::MissionItem make_mission_item(
        ControlMessage::MissionItem missionItem) {
    MissionRaw::MissionItem new_item{};

    new_item.seq = missionItem.seq();
    new_item.frame = missionItem.frame();
    new_item.current = missionItem.current();
    new_item.command = missionItem.command();
    new_item.autocontinue = missionItem.autocontinue();
    new_item.x = missionItem.x();
    new_item.y = missionItem.y();
    new_item.z = missionItem.z();
    new_item.mission_type = missionItem.mission_type();

    new_item.param1 = missionItem.param1();
    new_item.param2 = missionItem.param2();
    new_item.param3 = missionItem.param3();
    new_item.param4 = missionItem.param4();

    return new_item;
}

UAVApp::UAVApp() {
}

UAVApp::~UAVApp() {
    senderSocket = nullptr;
    listenerSocket = nullptr;
    system = nullptr;
}

void UAVApp::Setup(const Address &gcs, uint32_t port, Ptr<Node> node, int32_t id, std::string mavAddr) {

//    mavLinkAddr = "tcp://127.0.0.1:5770";
    mavLinkAddr = mavAddr;
    uavID = id;


//    uavAddress = InetSocketAddress(node->GetObject<Ipv4>()->GetAddress(1, 0).GetAddress(), port);
    uavAddress = InetSocketAddress(Ipv4Address::GetAny(), port);
    gcsAddress = gcs;

    std::cout << " UAVApp::UAV address: " << uavAddress << std::endl;
    std::cout << " UAVApp::4GCS address: " << gcsAddress << std::endl;

    TypeId tid = TypeId::LookupByName("ns3::UdpSocketFactory");

    Ptr<Socket> recvSink = Socket::CreateSocket(node, tid);
    recvSink->SetIpRecvTos(true);
    recvSink->SetIpRecvTtl(true);
    listenerSocket = recvSink;

    Ptr<Socket> source = Socket::CreateSocket(node, tid);
    senderSocket = source;


}

void UAVApp::StartApplication(void) {
    m_running = true;
    listenerSocket->Bind(uavAddress);
    listenerSocket->SetRecvCallback(MakeCallback(&UAVApp::ReceiveCommand, this));
    senderSocket->Connect(gcsAddress);

    Time tNext(Seconds(0.1));
    Simulator::Schedule(tNext, &UAVApp::InitUAV, this);
//    InitUAV();
}

void UAVApp::StopApplication(void) {
    m_running = false;

    telemetryThread->Join();
    controlThread->Join();
    if (listenerSocket) {
        listenerSocket->Close();
    }

    if (senderSocket) {
        senderSocket->Close();
    }
}

void UAVApp::SendPacket() {
//    Ptr<Packet> packet = Create<Packet>(m_packetSize);
//    sender_socket->Send(packet);
}


void UAVApp::ReceiveCommand(Ptr<Socket> socket) {
    std::cout << "ReceiveCommand \n";
    Ptr<Packet> packet = socket->Recv();
    ControlMessage msg = ParseCommand(packet);
    msg.set_receivetime(Simulator::Now().GetMilliSeconds());
    controlMessageQueue.push(msg);

    uavControlTraceFile << Simulator::Now().GetMilliSeconds() << ",\t";
    uavControlTraceFile << msg.senttime() << ",\t";
    uavControlTraceFile << msg.receivetime() << ",\t";
    uavControlTraceFile << msg.receivetime() - msg.senttime() << ",\t";
    uavControlTraceFile << msg.command() << "\n";

    uavControlTraceFile.flush();

}

ControlMessage UAVApp::ParseCommand(const Ptr<Packet> &packet) const {
    uint8_t *buffer = new uint8_t[packet->GetSize()];
    packet->CopyData(buffer, packet->GetSize());

    ControlMessage msg = ControlMessage();
    msg.ParseFromArray(buffer, packet->GetSize());

//    delete[] buffer;
//    buffer = nullptr;

    return msg;
}

bool UAVApp::ArmAndTakeoff(float alt) {
    auto action = Action{system};
    auto telemetry = Telemetry{system};

    while (telemetry.health_all_ok() != true) {
        std::cout << "Vehicle is getting ready to arm\n";
        sleep_for(seconds(1));
    }

// Arm vehicle
    std::cout << "Arming...\n";
    const Action::Result arm_result = action.arm();

    if (arm_result != Action::Result::Success) {
        std::cerr << "Arming failed: " << arm_result << '\n';
        return false;
    }

    // Setting takeoff alt.
    std::cout << "Setting takeoff alt....\n";
    const Action::Result alt_result = action.set_takeoff_altitude(alt);

    if (alt_result != Action::Result::Success) {
        std::cerr << "Setting takeoff alt. failed: " << alt_result << '\n';
        return false;
    }

    // Take off
    std::cout << "Taking off...\n";
    const Action::Result takeoff_result = action.takeoff();
    if (takeoff_result != Action::Result::Success) {
        std::cerr << "Takeoff failed: " << takeoff_result << '\n';
        return false;
    }
    return true;
}


bool UAVApp::ArmAndStartMission() {
    auto action = Action{system};
    auto telemetry = Telemetry{system};
    auto mission = MissionRaw{system};


    while (telemetry.health().is_armable != true) {
        std::cout << "Vehicle is getting ready to arm\n";
        sleep_for(seconds(1));
    }

    // Arm vehicle
    std::cout << "Arming...\n";
    const Action::Result arm_result = action.arm();

    if (arm_result != Action::Result::Success) {
        std::cerr << "Arming failed: " << arm_result << '\n';
        return false;
    }

    std::cout << "Starting mission...\n";
    MissionRaw::Result start_mission_result = mission.start_mission();
    if (start_mission_result != MissionRaw::Result::Success) {
        std::cerr << "Starting mission failed: " << start_mission_result << '\n';
        return false;
    }

    return true;
}

bool UAVApp::Land() {
    auto action = Action{system};

    std::cout << "Landing...\n";
    const Action::Result land_result = action.land();
    if (land_result != Action::Result::Success) {
        std::cerr << "Land failed: " << land_result << '\n';
        return false;
    }
    return true;
}

Ptr<MyConstantPositionMobilityModel> UAVApp::GetMobility() {
    if (mobilityModel == nullptr) {
        mobilityModel = m_node->GetObject<MyConstantPositionMobilityModel>();
    }
//    if (mobilityModel->GetReferenceCount() > 1000)
//        std::cout << "We are fucked up!\n";
    return mobilityModel;
}

void UAVApp::InitUAV() {

//    usage(addr);

    ConnectionResult connection_result = mavsdk.add_any_connection(mavLinkAddr);

    if (connection_result != ConnectionResult::Success) {
        std::cerr << "Connection failed: " << connection_result << '\n';
        return;
    }

    system = get_system(mavsdk);
    if (!system) {
        std::cerr << "Unable to create the system.\n";
        return;
    }

    // Instantiate plugins.
    telemetryThread = Create<SystemThread>(MakeCallback(&UAVApp::TelemetryThread, this));
    telemetryThread->Start();

    controlThread = Create<SystemThread>(MakeCallback(&UAVApp::CommandExecutionThread, this));
    controlThread->Start();

    std::string filename = "uav-";
    filename += std::to_string(uavID);
    filename += "-control.txt";
    EnableControlTrace(filename);

//

}

void UAVApp::SendTelemetry(std::string &serializedMsg) {
    std::vector<uint8_t> serializedMsgInUint(serializedMsg.begin(), serializedMsg.end());
    senderSocket->Send(&serializedMsgInUint[0], serializedMsgInUint.size(), 1);
//    std::cout << "Bytes sent: " << res << std::endl;
}

void UAVApp::TelemetryThread(void) {
    auto telemetry = Telemetry{system};

    // We want to listen to the altitude of the drone at 1 Hz.
    const auto set_rate_result = telemetry.set_rate_position(0.5);
    if (set_rate_result != Telemetry::Result::Success) {
        std::cerr << "Setting rate failed: " << set_rate_result << '\n';
        return;
    }


    // Set up callback to monitor altitude while the vehicle is in flight
    telemetry.subscribe_position([this, &telemetry](Telemetry::Position position) {
        if (telemetry.armed()) {
//            std::cout << "UAV Position: " << position.latitude_deg << ", "
//                      << position.longitude_deg << ", " << position.absolute_altitude_m << " \n";


            // Update location of the node
//            Ptr<ConstantPositionMobilityModel> mobilityModel = m_node->GetObject<ConstantPositionMobilityModel>();
//            Ptr<ConstantPositionMobilityModel> mobility = GetMobility();

//            Ptr<ConstantPositionMobilityModel> mobilityModel = m_node->GetObject<ConstantPositionMobilityModel>();

            Vector currentPosition = GeographicPositions::GeographicToCartesianCoordinates(position.latitude_deg,
                                                                                           position.longitude_deg,
                                                                                           position.absolute_altitude_m,
                                                                                           GeographicPositions::SPHERE);
            GetMobility()->SetPosition(currentPosition);
//            mobilityModel->Unref();
//            Waypoint wpt(MilliSeconds(Simulator::Now().GetMilliSeconds() + 1), currentPosition);
//            mobilityModel->AddWaypoint(wpt);


            // Send the telemetry info to the GCS
            TelemetryMessage *msg = CreeateTelemetryMessage(TelemetryMessage::PositionUpdate);
            TelemetryMessage::PositionInfo *pos = msg->mutable_position();
            pos->set_absolute_altitude_m(position.absolute_altitude_m);
            pos->set_relative_altitude_m(position.relative_altitude_m);
            pos->set_latitude_deg(position.latitude_deg);
            pos->set_longitude_deg(position.longitude_deg);

            std::string serializedMsg = msg->SerializeAsString();
            SendTelemetry(serializedMsg);

//            delete msg;
//            msg = nullptr;
        }

    });


    telemetry.subscribe_position_velocity_ned([this, &telemetry](Telemetry::PositionVelocityNed positionVelocityNed) {
//        positionVelocityNed.position.down_m;
//        std::cout << "UAV Position NED: " << positionVelocityNed.position.down_m << ", "
//                  << positionVelocityNed.position.east_m << ", " << positionVelocityNed.position.north_m << " \n";
//        std::cout << "UAV Velocity NED: " << positionVelocityNed.velocity.down_m_s << ", "
//                  << positionVelocityNed.velocity.east_m_s << ", " << positionVelocityNed.velocity.north_m_s << " \n";

        if (telemetry.armed()) {
            TelemetryMessage *msg = CreeateTelemetryMessage(TelemetryMessage::PositionVelocityNedUpdate);

            TelemetryMessage::PositionVelocityNed::PositionNed *pos = msg->mutable_positionvelocityned()->mutable_position();
            pos->set_down_m(positionVelocityNed.position.down_m);
            pos->set_east_m(positionVelocityNed.position.east_m);
            pos->set_north_m(positionVelocityNed.position.north_m);

            TelemetryMessage::PositionVelocityNed::VelocityNed *vel = msg->mutable_positionvelocityned()->mutable_velocity();
            vel->set_down_m_s(positionVelocityNed.velocity.down_m_s);
            vel->set_east_m_s(positionVelocityNed.velocity.east_m_s);
            vel->set_north_m_s(positionVelocityNed.velocity.north_m_s);

            std::string serializedMsg = msg->SerializeAsString();
            SendTelemetry(serializedMsg);
//            delete msg;
//            msg = nullptr;
        }
    });

    telemetry.subscribe_battery([this, &telemetry](Telemetry::Battery battery) {

        if (telemetry.armed()) {
//            std::cout << "UAV Battery: " << battery.remaining_percent << ", " << battery.voltage_v << " \n";
            TelemetryMessage *msg = CreeateTelemetryMessage(TelemetryMessage::BatteryUpdate);

            TelemetryMessage::BatteryInfo *batteryInfo = msg->mutable_battery();
            batteryInfo->set_id(battery.id);
            batteryInfo->set_remaining_percent(battery.remaining_percent);
            batteryInfo->set_voltage_v(battery.voltage_v);

            std::string serializedMsg = msg->SerializeAsString();
            SendTelemetry(serializedMsg);
//            delete msg;
//            msg = nullptr;
        }

    });

    // Check until vehicle is ready to arm
    while (telemetry.health_all_ok() != true) {
        std::cout << "Vehicle is getting ready to arm\n";
        sleep_for(seconds(1));
    }

    while (m_running) {
        sleep_for(milliseconds(500));
    }

}

ns3::TelemetryMessage *UAVApp::CreeateTelemetryMessage(TelemetryMessage_UpdateType type) const {
    TelemetryMessage *msg = new TelemetryMessage();
    msg->set_uavid(uavID);
    msg->set_uavarrivaltime(Simulator::Now().GetMilliSeconds());
    msg->set_update(type);
    return msg;
}

bool UAVApp::GoTo(double latitude, double longitude, float altitude, float yaw) {
    auto action = Action{this->system};
    auto tel = Telemetry{this->system};

    std::cout << "Going to" << latitude << ", " << longitude << ", " << altitude
              << ", with yaw: " << yaw << "\n";
    const Action::Result land_result = action.goto_location(latitude, longitude, altitude, yaw);
    if (land_result != Action::Result::Success) {
        std::cerr << "Goto action failed: " << land_result << '\n';
        return false;
    }
    return true;
}

bool UAVApp::ReturnToLaunch() {
    auto action = Action{system};
    std::cout << "Returning To Launch...\n";
    const Action::Result land_result = action.return_to_launch();
    if (land_result != Action::Result::Success) {
        std::cerr << "Returning To Launch failed: " << land_result << '\n';
        return false;
    }
    return true;
}


bool UAVApp::UploadMission(ControlMessage msg) {
    auto mission = MissionRaw{system};
    std::vector<MissionRaw::MissionItem> mission_items;

    for (int j = 0; j < msg.missionitems_size(); j++) {
        mission_items.push_back(make_mission_item(msg.missionitems(j)));
    }
    std::cout << "Uploading Mission...\n";
    const MissionRaw::Result upload_result = mission.upload_mission(mission_items);
    if (upload_result != MissionRaw::Result::Success) {
        std::cerr << "Mission upload failed: " << upload_result << ", exiting.\n";
        return false;
    }

    return true;
}

bool UAVApp::SetMaxSpeed(float speed) {
    auto action = Action{system};
    std::cout << "Setting Max Speed...\n";
    const Action::Result land_result = action.set_maximum_speed(speed);
    if (land_result != Action::Result::Success) {
        std::cerr << "Setting Max Speed failed: " << land_result << '\n';
        return false;
    }
    return true;
}

void UAVApp::CommandExecutionThread(void) {
//    ArmAndTakeoff(10);
    while (m_running) {
        int tries = 0;
        while (!controlMessageQueue.empty()) {
            ControlMessage msg = controlMessageQueue.front();
            bool succeed = false;
            switch (msg.command()) {
                case ControlMessage_CommandType_ARM_AND_START_MISSION:
                    succeed = ArmAndStartMission();
                    break;
                case ControlMessage_CommandType_UPLOAD_MISSION:
                    succeed = UploadMission(msg);
                    break;
                case ControlMessage_CommandType_ARM_AND_TAKEOFF:
                    succeed = ArmAndTakeoff(msg.altitude());
                    break;
                case ControlMessage_CommandType_LAND:
                    succeed = Land();
                    break;
                case ControlMessage_CommandType_GO_TO:
                    succeed = GoTo(msg.latitude(), msg.longitude(), msg.altitude(), msg.yaw());
                    break;
                case ControlMessage_CommandType_RETURN_TO_LAUNCH:
                    succeed = ReturnToLaunch();
                    break;
                case ControlMessage_CommandType_SET_MAX_SPEED:
                    succeed = SetMaxSpeed(msg.speed());
                    break;
                default:
                    break;
            }

            if (succeed) {
                controlMessageQueue.pop();
                tries = 0;
            } else {
                if (++tries > 10) {
                    std::cerr << "Attempt to execute the action failed 10 times!";
                    controlMessageQueue.pop();
                    tries = 0;
                }
            }
        }
        sleep_for(seconds(1));
    }
}

void UAVApp::EnableControlTrace(std::string filename) {
    uavControlTraceFile.open(filename.c_str());
//    uavControlTraceFile << "#\t";
    uavControlTraceFile << "Time\t";
    uavControlTraceFile << "SentTime\t";
    uavControlTraceFile << "ReceiveTime\t";
    uavControlTraceFile << "Delay\t";
    uavControlTraceFile << "CommandID\n";
}








