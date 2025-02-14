/* -*- Mode:C++; c-file-style:"gnu"; indent-tabs-mode:nil; -*- */
#ifndef ARDUPILOT_NETWORK_HELPER_H
#define ARDUPILOT_NETWORK_HELPER_H

#include <ns3/config.h>
#include <ns3/simulator.h>
#include <ns3/names.h>
#include <ns3/net-device.h>
#include <ns3/net-device-container.h>
#include <ns3/node.h>
#include <ns3/node-container.h>
#include <ns3/mobility-model.h>
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

#include "ns3/ardupilot.h"

namespace ns3 {
    class ArdupilotNetworkHelper : public Object {
    public:
        ArdupilotNetworkHelper(void);

        virtual ~ArdupilotNetworkHelper(void);

        /**
         *  Register this type.
         *  \return The object TypeId.
         */
        static TypeId GetTypeId(void);

        virtual void DoDispose(void);

        static void SetupLteNetwork(NodeContainer &nodes, NodeContainer &enbNodes, Ptr<Node> &remoteNode,
                             Ipv4InterfaceContainer &ueIpIfaceList,
                             Ipv4Address &remoteHostAddr);
    };

}

#endif /* ARDUPILOT_NETWORK_HELPER_H */

