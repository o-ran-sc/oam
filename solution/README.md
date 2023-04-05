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

  * **Controller** single node instance

    ... representing the NETCONF consumer on the Service Management and
    Orchestration framework (SMO) for O-RAN O1 interface and/or O-RAN OpenFronthaul Management Plane and/or other NETCONF/YANG schemas implemented by the OpenDaylight project.

  * **VES collector**

    ... representing the VES (REST) provider at SMO for all kind of events.

  * **Messages**
    ... representing SMO MessageRouter component, includes message-router

## Prerequisites

### Operating (HOST) System

```
$ cat /etc/os-release | grep PRETTY_NAME
PRETTY_NAME="Ubuntu 22.04.2 LTS"
```

### Docker

```
$ docker --version
Docker version 23.0.1, build a5ee5b1
```
Please follow the required docker daemon configuration as documented in the following README.md:
- [./smo/common/docker/README.md](./smo/common/docker/README.md)

### Docker Compose

```
$ docker compose version
Docker Compose version v2.17.2
```

### GIT

```
$ git --version
git version 2.34.1
```

### Python

```
$ python3 --version
Python 3.10.6
```

A python parser package is required.
```
sudo apt install python3-pip
pip install jproperties
```

It is beneficial (but not mandatory) adding the following line add the
end of your ~/.bashrc file. I will suppress warnings when python script
do not verify self signed certificates for HTTPS communication.

```
export PYTHONWARNINGS="ignore:Unverified HTTPS request"
```

### ETC Host (DNS function)

Please modify the /etc/hosts of your system.

* \<your-system>: is the hostname of the system, where the browser is started

* \<deployment-system-ipv4>: is the IP address of the system where the solution will be deployed

For development purposes <your-system> and <deployment-system> may reference the same system.

```
$ cat /etc/hosts
127.0.0.1	               localhost
127.0.1.1	               <your-system>

# SMO OAM development system
<deployment-system-ipv4>                   smo.o-ran-sc.org
<deployment-system-ipv4>           gateway.smo.o-ran-sc.org
<deployment-system-ipv4>          identity.smo.o-ran-sc.org
<deployment-system-ipv4>          messages.smo.o-ran-sc.org
<deployment-system-ipv4> ves-collector.oam.smo.o-ran-sc.org
<deployment-system-ipv4>         odlux.oam.smo.o-ran-sc.org
<deployment-system-ipv4>    controller.oam.smo.o-ran-sc.org

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
    ├── apps
    │   ├── .env
    │   ├── docker-compose.yml
    │   └── flows
    ├── common
    │   ├── .env
    │   ├── docker-compose.yml
    │   │
    │   ├── docker
    │   ├── gateway
    │   ├── identity
    │   ├── messages
    │   ├── kafka
    │   └── zookeeper
    └── oam
        ├── .env
        ├── docker-compose.yml
        │
        ├── odlux
        ├── controller
        └── ves-collector
```

## Usage

### Bring Up Solution

#### Short story

The following commands should be invoked. More detailed can be found in the
next chapters.

```
docker compose -f smo/common/docker-compose.yml up -d
# wait until the cpu load is low again
python smo/common/identity/config.py

docker compose -f smo/oam/docker-compose.yml up -d
docker compose -f smo/apps/docker-compose.yml up -d

# wait until the cpu load is low again

docker compose -f network/docker-compose.yml up -d
# wait about 2min
docker restart ntsim-ng-o-du-1122
python network/config.py
```

#### Check (adjust if required) environment variables

```
nano smo/common/.env
nano smo/oam/.env
nano network/.env
```

#### Startup solution

Please note that it is necessary to configure first the identity service,
before starting further docker images.

The several docker-compose yml files must be started in the right order as listed below:

```
docker compose -f smo/common/docker-compose.yml up -d
python smo/common/identity/config.py
```

The python script configure the users within the identity service (keycloak).
A system user (%USER) is also created with administration rights.


```
docker compose -f smo/oam/docker-compose.yml up -d
```

Looking into the ONAP SDN-R logs will give you the startup procedure.

```
docker logs -f controller
```

If you see the login page (https://odlux.oam.smo.o-ran-sc.org) you are good to go and can start the (simulated) network.

```
docker compose -f network/docker-compose.yml up -d
```

Usually the first ves:event gets lost. Please restart the O-DU docker container(s) to send a second ves:pnfRegistration.

```
docker compose -f network/docker-compose.yml restart ntsim-ng-o-du-1122
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
docker exec -it controller tail -f /opt/opendaylight/data/log/karaf.log
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

    https://odlux.oam.smo.o-ran-sc.org

    User: admin // see .env file

    Password: Kp8bJ4SXszM0WXlhak3eHlcse2gAw84vaoGGmJvUy2U

In case of trouble, please update the commands with your customized '.env' file.

### Terminate solution

To stop all container please respect the following order

```
docker compose -f network/docker-compose.yml down
docker compose -f smo/apps/docker-compose.yml down
docker compose -f smo/oam/docker-compose.yml down
docker compose -f smo/common/docker-compose.yml down
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
docker rm -f $(docker ps -aq)
