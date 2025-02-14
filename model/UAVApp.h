//
// Created by b502b586 on 11/8/21.
//

#ifndef UAVApp_H_
#define UAVApp_H_

#include <stdio.h>
#include <stdlib.h>
#include "ns3/core-module.h"
#include "ns3/applications-module.h"
#include "ns3/control-message.pb.h"
#include "ns3/telemetry-message.pb.h"
#include "ns3/my-constant-position-mobility-model.h"
#include "my-constant-position-mobility-model.h"
#include <mavsdk/mavsdk.h>
#include <mavsdk/plugins/action/action.h>
#include <mavsdk/plugins/telemetry/telemetry.h>
#include <iostream>
#include <future>
#include <memory>
#include <thread>

using namespace ns3;

class UAVApp : public Application {
public:
    UAVApp();

    virtual ~UAVApp();

    void Setup(const Address &gcs, uint32_t port, Ptr<Node> node, int32_t id, std::string mavAddr);

private:
    virtual void StartApplication(void);

    virtual void StopApplication(void);

    void ReceiveCommand(Ptr<Socket> socket);

    void InitUAV();

    bool ArmAndTakeoff(float alt);
    bool ArmAndStartMission();
    bool UploadMission(ControlMessage msg);

    bool GoTo(double latitude, double longitude, float altitude, float yaw);

    bool Land();

    bool ReturnToLaunch();

    bool SetMaxSpeed(float speed);

    void SendPacket(void);

    void TelemetryThread(void);

    void CommandExecutionThread(void);

    Ptr<MyConstantPositionMobilityModel> GetMobility();



    int32_t uavID;
    std::string mavLinkAddr;

    Ptr<Socket> senderSocket;
    Ptr<Socket> listenerSocket;
    Address uavAddress;
    Address gcsAddress;
    bool m_running;

    mavsdk::Mavsdk mavsdk;
    std::shared_ptr<mavsdk::System> system;
    Ptr<SystemThread> telemetryThread;
    Ptr<SystemThread> controlThread;

    std::queue<ControlMessage> controlMessageQueue;
    Ptr<MyConstantPositionMobilityModel> mobilityModel;

    std::ofstream uavControlTraceFile; //!< file stream for uav telemetry

    void EnableControlTrace(std::string filename);

//    std::shared_ptr<mavsdk::Telemetry> telemetry;
//    std::shared_ptr<mavsdk::Action> action;

    void SendTelemetry(std::string &serializedMsg);

    ns3::ControlMessage ParseCommand(const Ptr<Packet> &packet) const;

    void Goto(const ControlMessage &msg) const;

    void Goto(double longititude, double latitude, float altitude, float yaw) const;

    ns3::TelemetryMessage *CreeateTelemetryMessage(TelemetryMessage_UpdateType type) const;
};

#endif
