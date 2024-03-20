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

### Resources

The solution was tested on a VM with

- 4x Core
- 16 GBit RAM 
- 50 Gbit Storage

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

Please change in the different .env files the environment variable 'HOST_IP'
to the IP address of the system where you deploy the solution - search for 
'aaa.bbb.ccc.ddd' and replace it. 

Please modify the /etc/hosts of your system.

* \<your-system>: is the hostname of the system, where the browser is started

* \<deployment-system-ipv4>: is the IP address of the system where the solution will be deployed

For development purposes <your-system> and <deployment-system> may reference the same system.

```
$ cat /etc/hosts
127.0.0.1	               localhost
127.0.1.1	               10.20.35.165

# SMO OAM development system
<deployment-system-ipv4>                   smo.o-ran-sc.org
<deployment-system-ipv4>           gateway.smo.o-ran-sc.org 
<deployment-system-ipv4>          identity.smo.o-ran-sc.org
<deployment-system-ipv4>          messages.smo.o-ran-sc.org
<deployment-system-ipv4>      kafka-bridge.smo.o-ran-sc.org
<deployment-system-ipv4>         odlux.oam.smo.o-ran-sc.org
<deployment-system-ipv4>         flows.oam.smo.o-ran-sc.org
<deployment-system-ipv4>         tests.oam.smo.o-ran-sc.org
<deployment-system-ipv4>    controller.dcn.smo.o-ran-sc.org
<deployment-system-ipv4> ves-collector.dcn.smo.o-ran-sc.org

```

## Usage

### Bring Up Solution

#### Short story

The following commands should be invoked. More detailed can be found in the
next chapters.

```bash
docker compose -f smo/common/docker-compose.yaml up -d  --wait

# optionally adjust the users.csv file to create new users
vim users.csv
# override authentication.json with the new users
python3 create_users.py users.csv -o smo/common/identity/authentication.json

python smo/common/identity/config.py

docker compose -f smo/oam/docker-compose.yaml up -d
docker compose -f smo/apps/docker-compose.yaml up -d

# wait until the cpu load is low again

docker compose -f network/docker-compose.yaml up -d
docker compose -f network/docker-compose.yaml restart ntsim-ng-o-du-1122 ntsim-ng-o-du-1123
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

The several docker-compose yaml files must be started in the right order as listed below:

```
docker compose -f smo/common/docker-compose.yaml up -d
python smo/common/identity/config.py
```

The python script configure the users within the identity service (keycloak).
A system user (%USER) is also created with administration rights.


```
docker compose -f smo/oam/docker-compose.yaml up -d
```

Looking into the ONAP SDN-R logs will give you the startup procedure.

```
docker logs -f controller
```

If you see the login page (https://odlux.oam.smo.o-ran-sc.org) you are good to go and can start the (simulated) network.

```
docker compose -f network/docker-compose.yaml up -d
```

Usually the first ves:event gets lost. Please restart the O-DU docker container(s) to send a second ves:pnfRegistration.

```
docker compose -f network/docker-compose.yaml restart ntsim-ng-o-du-1122
python network/config.py
```

The python script configures the simulated O-DU and O-RU according to O-RAN hybrid architecture.

O-RU - NETCONF Call HOME and NETCONF notifications
O-DU - ves:pnfRegistration and ves:fault, ves:heartbeat

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

    https://odlux.oam.smo.o-ran-sc.org

    User: admin 

    Password: // see .env file

In case of trouble, please update the commands with your customized '.env' file.

#### Access to Node Red Flows

    https://flows.oam.smo.o-ran-sc.org

    User: admin 

    Password: // see .env file

In case of trouble, please update the commands with your customized '.env' file.

### Terminate solution

To stop all container please respect the following order

```
docker compose -f network/docker-compose.yaml down
docker compose -f smo/apps/docker-compose.yaml down
docker compose -f smo/oam/docker-compose.yaml down
docker compose -f smo/common/docker-compose.yaml down
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

## Commands in action

