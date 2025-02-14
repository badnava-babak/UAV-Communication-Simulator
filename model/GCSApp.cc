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


#include "GCSApp.h"
#include "ns3/control-message.pb.h"
#include "ns3/telemetry-message.pb.h"
#include <mavsdk/plugins/mavlink_passthrough/mavlink_passthrough.h>

using namespace ns3;
using std::chrono::seconds;
using std::chrono::milliseconds;
using std::this_thread::sleep_for;

NS_LOG_COMPONENT_DEFINE ("GCSApp");


GCSApp::GCSApp() {
}

GCSApp::~GCSApp() {
    senderSocket = nullptr;
    listenerSocket = nullptr;
}

void GCSApp::Setup(const Address &uav, const Address &gcs, Ptr<Node> node, int32_t id) {

    uavAddress = uav;
    gcsAddress = gcs;
    gcsID = id;

    std::cout << " GCSApp::UAV address: " << uavAddress << std::endl;
    std::cout << " GCSApp::GCS address: " << gcsAddress << std::endl;

    //Receiver socket on UAV i
    TypeId tid = TypeId::LookupByName("ns3::UdpSocketFactory");
    Ptr<Socket> recvSink = Socket::CreateSocket(node, tid);
    recvSink->SetIpRecvTos(true);
    recvSink->SetIpRecvTtl(true);
    listenerSocket = recvSink;

    //Sender socket on UAV i
    Ptr<Socket> source = Socket::CreateSocket(node, tid);
    senderSocket = source;
}

void GCSApp::StartApplication(void) {
    m_running = true;
    listenerSocket->Bind(gcsAddress);
    listenerSocket->SetRecvCallback(MakeCallback(&GCSApp::ReceiveTelemetry, this));
    senderSocket->Connect(uavAddress);
    Time tNext(Seconds(gcsID * 1));
    Simulator::Schedule(tNext, &GCSApp::InitUAV, this);

    telemetryThread = Create<SystemThread>(MakeCallback(&GCSApp::TelemetryThread, this));
    telemetryThread->Start();

    EnableTelemetryTrace("uav-telemetry.txt");

//    InitUAV();
}

void GCSApp::StopApplication(void) {
    m_running = false;

    if (listenerSocket) {
        listenerSocket->Close();
    }

    if (senderSocket) {
        senderSocket->Close();
    }

    telemetryThread->Join();
}

void GCSApp::SendPacket() {
//    Ptr<Packet> packet = Create<Packet>(m_packetSize);
//    sender_socket->Send(packet);
}


void GCSApp::ReceiveTelemetry(Ptr<Socket> socket) {
    Ptr<Packet> packet = socket->Recv();
    uint8_t *buffer = new uint8_t[packet->GetSize()];
    packet->CopyData(buffer, packet->GetSize());

    TelemetryMessage msg = TelemetryMessage();
    msg.ParseFromArray(buffer, packet->GetSize());
    msg.set_gcsarrivaltime(Simulator::Now().GetMilliSeconds());
//    delete[] buffer;
//    buffer = nullptr;

    auto search = uavLastTelemetry.find(msg.uavid());
    if (search != uavLastTelemetry.end()) {
        TelemetryMessage *latestTelemetry = &search->second;
        latestTelemetry->set_gcsarrivaltime(msg.gcsarrivaltime());
        latestTelemetry->set_uavarrivaltime(msg.uavarrivaltime());
        latestTelemetry->set_update(msg.update());

        if (msg.update() == TelemetryMessage::BatteryUpdate) {
            TelemetryMessage::BatteryInfo *battery = latestTelemetry->mutable_battery();
            battery->set_voltage_v(msg.battery().voltage_v());
            battery->set_remaining_percent(msg.battery().remaining_percent());
            battery->set_id(msg.battery().id());
        } else if (msg.update() == TelemetryMessage::PositionUpdate) {
            TelemetryMessage::PositionInfo *positionInfo = latestTelemetry->mutable_position();
            positionInfo->set_longitude_deg(msg.position().longitude_deg());
            positionInfo->set_latitude_deg(msg.position().latitude_deg());
            positionInfo->set_absolute_altitude_m(msg.position().absolute_altitude_m());
            positionInfo->set_relative_altitude_m(msg.position().relative_altitude_m());

//            std::cout << "UAV altitude: " << msg.position().absolute_altitude_m() << "\n";
        } else if (msg.update() == TelemetryMessage::PositionVelocityNedUpdate) {
            TelemetryMessage::PositionVelocityNed posVelNed = latestTelemetry->positionvelocityned();
            TelemetryMessage::PositionVelocityNed::PositionNed *pos = latestTelemetry->mutable_positionvelocityned()->mutable_position();
            pos->set_north_m(msg.positionvelocityned().position().north_m());
            pos->set_east_m(msg.positionvelocityned().position().east_m());
            pos->set_down_m(msg.positionvelocityned().position().down_m());

            TelemetryMessage::PositionVelocityNed::VelocityNed *vel = latestTelemetry->mutable_positionvelocityned()->mutable_velocity();
            vel->set_north_m_s(msg.positionvelocityned().velocity().north_m_s());
            vel->set_east_m_s(msg.positionvelocityned().velocity().east_m_s());
            vel->set_down_m_s(msg.positionvelocityned().velocity().down_m_s());
        }

    } else {
        uavLastTelemetry.emplace(std::make_pair(msg.uavid(), msg));
    }
//    std::cout << "Altitude: " << msg. << std::endl;
}

