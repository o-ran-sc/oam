# Service Management and Orchestration (SMO)

With respect to OAM the SMO implements the O1-interface provider. According to the O-RAN OAM Architecture and the O-RAN OAM Interface Specification, the SMO has a NetConf Client for configuration and HTTP/REST/VES Server for receiving all kind of events in a VES format. 

The setup contains an OpenDaylight based NetConf client and a VES Test Collector.

## Overview

This docker-compose file starts a pre-configured, self-contained SDN-R solution for developer test or demo purposes

  * **SDN-R** single node instance

    ... representing the NetConf consumer on the Service Management and Orchstration framework (SMO) for the O1 interface.
    ODL-Neon/CCSDK/SDNC-ElAlto

  * **VES test collector**

    ... representing the VES (REST) provider at SMO for all kind of events.
    DCAE-ElAlto/VES 5.0

  * **NTSDevice simulator**

    ... represents the NetConf Provider of an O-RAN component.

  * **NetconfServerSimulator** 

    ... another simulator

## Prerequisites

docker-compose file version 3.3 is used and tested with

  * Ubuntu 18.04 LTS
  * Docker version 19.03.x
  * docker-compose version 1.24.x
  * git version 2.17.1
  * docker-compose for the solution
  * enable git private docker registry, if used

```
cat /etc/os-release
docker --version
docker-compose --version
git --version
cd 
mkdir git
cd git
git clone  https://git-highstreet-technologies.com/highstreet/CICD_environment.git
cd CICD_environment/docker/solution/o-ran-dev
```

## Usage

### Bring Up Solution 

  * Check (adjust if required) environment variables

```
cd ~/git/CICD_environment/docker/solution/o-ran-dev
nano .env
```
  
  * startup solution 

```
cd ~/git/CICD_environment/docker/solution/o-ran-dev
docker-compose up -d
```

### Log files and karaf console

  * ODL karaf.logs can be found on docker host
```
tail -f /var/tmp/sdnr/logs/karaf.log
```

  * karaf console access (karaf:karaf)

```
ssh karaf@localhost -p 8101
```

  * ves-testcollector logs

```
  tail -f /var/tmp/ves-v5/logs/evel-output.log
```

### Customizing Solution

'.env' file contains customizing parameters


### Verification Solution

#### Access to SDN-R UX

  * login into SDN-R
    http://<host_ip>:8181/odlux/index.html
    User:admin
    Password:admin

#### Connectivity NETCONF interface to simulator of type 'NTSdevice'

  * Mount simulated network element (default parameters if not changed in '.env'
    * Open 'Connect'
    * Required Network Elements: add ('+' sign)
    * Name: NTSDevice
    * IP: <host_ip>
    * Port: 2240
    * User: netconf
    * Password: netconf
    
  Network Element 'NTSDevice' Should be connected

#### Connectivity NETCONF interface to simulator of type 'netconfserversimulator'

  * Mount simulated network element (default parameters if not changed in '.env'
    * Open 'Connect'
    * Required Network Elements: add ('+' sign)
    * Name: SIMTEST
    * IP: <host_ip>
    * Port: 2230
    * User: admin
    * Password: admin

  Network Element 'SIMTEST' Should be connected


#### Connectivity SDN-R to VES-testcollector 
  * verify VES-testcollector on host terminal
  ```
  tail -f /var/tmp/ves-v5/logs/evel-output.log
  ```
  
  * heart beat events should be visible
    
  ```
  Authenticated OK
==== Wed Aug 14 12:28:51 2019 =================================================
Valid body decoded & checked against schema OK:
{
    "event": {
        "commonEventHeader": {
            "domain": "heartbeat",
            "eventId": "testpattern-ab305d54-85b4-a31b-7db2-fb6b9e546015",
            "eventName": "heartbeat_Controller",
            "eventType": "Controller",
            "lastEpochMicrosec": 11087481660,
            "priority": "Low",
            "reportingEntityId": "",
            "reportingEntityName": "bf0c1c6deac1",
            "sequence": 7,
            "sourceId": "",
            "sourceName": "bf0c1c6deac1",
            "startEpochMicrosec": 11087481660,
            "version": 3.0
        },
        "heartbeatFields": {
            "additionalFields": [
                {
                    "name": "eventTime",
                    "value": "2019-08-14T12:28:51.5Z"
                }
            ],
            "heartbeatFieldsVersion": 1.0,
            "heartbeatInterval": 30
        }
    }
}172.20.0.3 - - [14/Aug/2019 12:28:51] "POST /eventListener/v5 HTTP/1.1" 202 0

  ```
#### Verify e2e event flow from 'NTSDevice' to VES-testcollector

NTSDevice simulator raise new alarms every 60 seconds. Time interval can be configured within .env file
This alarm shoulld be visible within the ves testcollector log file


#### Verify e2e event flow from 'netconfserversimulator' to VES-testcollector

Raise test event via device simulator and check VES log file
  
* login to simulator with admin:admin

  ```
  ssh admin@<host_IP> -p 8000
  
  ```
  * type 'n2'  (or 'n1') for m and clear event
 
  
```
==== Wed Aug 14 12:36:34 2019 =================================================
Valid body decoded & checked against schema OK:
{
    "event": {
        "commonEventHeader": {
            "domain": "fault",
            "eventId": "SIMTEST_LP-MWPS-RADIO_signalIsLostMajor",
            "eventName": "fault_Microwave_Radio_Alarms_signalIsLostMajor",
            "eventType": "Microwave_Radio_Alarms",
            "lastEpochMicrosec": 1565786194600000,
            "priority": "High",
            "reportingEntityId": "",
            "reportingEntityName": "bf0c1c6deac1",
            "sequence": 23,
            "sourceId": "",
            "sourceName": "SIMTEST",
            "startEpochMicrosec": 1565786194600000,
            "version": 3.0
        },
        "faultFields": {
            "alarmAdditionalInformation": [
                {
                    "name": "eventTime",
                    "value": "2019-08-14T12:36:34.6Z"
                },
                {
                    "name": "equipType",
                    "value": "unknown"
                },
                {
                    "name": "vendor",
                    "value": "unknown"
                },
                {
                    "name": "model",
                    "value": "unknown"
                }
            ],
            "alarmCondition": "signalIsLostMajor",
            "alarmInterfaceA": "LP-MWPS-RADIO",
            "eventSeverity": "MAJOR",
            "eventSourceType": "Microwave_Radio",
            "faultFieldsVersion": 2.0,
            "specificProblem": "signalIsLostMajor",
            "vfStatus": "Active"
        }
    }
}172.20.0.3 - - [14/Aug/2019 12:36:34] "POST /eventListener/v5 HTTP/1.1" 202 0
```
  * type '~.' to exit ssh
  * 
  
### Terminate solution

To stop all container:

```
cd ~/git/CICD_environment/docker/solution/o-ran-dev
docker-compose down
```

re-start solution at any point in time with 
```
cd ~/git/CICD_environment/docker/solution/o-ran-dev
docker-compose up -d
```


### Cleanup

!!! be careful if other stopped containers are on the same system
```
docker system prune -a -f
sudo rm -rf /var/tmp/ves-v5/

```
### Troubleshooting

Issue: no VES events, no heartbeat events
  * For some reasons SDN-R overwrites DCAE settings in devicemanager.properties.

```
sudo docker-compose down
git checkout -- devicemanager.properties
sudo docker-compose up -d
```