# Service Management and Orchestration (SMO)

This project focus on a docker-compose deployment solution for SMO/OAM Components.

## Introduction

With respect to OAM the SMO implements the O1-interface consumers.
According to the O-RAN OAM Architecture and the O-RAN OAM Interface Specification,
the SMO implements a NETCONF Client for configuration and a HTTP/REST/VES server
for receiving all kind of events in VES format.

The setup contains an OpenDaylight based NETCONF client and an ONAP VES Collector.

## SMO OAM Components

This docker-compose file starts a pre-configured, self-contained SDN-R solution
with the following components.

  * **Identity**
    ... representing an KeyCloak based identity service for centralized user
    management. Please note that the implementation does not support IPv6.
    Therefore, its own network is required called 'DMZ'.
    In this configuration the external https port is 8463.

  * **SDN-R** single node instance

    ... representing the NETCONF consumer on the Service Management and
    Orchestration framework (SMO) for the O1 interface based on
    ODL-Phosphorus.
    SDN-R comes with is own web-portal the external port is 8463.

  * **VES collector**

    ... representing the VES (REST) provider at SMO for all kind of events. In this configuration the external https port is 8443.

  * **DMaaP**
    ... representing SMO DMaaP component, includes message-router

## Prerequisites

```
$ cat /etc/os-release | grep PRETTY_NAME
PRETTY_NAME="Ubuntu 20.04.2 LTS"

$ docker --version
Docker version 20.10.7, build 20.10.7-0ubuntu1~20.04.2

$ docker-compose version
docker-compose version 1.29.1, build c34c88b2
docker-py version: 5.0.0
CPython version: 3.7.10
OpenSSL version: OpenSSL 1.1.0l  10 Sep 2019


$ git --version
git version 2.25.1

```
Please modify the /etc/hosts of your system.

* \<your-system>: is the hostname of the system, where the browser is started

* \<deployment-system-ipv4>: is the IP address of the system where the solution will be deployed

For development purposes <your-system> and <deployment-system> may reference the same system.

```
$ cat /etc/hosts
127.0.0.1	               localhost
127.0.1.1	               <your-system>
<deployment-system-ipv4>   sdnc-web <your-system>
<deployment-system-ipv4>   identity <your-system>
```

It is beneficial (but not mandatory) adding the following line add the
end of your ~/.bashrc file. I will suppress warnings when python script
do not verify self signed certificates for HTTPS communication.

```
export PYTHONWARNINGS="ignore:Unverified HTTPS request"
```

Please ensure that you download and copy the required 3GPP OpenAPIs for VES-stndDefined
message validation into the folder './solution/operation-and-maintenance/smo/oam/ves-collector/externalRepo'.

Please follow the instructions in ./solution/operation-and-maintenance/smo/oam/ves-collector/externalRepo/3gpp/rep/sa5/MnS/blob/Rel16/OpenAPI/README.md.

The following tree shows the successfully tested folder structure. It combines different versions of the schemas ('Rel16' and 'SA88-Rel16') using 3GPP branch names.

```
$ tree solution/operation-and-maintenance/smo/oam/ves-collector/externalRepo/
solution/operation-and-maintenance/smo/oam/ves-collector/externalRepo/
├── 3gpp
│   └── rep
│       └── sa5
│           └── MnS
│               └── blob
│                   ├── Rel16
│                   │   └── OpenAPI
│                   │       ├── 5gcNrm.yaml
│                   │       ├── PerfMeasJobCtrlMnS.yaml
│                   │       ├── README.md
│                   │       ├── comDefs.yaml
│                   │       ├── coslaNrm.yaml
│                   │       ├── faultMnS.yaml
│                   │       ├── fileDataReportingMnS.yaml
│                   │       ├── genericNrm.yaml
│                   │       ├── heartbeatNtf.yaml
│                   │       ├── nrNrm.yaml
│                   │       ├── perfMnS.yaml
│                   │       ├── provMnS.yaml
│                   │       ├── sliceNrm.yaml
│                   │       └── streamingDataMnS.yaml
│                   └── SA88-Rel16
│                       └── OpenAPI
│                           ├── 5gcNrm.yaml
│                           ├── PerDataFileReportMnS.yaml
│                           ├── PerMeasJobCtlMnS.yaml
│                           ├── PerThresMonMnS.yaml
│                           ├── PerfDataStreamingMnS.yaml
│                           ├── README.md
│                           ├── comDefs.yaml
│                           ├── coslaNrm.yaml
│                           ├── faultMnS.yaml
│                           ├── genericNrm.yaml
│                           ├── heartbeatNtf.yaml
│                           ├── nrNrm.yaml
│                           ├── provMnS.yaml
│                           ├── sliceNrm.yaml
│                           └── streamingDataMnS.yaml
```

