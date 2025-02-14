//
// Created by b502b586 on 11/8/21.
//

#ifndef UAVSimInfo_H_
#define UAVSimInfo_H_

#include "ns3/core-module.h"
#include "ns3/control-message.pb.h"
#include <stdio.h>
#include <stdlib.h>

using namespace ns3;

class UAVSimInfo {
public:
    UAVSimInfo();

    UAVSimInfo(double lat, double lon, double alt, std::string mavlinkAddr, Callback<ControlMessage, int32_t> mission);

    virtual ~UAVSimInfo();

    double latitude;
    double longitude;
    double altitude;
    std::string mavlinkAddress;
    Callback<ControlMessage, int32_t> missionCallback;

private:

};

#endif