void GCSApp::TelemetryThread(void) {

    while (m_running) {
        if (!uavLastTelemetry.empty()) {
            for (const auto &uavTelemetry: uavLastTelemetry) {
                TelemetryMessage telemetryMessage = uavTelemetry.second;

//                PrintTelemetry(telemetryMessage);

                uavTelemetryTraceFile << Simulator::Now().GetMilliSeconds() << ",\t";
                uavTelemetryTraceFile << telemetryMessage.uavid() << ",\t";
                uavTelemetryTraceFile << telemetryMessage.uavarrivaltime() << ",\t";
                uavTelemetryTraceFile << telemetryMessage.gcsarrivaltime() << ",\t";
                uavTelemetryTraceFile << telemetryMessage.gcsarrivaltime() - telemetryMessage.uavarrivaltime() << ",\t";
                uavTelemetryTraceFile << telemetryMessage.gcsarrivaltime() << ",\t";

                uavTelemetryTraceFile << telemetryMessage.position().latitude_deg() << ",\t";
                uavTelemetryTraceFile << telemetryMessage.position().longitude_deg() << ",\t";
                uavTelemetryTraceFile << telemetryMessage.position().relative_altitude_m() << ",\t";
                uavTelemetryTraceFile << telemetryMessage.position().absolute_altitude_m() << ",\t";

                uavTelemetryTraceFile << telemetryMessage.battery().remaining_percent() << ",\t";
                uavTelemetryTraceFile << telemetryMessage.battery().voltage_v() << ",\t";

                uavTelemetryTraceFile << telemetryMessage.positionvelocityned().position().north_m() << ",\t";
                uavTelemetryTraceFile << telemetryMessage.positionvelocityned().position().down_m() << ",\t";
                uavTelemetryTraceFile << telemetryMessage.positionvelocityned().position().east_m() << ",\t";

                uavTelemetryTraceFile << telemetryMessage.positionvelocityned().velocity().north_m_s() << ",\t";
                uavTelemetryTraceFile << telemetryMessage.positionvelocityned().velocity().down_m_s() << ",\t";
                uavTelemetryTraceFile << telemetryMessage.positionvelocityned().velocity().east_m_s() << "\n";

                uavTelemetryTraceFile.flush();

                //                std::cout << n.first << " = " << n.second << "; ";
                sleep_for(milliseconds(500));
            }
        }

    }

}

