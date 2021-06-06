# Service Management and Orchestration (SMO)

##### Table of Contents
[Service Management and Orchestration (SMO)](#service-management-and-orchestration-smo)
- [Introduction](#introduction)
- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Usage](#usage)
  - [Bring Up Solution](#bring-up-solution)
  - [Log files and karaf console](#log-files-and-karaf-console)
  - [Customizing Solution](#customizing-solution)
  - [Verification Solution](#verification-solution)
    - [Access to SDN-R UX](#access-to-sdn-r-ux)
  - [Terminate solution](#terminate-solution)
  - [Cleanup](#cleanup)
  - [Troubleshooting](#troubleshooting)

## Introduction

With respect to OAM the SMO implements the O1-interface consumers. According to the O-RAN OAM Architecture and the O-RAN OAM Interface Specification, the SMO implements a NetConf Client for configuration and a HTTP/REST/VES server for receiving all kind of events in a VES format.

The setup contains an OpenDaylight based NetConf client and a VES Collector.

## Overview

This docker-compose file starts a pre-configured, self-contained SDN-R solution 
for developer test or demo purposes

  * **Identity**
    ... representing an KeyCloak based identity service for centralized user 
    management. Please note that the implementation does not support IPv6. 
    Therefore, its own network is required called 'DMZ'.

  * **SDN-R** single node instance

    ... representing the NetConf consumer on the Service Management and 
    Orchestration framework (SMO) for the O1 interface based on 
    ODL-Silicon/ONAP-Istanbul

  * **VES collector**

    ... representing the VES (REST) provider at SMO for all kind of events.

  * **DMaaP**
    ... representing SMO DMaaP component, includes message-router

## Prerequisites

```
$ cat /etc/os-release | grep PRETTY_NAME
PRETTY_NAME="Ubuntu 20.04.2 LTS"

$ docker --version
Docker version 20.10.2, build 20.10.2-0ubuntu1~20.04.2

$ docker-compose version
docker-compose version 1.29.1, build c34c88b2
docker-py version: 5.0.0
CPython version: 3.7.10
OpenSSL version: OpenSSL 1.1.0l  10 Sep 2019

$ git --version
git version 2.25.1

```
Please modify the /etc/hosts of your system.

* <your-system>: is the hostname of the system, where the browser is started

* <deployment-system-ipv4>: is the IP address of the system where the solution will be deployed

For development purposes <your-system> and <deployment-system> may reference the same system.

```
$ cat /etc/hosts
127.0.0.1	              localhost
127.0.1.1	              <your-system>
<deployment-system-ipv4>   sdnc-web <your-system>
<deployment-system-ipv4>   identity <your-system>
```

## Expected Folder Structure

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
    ├── non-rt-ric
    │   ├── .env
    │   ├── docker-compose.yml
    │   │
    │   └── <config-folders>
    └── oam
        ├── docker-compose.yml
        │
        ├── sdnc-web
        ├── sdnr
        └── ves-collector
```

## Usage

### Bring Up Solution

#### Check (adjust if required) environment variables

```
nano smo/common/.env
nano smo/non-rt-ric/.env
nano smo/oam/.env
nano network/.env
```

#### Startup solution

Please note that it is necessary to configure first the identity service,
before starting further docker images.

The several docker-compose yml files must be started in the right order as listed below:

```
docker-compose -f smo/common/docker-compose.yml up -d 
python smo/common/identity/config.py 
```

The python script configure the users within the identity service (keycloak).
A system user (%USER) is also created with administration rights.

```
docker-compose -f smo/non-rt-ric/docker-compose.yml up -d 
docker-compose -f smo/oam/docker-compose.yml up -d 
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

#### karaf console access (karaf:karaf)

```
ssh karaf@localhost -p 8101
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
docker-compose -f smo/non-rt-ric/docker-compose.yml down 
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

## Prerequisites
# python3, tmux, libtmux
tmux new-session -n workspace -s integration

# within tmux session
python tmux-logging.py
```
... are your friends.

![tmux logging](docs/tmux-logging.png "tmux logging")