```
$ docker ps -a --format "table {{.Names}}\t{{.Image}}\t{{.Status}}" 
NAMES     IMAGE     STATUS
$ docker compose -f smo/common/docker-compose.yaml up -d
[+] Running 9/9
 ✔ Network smo            Created                                                                                                                                                                  0.1s 
 ✔ Network dmz            Created                                                                                                                                                                  0.1s 
 ✔ Container zookeeper    Started                                                                                                                                                                  1.6s 
 ✔ Container persistence  Started                                                                                                                                                                  1.5s 
 ✔ Container identitydb   Started                                                                                                                                                                  1.2s 
 ✔ Container gateway      Healthy                                                                                                                                                                 12.1s 
 ✔ Container kafka        Started                                                                                                                                                                  2.2s 
 ✔ Container identity     Started                                                                                                                                                                 13.4s 
 ✔ Container messages     Started                                                                                                                                                                 13.4s 
$ python3 smo/common/identity/config.py 
Got token!
User leia.organa created!
User r2.d2 created!
User luke.skywalker created!
User jargo.fett created!
User role jargo.fett supervision created!
User role leia.organa administration created!
User role luke.skywalker provision created!
User role r2.d2 administration created!
$ docker compose -f smo/oam/docker-compose.yaml up -d
[+] Running 4/4
 ✔ Network oam              Created                                                                                                                                                                0.1s 
 ✔ Container controller     Healthy                                                                                                                                                               83.4s 
 ✔ Container ves-collector  Started                                                                                                                                                                1.2s 
 ✔ Container odlux          Started                                                                                                                                                               84.0s 
$ docker compose -f smo/apps/docker-compose.yaml up -d
WARN[0000] Found orphan containers ([odlux controller ves-collector]) for this project. If you removed or renamed this service in your compose file, you can run this command with the --remove-orphans flag to clean it up. 
[+] Running 1/1
 ✔ Container flows  Started                                                                                                                                                                        0.9s 
$ docker compose -f network/docker-compose.yaml up -d
WARN[0000] Found orphan containers ([flows odlux controller ves-collector]) for this project. If you removed or renamed this service in your compose file, you can run this command with the --remove-orphans flag to clean it up. 
[+] Running 6/6
 ✔ Container ntsim-ng-o-du-1123   Started                                                                                                                                                          2.6s 
 ✔ Container ntsim-ng-o-ru-11223  Started                                                                                                                                                          2.2s 
 ✔ Container ntsim-ng-o-ru-11221  Started                                                                                                                                                          1.9s 
 ✔ Container ntsim-ng-o-ru-11224  Started                                                                                                                                                          1.9s 
 ✔ Container ntsim-ng-o-du-1122   Started                                                                                                                                                          2.4s 
 ✔ Container ntsim-ng-o-ru-11222  Started                                                                                                                                                          2.3s 
$ docker compose -f network/docker-compose.yaml restart ntsim-ng-o-du-1122 ntsim-ng-o-du-1123
[+] Running 2/2
 ✔ Container ntsim-ng-o-du-1122  Started                                                                                                                                                           2.8s 
 ✔ Container ntsim-ng-o-du-1123  Started                                                                                                                                                           2.9s 
$ python3 network/config.py 
Set O-RU-11221 True
Set O-RU-11224 True
Set O-RU-11222 True
Set O-DU-1123 True
Set O-DU-1122 True
Set O-RU-11223 True
$ docker ps -a --format "table {{.Names}}\t{{.Image}}\t{{.Status}}"
NAMES                 IMAGE                                                                                        STATUS
ntsim-ng-o-ru-11221   nexus3.o-ran-sc.org:10004/o-ran-sc/nts-ng-o-ran-ru-fh:1.6.2                                  Up 4 minutes
ntsim-ng-o-ru-11224   nexus3.o-ran-sc.org:10004/o-ran-sc/nts-ng-o-ran-ru-fh:1.6.2                                  Up 4 minutes
ntsim-ng-o-ru-11222   nexus3.o-ran-sc.org:10004/o-ran-sc/nts-ng-o-ran-ru-fh:1.6.2                                  Up 4 minutes
ntsim-ng-o-du-1123    o-ran-sc/nts-ng-o-ran-du-rel-18:1.6.2                                                        Up 54 seconds
ntsim-ng-o-du-1122    nexus3.o-ran-sc.org:10004/o-ran-sc/nts-ng-o-ran-du:1.6.2                                     Up About a minute
ntsim-ng-o-ru-11223   nexus3.o-ran-sc.org:10004/o-ran-sc/nts-ng-o-ran-ru-fh:1.6.2                                  Up 4 minutes
flows                 nodered/node-red:latest-configured                                                           Up 4 minutes (healthy)
odlux                 nexus3.onap.org:10001/onap/sdnc-web-image:2.4.2                                              Up 7 minutes
controller            nexus3.onap.org:10001/onap/sdnc-image:2.4.2                                                  Up 8 minutes (healthy)
ves-collector         nexus3.onap.org:10001/onap/org.onap.dcaegen2.collectors.ves.vescollector:1.10.1-configured   Up 8 minutes (healthy)
messages              nexus3.onap.org:10001/onap/dmaap/dmaap-mr:1.1.18                                             Up 11 minutes
identity              bitnami/keycloak:18.0.2                                                                      Up 11 minutes
kafka                 nexus3.onap.org:10001/onap/dmaap/kafka111:1.0.4                                              Up 11 minutes
zookeeper             nexus3.onap.org:10001/onap/dmaap/zookeeper:6.0.3                                             Up 11 minutes
identitydb            bitnami/postgresql:13                                                                        Up 11 minutes
persistence           docker.elastic.co/elasticsearch/elasticsearch-oss:7.9.3                                      Up 11 minutes
gateway               traefik:v2.9                                                                                 Up 11 minutes (healthy)
$ 
```
