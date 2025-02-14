/* -*- Mode:C++; c-file-style:"gnu"; indent-tabs-mode:nil; -*- */

#include "ns3/core-module.h"
#include "ns3/ardupilot-helper.h"

#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/mobility-module.h"
#include "ns3/lte-module.h"
#include "ns3/config-store.h"
#include <ns3/buildings-helper.h>
#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/mobility-module.h"
#include "ns3/wifi-module.h"
#include "ns3/internet-module.h"
#include "ns3/applications-module.h"
#include "ns3/ipv4-global-routing-helper.h"
#include "ns3/lte-helper.h"
#include "ns3/epc-helper.h"
#include "ns3/lte-module.h"
#include "ns3/point-to-point-module.h"
#include "ns3/csma-module.h"
#include "ns3/channel-condition-model.h"

#include "ns3/UAVApp.h"
#include "ns3/GCSApp.h"
#include "ns3/UAVSimInfo.h"
#include <mavsdk/plugins/mavlink_passthrough/mavlink_passthrough.h>

using namespace ns3;



//UAVSimInfo gcsSimInfo = UAVSimInfo(38.95209759531131, -95.26429358856721, 0, "");


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

ControlMessage Mission1(int32_t uavID) {

    ControlMessage msg;
    msg.set_uavid(uavID);
    msg.set_senttime(Simulator::Now().GetMilliSeconds());

    msg.set_command(ControlMessage::UPLOAD_MISSION);

    uint32_t seq = 0;
    make_mission_item(msg.add_missionitems(), seq++, 1, MAV_FRAME_GLOBAL_RELATIVE_ALT,
                      38.952098, -95.264293, 0,
                      MAV_MISSION_TYPE_MISSION, MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0);


    make_mission_item(msg.add_missionitems(), seq++, 0, MAV_FRAME_GLOBAL_RELATIVE_ALT,
                      38.952098, -95.264293, 20,
                      MAV_MISSION_TYPE_MISSION, MAV_CMD_NAV_TAKEOFF, 0, 0, 0, 0);

    make_mission_item(msg.add_missionitems(), seq++, 0, MAV_FRAME_GLOBAL_RELATIVE_ALT,
                      38.955002, -95.262816, 20,
                      MAV_MISSION_TYPE_MISSION, MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0);

    make_mission_item(msg.add_missionitems(), seq++, 0, MAV_FRAME_GLOBAL_RELATIVE_ALT,
                      38.955002, -95.262816, 0,
                      MAV_MISSION_TYPE_MISSION, MAV_CMD_DO_CHANGE_SPEED, 1, 30, -1, 0);

    make_mission_item(msg.add_missionitems(), seq++, 0, MAV_FRAME_GLOBAL_RELATIVE_ALT,
                      38.955402, -95.257062, 20,
                      MAV_MISSION_TYPE_MISSION, MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0);

    make_mission_item(msg.add_missionitems(), seq++, 0, MAV_FRAME_GLOBAL_RELATIVE_ALT,
                      38.952416, -95.257472, 20,
                      MAV_MISSION_TYPE_MISSION, MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0);
    make_mission_item(msg.add_missionitems(), seq++, 0, MAV_FRAME_GLOBAL_RELATIVE_ALT,
                      38.952048, -95.263763, 20,
                      MAV_MISSION_TYPE_MISSION, MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0);

    make_mission_item(msg.add_missionitems(), seq++, 0, MAV_FRAME_GLOBAL_RELATIVE_ALT,
                      0, 0, 0,
                      MAV_MISSION_TYPE_MISSION, MAV_CMD_DO_JUMP, 2, 10, 0, 0);

    return msg;
}

