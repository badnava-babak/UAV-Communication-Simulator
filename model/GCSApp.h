//
// Created by b502b586 on 11/8/21.
//

#ifndef GCSApp_H_
#define GCSApp_H_

#include <stdio.h>
#include <stdlib.h>
#include "ns3/core-module.h"
#include "ns3/applications-module.h"
#include "ns3/control-message.pb.h"
#include "ns3/telemetry-message.pb.h"
#include <mavsdk/mavsdk.h>
#include <mavsdk/plugins/action/action.h>
#include <mavsdk/plugins/telemetry/telemetry.h>
#include <iostream>
#include <future>
#include <memory>
#include <thread>

using namespace ns3;

class GCSApp : public Application {
public:
    GCSApp();

    virtual ~GCSApp();

    void Setup(const Address &uav, const Address &gcs, Ptr<Node> node, int32_t gcsID);
    void SetMissionCreator(Callback<ControlMessage, int32_t> mission);

private:
    virtual void StartApplication(void);

    virtual void StopApplication(void);

    void InitUAV();

    void ArmAndTakeoff(float alt);

    void ArmAndStartMission();

    void GoTo(double latitude, double longitude, float altitude, float yaw);

    void Land();

    void SendPacket(void);

    void ReceiveTelemetry(Ptr<Socket> socket);

    void TelemetryThread(void);


    Callback<ControlMessage, int32_t> missionCreator;


    int32_t gcsID;
    Ptr<Socket> senderSocket;
    Ptr<Socket> listenerSocket;
    Address uavAddress;
    Address gcsAddress;
    bool m_running;

    std::map<int32_t, TelemetryMessage> uavLastTelemetry;
    std::ofstream uavTelemetryTraceFile; //!< file stream for uav telemetry

    void EnableTelemetryTrace(std::string filename);

    Ptr<SystemThread> telemetryThread;

    void SendCommand(const ns3::ControlMessage &msg);

    ControlMessage CreateNewMessage() const;

    void PrintTelemetry(const TelemetryMessage &telemetryMessage) const;
};

#endif
