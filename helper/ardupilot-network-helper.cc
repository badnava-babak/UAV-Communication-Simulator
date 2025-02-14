/* -*- Mode:C++; c-file-style:"gnu"; indent-tabs-mode:nil; -*- */

#include "ardupilot-network-helper.h"

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

namespace ns3 {
    NS_LOG_COMPONENT_DEFINE ("ArdupilotNetworkHelper");

    NS_OBJECT_ENSURE_REGISTERED (ArdupilotNetworkHelper);


    ArdupilotNetworkHelper::ArdupilotNetworkHelper(void) {

    }

    ArdupilotNetworkHelper::~ArdupilotNetworkHelper(void) {

    }

    TypeId ArdupilotNetworkHelper::GetTypeId(void) {
        static TypeId
                tid =
                TypeId("ns3::ArdupilotNetworkHelper")
                        .SetParent<Object>()
                        .AddConstructor<ArdupilotNetworkHelper>();
        return tid;
    }

    void ArdupilotNetworkHelper::DoDispose(void) {
        Object::DoDispose();
    }

    void
    ArdupilotNetworkHelper::SetupLteNetwork(NodeContainer &nodes, NodeContainer &enbNodes, Ptr<Node> &remoteNode,
                                            Ipv4InterfaceContainer &ueIpIfaceList,
                                            Ipv4Address &remoteHostAddr
    ) {

        /********************* Configure Default LTE Parameters ****************************/
        Config::SetDefault("ns3::LteSpectrumPhy::CtrlErrorModelEnabled", BooleanValue(false));
        Config::SetDefault("ns3::LteSpectrumPhy::DataErrorModelEnabled", BooleanValue(true));
        Config::SetDefault("ns3::PfFfMacScheduler::HarqEnabled", BooleanValue(false));
        Config::SetDefault("ns3::PfFfMacScheduler::CqiTimerThreshold", UintegerValue(10));
        Config::SetDefault("ns3::LteEnbRrc::EpsBearerToRlcMapping", EnumValue(LteEnbRrc::RLC_AM_ALWAYS));
        Config::SetDefault("ns3::LteEnbNetDevice::UlBandwidth", UintegerValue(100));
        Config::SetDefault("ns3::LteEnbNetDevice::DlBandwidth", UintegerValue(100));
        Config::SetDefault("ns3::LteUePhy::EnableUplinkPowerControl", BooleanValue(false));

        Ptr<LteHelper> lteHelper = CreateObject<LteHelper>();
        Ptr<PointToPointEpcHelper> epcHelper = CreateObject<PointToPointEpcHelper>();
        lteHelper->SetEpcHelper(epcHelper);

        //This creates the sgw/pgw node
        Ptr<Node> pgw = epcHelper->GetPgwNode();

        /*********************** INTERNET stack in EPC *********************************/
        PointToPointHelper p2ph;
        p2ph.SetDeviceAttribute("DataRate", DataRateValue(DataRate("100Gb/s")));
        p2ph.SetDeviceAttribute("Mtu", UintegerValue(1500));
        p2ph.SetChannelAttribute("Delay", TimeValue(Seconds(0.00001)));

        NetDeviceContainer internetDevices = p2ph.Install(pgw, remoteNode);

        Ipv4AddressHelper ipv4h;
        ipv4h.SetBase("1.0.0.0", "255.0.0.0");
        Ipv4InterfaceContainer internetIpIfaces = ipv4h.Assign(internetDevices);
        remoteHostAddr = internetIpIfaces.GetAddress(1);


        Ipv4StaticRoutingHelper ipv4RoutingHelper;


        MobilityHelper enbMobilityHelper;
        enbMobilityHelper.SetPositionAllocator("ns3::RandomBoxPositionAllocator",
                                               "X", StringValue("ns3::UniformRandomVariable[Min=-460351|Max=-449450]"),
                                               "Y",
                                               StringValue("ns3::UniformRandomVariable[Min=-4934130|Max=-4931890]"),
                                               "Z", StringValue("ns3::UniformRandomVariable[Min=4004000|Max=4008170]"));
        enbMobilityHelper.Install(enbNodes);


        /**************** Scheduler, Propagation and Fading *********************/
        lteHelper->SetHandoverAlgorithmType("ns3::A3RsrpHandoverAlgorithm");
        lteHelper->SetHandoverAlgorithmAttribute("Hysteresis", DoubleValue(3.5));
        lteHelper->SetHandoverAlgorithmAttribute("TimeToTrigger", TimeValue(MilliSeconds(256)));


        Ptr<ChannelConditionModel> losCondModel = CreateObject<ThreeGppUmaChannelConditionModel>();
        lteHelper->SetAttribute("PathlossModel", StringValue("ns3::ThreeGppV2vUrbanPropagationLossModel"));
        lteHelper->SetPathlossModelAttribute("ShadowingEnabled", BooleanValue(true));
        lteHelper->SetPathlossModelAttribute("ChannelConditionModel", PointerValue(losCondModel));

        /*************** Create Devices **************************/
        NetDeviceContainer enbDevices;
        enbDevices = lteHelper->InstallEnbDevice(enbNodes);

        for (NetDeviceContainer::Iterator it = enbDevices.Begin(); it != enbDevices.End(); ++it) {
            Ptr<LteEnbRrc> enbRrc = (*it)->GetObject<LteEnbNetDevice>()->GetRrc();
            enbRrc->SetAttribute("AdmitHandoverRequest", BooleanValue(true));
        }

        NetDeviceContainer uavDevices;
        uavDevices = lteHelper->InstallUeDevice(nodes);

        /******************* INTERNET Stack in LTE ***********************/

        // assign IP address to UEs
        for (uint32_t u = 0; u < nodes.GetN(); ++u) {
            Ptr<Node> ue = nodes.Get(u);
            Ptr<NetDevice> ueLteDevice = uavDevices.Get(u);
            Ipv4InterfaceContainer ueIpIface = epcHelper->AssignUeIpv4Address(NetDeviceContainer(ueLteDevice));
            ueIpIfaceList.Add(ueIpIface);

            // set the default gateway for the UE
            Ptr<Ipv4StaticRouting> ueStaticRouting = ipv4RoutingHelper.GetStaticRouting(ue->GetObject<Ipv4>());
            ueStaticRouting->SetDefaultRoute(epcHelper->GetUeDefaultGatewayAddress(), 1);

            lteHelper->AttachToClosestEnb(ueLteDevice, enbDevices);
            lteHelper->ActivateDedicatedEpsBearer(ueLteDevice,
                                                  EpsBearer(EpsBearer::NGBR_VIDEO_TCP_DEFAULT),
                                                  EpcTft::Default());
        }


        Ptr<Ipv4StaticRouting> remoteHostStaticRouting = ipv4RoutingHelper.GetStaticRouting(
                remoteNode->GetObject<Ipv4>());
        remoteHostStaticRouting->AddNetworkRouteTo(Ipv4Address("7.0.0.0"), Ipv4Mask("255.0.0.0"), 1);

        lteHelper->EnableTraces();
        p2ph.EnablePcapAll(std::string("uav-net-sim"));
    }
}