ControlMessage Mission2(int32_t uavID) {

    ControlMessage msg;
    msg.set_uavid(uavID);
    msg.set_senttime(Simulator::Now().GetMilliSeconds());

    msg.set_command(ControlMessage::UPLOAD_MISSION);


    uint32_t seq = 0;
    make_mission_item(msg.add_missionitems(), seq++, 1, MAV_FRAME_GLOBAL_RELATIVE_ALT,
                      38.952098, -95.264293, 0,
                      MAV_MISSION_TYPE_MISSION, MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0);


    make_mission_item(msg.add_missionitems(), seq++, 0, MAV_FRAME_GLOBAL_RELATIVE_ALT,
                      38.952098, -95.264293, 20,
                      MAV_MISSION_TYPE_MISSION, MAV_CMD_NAV_TAKEOFF, 0, 0, 0, 0);

    make_mission_item(msg.add_missionitems(), seq++, 0, MAV_FRAME_GLOBAL_RELATIVE_ALT,
                      38.9518304000, -95.2547072000, 20,
                      MAV_MISSION_TYPE_MISSION, MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0);

    make_mission_item(msg.add_missionitems(), seq++, 0, MAV_FRAME_GLOBAL_RELATIVE_ALT,
                      38.9581216000, -95.2358656000, 0,
                      MAV_MISSION_TYPE_MISSION, MAV_CMD_NAV_WAYPOINT, 1, 30, -1, 0);

    make_mission_item(msg.add_missionitems(), seq++, 0, MAV_FRAME_GLOBAL_RELATIVE_ALT,
                      38.9637440000, -95.2463360000, 20,
                      MAV_MISSION_TYPE_MISSION, MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0);

    make_mission_item(msg.add_missionitems(), seq++, 0, MAV_FRAME_GLOBAL_RELATIVE_ALT,
                      38.9577408000, -95.2526464000, 20,
                      MAV_MISSION_TYPE_MISSION, MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0);
    make_mission_item(msg.add_missionitems(), seq++, 0, MAV_FRAME_GLOBAL_RELATIVE_ALT,
                      38.9550208000, -95.2629824000, 20,
                      MAV_MISSION_TYPE_MISSION, MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0);

    make_mission_item(msg.add_missionitems(), seq++, 0, MAV_FRAME_GLOBAL_RELATIVE_ALT,
                      38.9526528000, -95.2641088000, 20,
                      MAV_MISSION_TYPE_MISSION, MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0);

    make_mission_item(msg.add_missionitems(), seq++, 0, MAV_FRAME_GLOBAL_RELATIVE_ALT,
                      0, 0, 0,
                      MAV_MISSION_TYPE_MISSION, MAV_CMD_DO_JUMP, 2, 10, 0, 0);

    return msg;
}


const static std::map<uint32_t, UAVSimInfo> simInfo = {
        {0, UAVSimInfo(38.95209759531131, -95.26429358856721, 0,
                       "tcp://127.0.0.1:6760", MakeCallback(&Mission1))},
        {1, UAVSimInfo(38.95209759531131, -95.26429358856721, 0,
                       "tcp://127.0.0.1:6770", MakeCallback(&Mission1))},
        {2, UAVSimInfo(38.95209759531131, -95.26429358856721, 0,
                       "tcp://127.0.0.1:6780", MakeCallback(&Mission1))},
};

void setupMobilityModelInitialPositions(NodeContainer allNodes) {
    MobilityHelper mobility;
//    mobility.SetMobilityModel("ns3::WaypointMobilityModel");
    mobility.SetMobilityModel("ns3::MyConstantPositionMobilityModel");
    mobility.Install(allNodes);

    for (uint32_t i = 0; i < allNodes.GetN(); i++) {
        Ptr<Node> refNode = allNodes.Get(i);
        Ptr<MobilityModel> mobilityModel = refNode->GetObject<MobilityModel>();

        UAVSimInfo initialInfo = simInfo.find(i)->second;
        Vector initialPos = GeographicPositions::GeographicToCartesianCoordinates(initialInfo.latitude,
                                                                                  initialInfo.longitude,
                                                                                  initialInfo.altitude,
                                                                                  GeographicPositions::SPHERE);
        mobilityModel->SetPosition(initialPos);
//        mobilityModel->Unref();
//        Waypoint wpt0(Seconds(0), initialPos);
//        mobilityModel->AddWaypoint(wpt0);
    }
}