void GCSApp::PrintTelemetry(const TelemetryMessage &telemetryMessage) const {
    std::cout << "########### UAV INFO Begin #############\n";

    std::cout << "UAV ID: " << telemetryMessage.uavid() << "\n";
    std::cout << "Last telemetry delay: "
              << telemetryMessage.gcsarrivaltime() - telemetryMessage.uavarrivaltime() << " ms\n";

    std::cout << "Position: \n";
    std::cout << "\t Latitude: " << telemetryMessage.position().latitude_deg() << "\n";
    std::cout << "\t Longitude: " << telemetryMessage.position().longitude_deg() << "\n";
    std::cout << "\t Relative Altitude: " << telemetryMessage.position().relative_altitude_m() << "\n";
    std::cout << "\t Absolute Altitude: " << telemetryMessage.position().absolute_altitude_m() << "\n";

    std::cout << "Battery: \n";
    std::cout << "\t Remaining: " << telemetryMessage.battery().remaining_percent() << "\n";
    std::cout << "\t Voltage: " << telemetryMessage.battery().voltage_v() << "\n";

    std::cout << "PositionVelocityNed: \n";
    std::cout << "\tPosition: \n";
    std::cout << "\t\t North: " << telemetryMessage.positionvelocityned().position().north_m() << "\n";
    std::cout << "\t\t Down: " << telemetryMessage.positionvelocityned().position().down_m() << "\n";
    std::cout << "\t\t East: " << telemetryMessage.positionvelocityned().position().east_m() << "\n";
    std::cout << "\tVelocity: \n";
    std::cout << "\t\t North: " << telemetryMessage.positionvelocityned().velocity().north_m_s() << "\n";
    std::cout << "\t\t Down: " << telemetryMessage.positionvelocityned().velocity().down_m_s() << "\n";
    std::cout << "\t\t East: " << telemetryMessage.positionvelocityned().velocity().east_m_s() << "\n";

    std::cout << "########### UAV INFO End #############\n\n";
}

void GCSApp::ArmAndTakeoff(float alt) {
    ControlMessage msg = CreateNewMessage();
    msg.set_command(ControlMessage::ARM_AND_TAKEOFF);
    msg.set_altitude(alt);

    SendCommand(msg);
}

void GCSApp::ArmAndStartMission() {
    ControlMessage msg = CreateNewMessage();
    msg.set_command(ControlMessage::ARM_AND_START_MISSION);

    SendCommand(msg);
}

void GCSApp::Land() {
    ControlMessage msg = CreateNewMessage();
    msg.set_command(ControlMessage::LAND);
    SendCommand(msg);
}

ControlMessage GCSApp::CreateNewMessage() const {
    ControlMessage msg;
    msg.set_uavid(1);
    msg.set_senttime(Simulator::Now().GetMilliSeconds());

    return msg;
}

void GCSApp::SendCommand(const ControlMessage &msg) {
    std::string serializedMsg = msg.SerializeAsString();
    std::vector<uint8_t> serializedMsgInUint(serializedMsg.begin(), serializedMsg.end());
    if (senderSocket->Send(&serializedMsgInUint[0], serializedMsgInUint.size(), 1) > 0) {
        std::cout << "Command Sent Successfully.\n";
    } else {
        std::cerr << "Couldn't Send the Command.\n";
    }
}

void make_mission_item(
        ControlMessage::MissionItem *missionItem,
        uint32_t seq,
        uint32_t current,
        uint32_t frame,
        double latitude_deg,
        double longitude_deg,
        float relative_altitude_m,
        uint32_t mission_type,
        uint32_t command,
        float p1,
        float p2,
        float p3,
        float p4) {

    missionItem->set_seq(seq);
    missionItem->set_frame(frame);
    missionItem->set_current(current);
    missionItem->set_command(command);
    missionItem->set_autocontinue(1);
    missionItem->set_x(int32_t(std::round(latitude_deg * 1e7)));
    missionItem->set_y(int32_t(std::round(longitude_deg * 1e7)));
    missionItem->set_z(relative_altitude_m);
    missionItem->set_mission_type(mission_type);

    missionItem->set_param1(p1);
    missionItem->set_param2(p2);
    missionItem->set_param3(p3);
    missionItem->set_param4(p4);

}

