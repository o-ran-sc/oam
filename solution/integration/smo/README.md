# Service Management and Orchestration (SMO)

With respect to OAM the SMO implements the O1-interface provider. According to the O-RAN OAM Architecture and the O-RAN OAM Interface Specification, the SMO has a NetConf Client for configuration and HTTP/REST/VES Server for receiving all kind of events in a VES format.

The setup contains an OpenDaylight based NetConf client and a VES Test Collector.

## Overview

This docker-compose file starts a pre-configured, self-contained SDN-R solution for developer test or demo purposes

  * **SDN-R** single node instance

    ... representing the NetConf consumer on the Service Management and Orchstration framework (SMO) for the O1 interface.
    based on ODL-Sodium/ONAP-Guilin

  * **VES collector**

    ... representing the VES (REST) provider at SMO for all kind of events.

  * **DMaaP**
    ... representing SMO DMaaP component, includes message-router

## Prerequisites

docker-compose file version 2.2 is used and tested with

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
cd ~
git clone https://gerrit.o-ran-sc.org:29418/oam.git
cd ~/oam/solution/integration/smo
```

## Usage

### Bring Up Solution

  * Check (adjust if required) environment variables

```
cd ~/oam/solution/integration/smo
nano .env
```

  * startup solution

```
cd ~/oam/solution/integration/smo
docker-compose up -d
```

### Log files and karaf console

  * ODL karaf.logs
```
docker exec -it sdnr  tail -f /opt/opendaylight/data/log/karaf.log
```

  * karaf console access (karaf:karaf)

```
ssh karaf@localhost -p 8101
```

  * vescollector logs

```
   docker logs -f vescollector
```

### Customizing Solution

'.env' file contains customizing parameters


### Verification Solution

#### Access to SDN-R UX

  * login into SDN-R
    http://<host_ip>:8181/odlux/index.html
    User:admin
    Password:Kp8bJ4SXszM0WXlhak3eHlcse2gAw84vaoGGmJvUy2U


### Terminate solution

To stop all container:

```
cd ~/oam/solution/integration/smo
docker-compose down
```

re-start solution at any point in time with
```
cd ~/oam/solution/integration/smo
docker-compose up -d
```


### Cleanup

!!! be careful if other stopped containers are on the same system
```
docker system prune -a -f


```
### Troubleshooting