int main(int argc, char *argv[]) {
    int nUAV = 3;
    int numENBNodes = 5;

    uint32_t m_dlEarfcn = 5330;
    uint32_t m_ulEarfcn = 23330;
    uint32_t m_ulBandwidth = 50;
    uint32_t m_dlBandwidth = 50;
    double m_ueTxPower = 23;
    double m_eNbTxPower = 46;
    DataRateValue m_linkDataRate = DataRateValue(DataRate("100Gb/s"));
    TimeValue m_linkDelay = MilliSeconds(1);
    uint32_t m_defaultTransmissionMode = 2; // Default Transmission Mode (SISO, MIMO Spatial Multiplexing, etc.

//    int nCong = 0;
//    float inputCongRate = 200.0;
//    int congPktSize = 1040;
//    std::string congRate = "2Mbps"; // This rate will not have any effect, actual rate is taken from inputCongRate

    // LogComponentEnableAll(LOG_ALL);
    GlobalValue::Bind("SimulatorImplementationType", StringValue("ns3::RealtimeSimulatorImpl"));
    Config::SetDefault("ns3::TcpSocket::SegmentSize", UintegerValue(1448));

//    Config::SetDefault("ns3::Ipv4GlobalRouting::RespondToInterfaceEvents", BooleanValue(true));


    /***************** Define the Network Physical Layer *******************/

    NodeContainer uavNodes;
    uavNodes.Create(nUAV);

    // Create a single RemoteHost
    NodeContainer gcsNodeContainer;
    gcsNodeContainer.Create(1);
    Ptr<Node> gcsNode = gcsNodeContainer.Get(0); // This remote host will be in GCS


    NodeContainer enbNodes;
    enbNodes.Create(numENBNodes);

    MobilityHelper enbMobilityHelper;
    enbMobilityHelper.SetPositionAllocator("ns3::RandomBoxPositionAllocator",
                                           "X",
                                           StringValue("ns3::UniformRandomVariable[Min=-460351|Max=-449450]"),
                                           "Y",
                                           StringValue("ns3::UniformRandomVariable[Min=-4934130|Max=-4931890]"),
                                           "Z",
                                           StringValue("ns3::UniformRandomVariable[Min=4004000|Max=4008170]")
    );
    enbMobilityHelper.Install(enbNodes);

    /********* Set Position and Mobility for WiFi Sta nodes *******/
    setupMobilityModelInitialPositions(uavNodes);



    /*********** Install IP stack on all WiFi Station nodes *********/
    InternetStackHelper internetStackHelper;
    internetStackHelper.Install(uavNodes);
    internetStackHelper.Install(gcsNode);

    /********************* Configure Default LTE Parameters ****************************/

    // Set the SRS periodicity to the highest value, to allow for as many
    // UEs in the same sector as possible
    Config::SetDefault("ns3::LteEnbRrc::SrsPeriodicity", UintegerValue(320));
    Config::SetDefault("ns3::LteEnbRrc::DefaultTransmissionMode", UintegerValue(m_defaultTransmissionMode));
    Config::SetDefault("ns3::LteRlcUm::MaxTxBufferSize", UintegerValue(2000 * 1024));
    Config::SetDefault("ns3::LteEnbPhy::TxPower", DoubleValue(m_eNbTxPower));
    Config::SetDefault("ns3::LteUePhy::TxPower", DoubleValue(m_ueTxPower));


    Config::SetDefault("ns3::LteSpectrumPhy::CtrlErrorModelEnabled", BooleanValue(false));
    Config::SetDefault("ns3::LteSpectrumPhy::DataErrorModelEnabled", BooleanValue(true));
//    Config::SetDefault("ns3::PfFfMacScheduler::HarqEnabled", BooleanValue(false));
    Config::SetDefault("ns3::PfFfMacScheduler::CqiTimerThreshold", UintegerValue(10));
    Config::SetDefault("ns3::LteEnbRrc::EpsBearerToRlcMapping", EnumValue(LteEnbRrc::RLC_AM_ALWAYS));
//    Config::SetDefault("ns3::LteEnbNetDevice::UlBandwidth", UintegerValue(100));
//    Config::SetDefault("ns3::LteEnbNetDevice::DlBandwidth", UintegerValue(100));
    Config::SetDefault("ns3::LteUePhy::EnableUplinkPowerControl", BooleanValue(false));

    Ptr<LteHelper> lteHelper = CreateObject<LteHelper>();
    Ptr<PointToPointEpcHelper> m_epcHelper = CreateObject<PointToPointEpcHelper>();
    m_epcHelper->SetAttribute("S1uLinkMtu", UintegerValue(15000));
    m_epcHelper->SetAttribute("S1uLinkDataRate", DataRateValue(m_linkDataRate));
    m_epcHelper->SetAttribute("S1uLinkDelay", TimeValue(m_linkDelay));
    m_epcHelper->SetAttribute("X2LinkMtu", UintegerValue(15000));
    lteHelper->SetEpcHelper(m_epcHelper);

    /**************** Scheduler, Propagation and Fading *********************/
    lteHelper->SetHandoverAlgorithmType("ns3::A3RsrpHandoverAlgorithm");
    lteHelper->SetHandoverAlgorithmAttribute("Hysteresis", DoubleValue(3.5));
    lteHelper->SetHandoverAlgorithmAttribute("TimeToTrigger", TimeValue(MilliSeconds(256)));


    Ptr<ChannelConditionModel> losCondModel = CreateObject<ThreeGppUmaChannelConditionModel>();
    lteHelper->SetAttribute("PathlossModel", StringValue("ns3::ThreeGppV2vUrbanPropagationLossModel"));
    lteHelper->SetPathlossModelAttribute("ShadowingEnabled", BooleanValue(true));
    lteHelper->SetPathlossModelAttribute("ChannelConditionModel", PointerValue(losCondModel));

    lteHelper->SetAttribute("UseIdealRrc", BooleanValue(false));
    lteHelper->SetEnbDeviceAttribute("DlBandwidth", UintegerValue(m_dlBandwidth));
    lteHelper->SetEnbDeviceAttribute("UlBandwidth", UintegerValue(m_ulBandwidth));
    lteHelper->SetSchedulerType("ns3::RrFfMacScheduler");
    lteHelper->SetSchedulerAttribute("HarqEnabled", BooleanValue(false));
    lteHelper->SetEnbDeviceAttribute("DlEarfcn", UintegerValue(m_dlEarfcn));
    lteHelper->SetEnbDeviceAttribute("UlEarfcn", UintegerValue(m_ulEarfcn));
    lteHelper->SetUeDeviceAttribute("DlEarfcn", UintegerValue(m_dlEarfcn));

    //This creates the sgw/pgw node
    Ptr<Node> pgw = m_epcHelper->GetPgwNode();

    /*********************** INTERNET stack in EPC *********************************/
    PointToPointHelper p2ph;
    p2ph.SetDeviceAttribute("DataRate", DataRateValue(DataRate("100Gb/s")));
    p2ph.SetDeviceAttribute("Mtu", UintegerValue(1500));
    p2ph.SetChannelAttribute("Delay", TimeValue(Seconds(0.00001)));

    NetDeviceContainer internetDevices = p2ph.Install(pgw, gcsNode);

    Ipv4AddressHelper ipv4h;
    ipv4h.SetBase("1.0.0.0", "255.0.0.0");
    Ipv4InterfaceContainer internetIpIfaces = ipv4h.Assign(internetDevices);

//    Ipv4Address remoteHostAddr = internetIpIfaces.GetAddress(1);
    Ipv4Address remoteHostAddr = gcsNode->GetObject<Ipv4>()->GetAddress(1, 0).GetAddress();


    Ipv4StaticRoutingHelper ipv4RoutingHelper;






    /*************** Create Devices **************************/
    NetDeviceContainer enbDevices;
    enbDevices = lteHelper->InstallEnbDevice(enbNodes);

    for (NetDeviceContainer::Iterator it = enbDevices.Begin(); it != enbDevices.End(); ++it) {
        Ptr<LteEnbRrc> enbRrc = (*it)->GetObject<LteEnbNetDevice>()->GetRrc();
        enbRrc->SetAttribute("AdmitHandoverRequest", BooleanValue(true));
    }

    NetDeviceContainer uavDevices;
    uavDevices = lteHelper->InstallUeDevice(uavNodes);

    /******************* INTERNET Stack in LTE ***********************/
    Ipv4InterfaceContainer ueIpIfaceList = m_epcHelper->AssignUeIpv4Address(uavDevices);
    // assign IP address to UEs
    for (uint32_t u = 0; u < uavNodes.GetN(); ++u) {
        Ptr<Node> ue = uavNodes.Get(u);

        // set the default gateway for the UE
        Ptr<Ipv4StaticRouting> ueStaticRouting = ipv4RoutingHelper.GetStaticRouting(ue->GetObject<Ipv4>());
        ueStaticRouting->SetDefaultRoute(m_epcHelper->GetUeDefaultGatewayAddress(), 1);

    }
    lteHelper->AttachToClosestEnb(uavDevices, enbDevices);
    lteHelper->ActivateDedicatedEpsBearer(uavDevices,
                                          EpsBearer(EpsBearer::NGBR_VIDEO_TCP_DEFAULT),
                                          EpcTft::Default());


    Ptr<Ipv4StaticRouting> remoteHostStaticRouting = ipv4RoutingHelper.GetStaticRouting(
            gcsNode->GetObject<Ipv4>());
    remoteHostStaticRouting->AddNetworkRouteTo(Ipv4Address("7.0.0.0"), Ipv4Mask("255.0.0.0"), 1);



    /************** LTE Uplink Data transfer for Telemetry *************/
    for (uint32_t i = 0; i < uavNodes.GetN(); ++i) {
        uint32_t uavBasePort = 10000 + (i + 1) * 100; /*10100, 10200, 10300, ... */
        std::cout << " UAV address: " << ueIpIfaceList.GetAddress(i) << std::endl;

        uint32_t communicationPort = uavBasePort + 1;

        std::cout << " MEC Address: " << remoteHostAddr << std::endl;
        Ptr<Node> node = uavNodes.Get(i);


        Ipv4Address ip = uavNodes.Get(i)->GetObject<Ipv4>()->GetAddress(1, 0).GetAddress();

        Ptr<GCSApp> gcsApp = CreateObject<GCSApp>();
        gcsApp->Setup(InetSocketAddress(ip, communicationPort),
                      InetSocketAddress(Ipv4Address::GetAny(), communicationPort),
                      gcsNode, i + 1);

        gcsApp->SetMissionCreator(simInfo.find(i)->second.missionCallback);

        gcsNode->AddApplication(gcsApp);
        gcsApp->SetStartTime(Seconds(0.0));

        Ptr<UAVApp> app = CreateObject<UAVApp>();
        app->Setup(InetSocketAddress(remoteHostAddr, communicationPort),
                   communicationPort,
                   node, i + 1, simInfo.find(i)->second.mavlinkAddress);
        uavNodes.Get(i)->AddApplication(app);
        app->SetStartTime(Seconds(0.0));


    }

    /*****************************************************/

    AsciiTraceHelper ascii;

    lteHelper->EnableTraces();
    p2ph.EnablePcapAll(std::string("uav-net-sim"));
    MobilityHelper::EnableAsciiAll(ascii.CreateFileStream("mobility-trace-example.mob"));

//    Ipv4GlobalRoutingHelper::PopulateRoutingTables ();

    Simulator::Stop(Seconds(10000.));
    Simulator::Run();
    Simulator::Destroy();
    return 0;
}