void GCSApp::InitUAV() {

//    ControlMessage msg = CreateNewMessage();
//    msg.set_command(ControlMessage::UPLOAD_MISSION);
//
//    uint32_t seq = 0;
//    make_mission_item(msg.add_missionitems(), seq++, 1, MAV_FRAME_GLOBAL_RELATIVE_ALT,
//                      38.952098, -95.264293, 0,
//                      MAV_MISSION_TYPE_MISSION, MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0);
//
//
//    make_mission_item(msg.add_missionitems(), seq++, 0, MAV_FRAME_GLOBAL_RELATIVE_ALT,
//                      38.952098, -95.264293, 20,
//                      MAV_MISSION_TYPE_MISSION, MAV_CMD_NAV_TAKEOFF, 0, 0, 0, 0);
//
//    make_mission_item(msg.add_missionitems(), seq++, 0, MAV_FRAME_GLOBAL_RELATIVE_ALT,
//                      38.955002, -95.262816, 20,
//                      MAV_MISSION_TYPE_MISSION, MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0);
//
//    make_mission_item(msg.add_missionitems(), seq++, 0, MAV_FRAME_GLOBAL_RELATIVE_ALT,
//                      38.955002, -95.262816, 0,
//                      MAV_MISSION_TYPE_MISSION, MAV_CMD_DO_CHANGE_SPEED, 1, 30, -1, 0);
//
//    make_mission_item(msg.add_missionitems(), seq++, 0, MAV_FRAME_GLOBAL_RELATIVE_ALT,
//                      38.955402, -95.257062, 20,
//                      MAV_MISSION_TYPE_MISSION, MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0);
//
//    make_mission_item(msg.add_missionitems(), seq++, 0, MAV_FRAME_GLOBAL_RELATIVE_ALT,
//                      38.952416, -95.257472, 20,
//                      MAV_MISSION_TYPE_MISSION, MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0);
//    make_mission_item(msg.add_missionitems(), seq++, 0, MAV_FRAME_GLOBAL_RELATIVE_ALT,
//                      38.952048, -95.263763, 20,
//                      MAV_MISSION_TYPE_MISSION, MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0);
//
//    make_mission_item(msg.add_missionitems(), seq++, 0, MAV_FRAME_GLOBAL_RELATIVE_ALT,
//                      0, 0, 0,
//                      MAV_MISSION_TYPE_MISSION, MAV_CMD_DO_JUMP, 2, 10, 0, 0);


    ControlMessage msg = missionCreator(gcsID);
    SendCommand(msg);

    ArmAndStartMission();

//    ArmAndTakeoff(10.0f);
//
//    Time tNext(Seconds(15.1));
//    Simulator::Schedule(tNext, &GCSApp::GoTo, this, 38.95381252261502, -95.26538584368772, 10.0f, 45.0f);
////    GoTo(38.95381252261502, -95.26538584368772, 10.0f, 45.0f);
//
//    Time t2(Seconds(25.1));
//    Simulator::Schedule(t2, &GCSApp::Land, this);
//    Land();
}

void GCSApp::GoTo(double latitude, double longitude, float altitude, float yaw) {
    ControlMessage msg = CreateNewMessage();
    msg.set_command(ControlMessage::GO_TO);
    msg.set_latitude(latitude);
    msg.set_longitude(longitude);
    msg.set_altitude(altitude);
    msg.set_yaw(yaw);

    SendCommand(msg);
}

void GCSApp::EnableTelemetryTrace(std::string filename) {
    uavTelemetryTraceFile.open(filename.c_str());
    uavTelemetryTraceFile << "#\t";
    uavTelemetryTraceFile << "Time\t";
    uavTelemetryTraceFile << "UAV_ID\t";
    uavTelemetryTraceFile << "UAV_Arrival\t";
    uavTelemetryTraceFile << "GCS_Arrival\t";
    uavTelemetryTraceFile << "Delay\t";

    uavTelemetryTraceFile << "Latitude\t";
    uavTelemetryTraceFile << "Longitude\t";
    uavTelemetryTraceFile << "RelativeAltitude\t";
    uavTelemetryTraceFile << "Absolute Altitude\t";

    uavTelemetryTraceFile << "RemainingBattery\t";
    uavTelemetryTraceFile << "BatteryVoltage\t";

    uavTelemetryTraceFile << "PositionNorth\t";
    uavTelemetryTraceFile << "PositionDown\t";
    uavTelemetryTraceFile << "PositionEast\t";

    uavTelemetryTraceFile << "VelocityNorth\t";
    uavTelemetryTraceFile << "VelocityDown\t";
    uavTelemetryTraceFile << "VelocityEast\n";

}

void GCSApp::SetMissionCreator(Callback<ControlMessage, int32_t> mission) {
    missionCreator = mission;
}