## Expected Folder Structure

The following figure show the expected folder structure for the different
docker-compose file and its configurations.

```
├── network
│   ├── .env
│   ├── config.py
│   ├── docker-compose.yml
│   │
│   ├── ntsim-ng-o-du
│   └── ntsim-ng-o-ru
└── smo
    ├── common
    │   ├── .env
    │   ├── docker-compose.yml
    │   │
    │   ├── dmaap
    │   ├── docker
    │   ├── identity
    │   ├── kafka
    │   └── zookeeper
    └── oam
        ├── .env
        ├── docker-compose.yml
        │
        ├── web
        ├── controller
        └── ves-collector
```

## Usage

### Bring Up Solution

#### Short story

The following commands should be invoked. More detailed can be found in the
next chapters.

```
docker-compose -f smo/common/docker-compose.yml up -d
# wait until the cpu load is low again
python smo/common/identity/config.py

docker-compose -f smo/oam/docker-compose.yml up -d
# wait until the cpu load is low again

docker-compose -f network/docker-compose.yml up -d
# wait about 2min
docker restart ntsim-ng-o-du-1122
python network/config.py
```

#### Check (adjust if required) environment variables

```
nano smo/.env
nano network/.env
```

The tested configuration uses the following external https ports:

 * 8443 for the ves-collector
 * 8453 for web access to ODLUX (SDNC_WEB_PORT)
 * 8463 for the keyclock web administrator user interface.

#### Startup solution

Please note that it is necessary to configure first the identity service,
before starting further docker images.

The several docker-compose yml files must be started in the right order as listed below:

```
docker-compose -f smo/common/docker-compose.yml up -d
python smo/identity/config.py
```

The python script configure the users within the identity service (keycloak).
A system user (%USER) is also created with administration rights.


```
docker-compose -f smo/oam/docker-compose.yml up -d
python smo/identity/config.py
```

Please wait about 2min until all the service are up and running.
If you see the login page (https://sdnc-web:8453) you are good to go and can start the (simulated) network.

```
docker-compose -f network/docker-compose.yml up -d
```

Usually the first ves:event gets lost. Please restart the O-DU docker container(s) to send a second ves:pnfRegistration.

```
docker-compose -f network/docker-compose.yml restart ntsim-ng-o-du-1122
python network/config.py
```

The python script configures the simulated O-DU and O-RU according to O-RAN hybrid architecture.

O-DU - NETCONF Call HOME and NETCONF notifications
O-RU - ves:pnfRegistration and ves:fault, ves:heartbeat

![ves:pnfRegistration in ODLUX](docs/nstim-ng-connected-after-ves-pnf-registration-in-odlux.png "ves:pnfRegistration in ODLUX")

'True' indicated that the settings through SDN-R to the NETCONF server were
successful.

SDN-R reads the fault events from DMaaP and processes them.
Finally the fault events are visible in ODLUX.

![ves:fault in ODLUX](docs/ves-fault-in-odlux.png "ves:fault in ODLUX")


### Log files and karaf console

#### ODL karaf.logs

```
docker exec -it sdnr tail -f /opt/opendaylight/data/log/karaf.log
```

#### ves-collector logs

```
docker logs -f ves-collector
```

### Customizing Solution

'.env' file contains customizing parameters

### Verification Solution

#### Access to SDN-R ODLUX

##### Login into SDN-R

    https://sdnc-web:8453

    User: admin // see .env file

    Password: Kp8bJ4SXszM0WXlhak3eHlcse2gAw84vaoGGmJvUy2U

In case of trouble, please update the commands with your customized '.env' file.

### Terminate solution

To stop all container please respect the following order

```
docker-compose -f network/docker-compose.yml down
docker-compose -f smo/oam/docker-compose.yml down
docker-compose -f smo/common/docker-compose.yml down
```

### Cleanup

!!! be careful if other stopped containers are on the same system
```
docker system prune -a -f
```
### Troubleshooting

In most cases the .env setting do not fit to the environment and need to be
adjusted.

Please make sure that the network settings to not overlap with other networks.

The commands ...
```
docker ps -a
docker-compose ps