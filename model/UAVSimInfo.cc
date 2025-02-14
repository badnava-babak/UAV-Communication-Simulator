//
// Created by b502b586 on 11/8/21.
//

#include <iostream>
#include <fstream>
#include <string>
#include <stdio.h>
#include <stdlib.h>
#include "UAVSimInfo.h"
#include "ns3/core-module.h"

using namespace ns3;
NS_LOG_COMPONENT_DEFINE ("UAVSimInfo");

UAVSimInfo::UAVSimInfo() {

}

UAVSimInfo::~UAVSimInfo() {

}

UAVSimInfo::UAVSimInfo(double lat, double lon, double alt, std::string mavlinkAddr,
                       Callback<ControlMessage, int32_t> mission) {
    latitude = lat;
    longitude = lon;
    altitude = alt;
    mavlinkAddress = mavlinkAddr;
    missionCallback = mission;

}


