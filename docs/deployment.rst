.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. SPDX-License-Identifier: CC-BY-4.0
.. Copyright (C) 2022 highstreet technologies and others

Deployment
==========

OAM Components are deployed in different context and for different use cases.
Please see the Kubernetes deployment within the `it/deb <https://gerrit.o-ran-sc.org/r/gitweb?p=it/dep>`__ repository and its description in `O-RAN-SC wiki <https://lf-o-ran-sc.atlassian.net/wiki/spaces/IAT/pages/14516593/Automated+deployment+and+testing+-+using+SMO+package+and+ONAP+Python+SDK>`__.

The main OAM Components are:

- OAM-Controller from ONAP SDN-R using OpenDaylight for O1-NETCONF and OpenFronthaul-Management-NETCONF support.
- VES-Collector from ONAP DCAE for processing O1-VES messages.
- Message-router from ONAP DMaaP using Kafka
- Identity service from Keycloak for AAA support.


This page focus on a lightweight deployment using docker-compose on an Ubuntu system for experience with SMO OAM Components and/or development.


Prerequisites
-------------

The following command are used to verify your system and it installed software package.
In general new version then display here should be fine.::

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

The communication between the components bases on domain-names. For a lightweight
deployment on a single laptop or virtual-machine the /etc/hosts file should be
modified as a simple DNS.

Please modify the /etc/hosts of your system.

* \<your-system>: is the hostname of the system, where the browser is started

* \<deployment-system-ipv4>: is the IP address of the system where the solution will be deployed

For development purposes <your-system> and <deployment-system> may reference the same system.::

   $ cat /etc/hosts
   127.0.0.1	               localhost
   127.0.1.1	               <your-system>
   <deployment-system-ipv4>   sdnc-web <your-system>
   <deployment-system-ipv4>   identity <your-system>

Docker Enable IPv6
^^^^^^^^^^^^^^^^^^

The O-RAN Alliance specifications target the support of IPv6.
To support IPv6 by docker the docker configuration must be modified.

Please see:
https://docs.docker.com/engine/daemon/ipv6/

1. Edit /etc/docker/daemon.json, set the ipv6 key to true and the fixed-cidr-v6 key to your IPv6 subnet. In this example we are setting it to 2001:db8:1::/64.

.. code-block:: json

  {
      "dns": ["1.1.1.1"],
      "registry-mirrors": [
          "https://nexus3.o-ran-sc.org:10002",
          "https://nexus3.onap.org:10001"
      ],
      "log-driver": "json-file",
      "log-opts": {
          "max-size": "10m",
          "max-file": "3"
      },
      "ipv6": true,
      "fixed-cidr-v6": "2001:db8:1::/64"
  }

2. Reload the Docker configuration file.

.. code-block:: bash

  $ systemctl reload docker

It is beneficial (but not mandatory) adding the following line add the
end of your ~/.bashrc file. I will suppress warnings when python script
do not verify self signed certificates for HTTPS communication.::

   export PYTHONWARNINGS="ignore:Unverified HTTPS request"

Please ensure that you download and copy the required 3GPP OpenAPIs for VES-stndDefined
message validation into the folder './solution/operation-and-maintenance/smo/oam/ves-collector/externalRepo'.

Please follow the instructions in ./solution/operation-and-maintenance/smo/oam/ves-collector/externalRepo/3gpp/rep/sa5/MnS/blob/Rel16/OpenAPI/README.md.

The following tree shows the successfully tested folder structure. It combines different versions of the schemas ('Rel16' and 'SA88-Rel16') using 3GPP branch names.::

   $ tree solution/operation-and-maintenance/smo/oam/ves-collector/externalRepo/
   solution/operation-and-maintenance/smo/oam/ves-collector/externalRepo/
   ├── 3gpp
   │   └── rep
   │       └── sa5
   │           └── MnS
   │               └── blob
   │                   ├── Rel16
   │                   │   └── OpenAPI
   │                   │       ├── README.md
   │                   │       ├── TS28532_FaultMnS.yaml
   │                   │       ├── TS28532_FileDataReportingMnS.yaml
   │                   │       ├── TS28532_HeartbeatNtf.yaml
   │                   │       ├── TS28532_PerfMnS.yaml
   │                   │       ├── TS28532_ProvMnS.yaml
   │                   │       ├── TS28532_StreamingDataMnS.yaml
   │                   │       ├── TS28536_CoslaNrm.yaml
   │                   │       ├── TS28541_5GcNrm.yaml
   │                   │       ├── TS28541_NrNrm.yaml
   │                   │       ├── TS28541_SliceNrm.yaml
   │                   │       ├── TS28550_PerfMeasJobCtrlMnS.yaml
   │                   │       ├── TS28623_ComDefs.yaml
   │                   │       ├── TS28623_GenericNrm.yaml
   │                   │       ├── TS29512_Npcf_SMPolicyControl.yaml
   │                   │       ├── TS29514_Npcf_PolicyAuthorization.yaml
   │                   │       └── TS29571_CommonData.yaml
   │                   └── SA88-Rel16
   │                       └── OpenAPI
   │                           ├── 5gcNrm.yaml
   │                           ├── PerDataFileReportMnS.yaml
   │                           ├── PerMeasJobCtlMnS.yaml
   │                           ├── PerThresMonMnS.yaml
   │                           ├── PerfDataStreamingMnS.yaml
   │                           ├── README.md
   │                           ├── comDefs.yaml
   │                           ├── coslaNrm.yaml
   │                           ├── faultMnS.yaml
   │                           ├── genericNrm.yaml
   │                           ├── heartbeatNtf.yaml
   │                           ├── nrNrm.yaml
   │                           ├── provMnS.yaml
   │                           ├── sliceNrm.yaml
   │                           └── streamingDataMnS.yaml

Expected Folder Structure
-------------------------

The following figure show the expected folder structure for the different
docker-compose file and its configurations.::

   ├── network
   │   ├── .env
   │   ├── config.py
   │   ├── docker-compose.yaml
   │   │
   │   ├── ntsim-ng-o-du
   │   └── ntsim-ng-o-ru
   └── smo
      ├── common
      │   ├── .env
      │   ├── docker-compose.yaml
      │   │
      │   ├── dmaap
      │   ├── docker
      │   ├── identity
      │   ├── kafka
      │   └── zookeeper
      └── oam
         ├── .env
         ├── docker-compose.yaml
         │
         ├── web
         ├── controller
         └── ves-collector

Usage
-----

Bring Up Solution
^^^^^^^^^^^^^^^^^

Please check and adjust, if required the environment variables::

   nano smo/common/.env
   nano smo/oam/.env
   nano network/.env

The tested configuration uses the following external https ports:

* 8443 for the ves-collector
* 8453 for web access to ODLUX (SDNC_WEB_PORT)
* 8463 for the keyclock web administrator user interface.

Please note that it is necessary to configure first the identity service,
before starting further docker images.

The several docker-compose yaml files must be started in the right order as listed below:

First the SMO common services must be started::

   docker-compose -f smo/common/docker-compose.yaml up -d
   python smo/common/identity/config.py

The python script configure the users within the identity service (keycloak).
A system user (%USER) is also created with administration rights. The initial password (Default4SDN!).
The identity service implemented by Keycloak is configured in a way that the user must change its initial password after the first successful login.

In a second step the OAM specific service can be started: ::

   docker-compose -f smo/oam/docker-compose.yaml up -d

Looking into the ONAP SDN-R logs will give you the startup procedure.::

   docker logs -f sdnr

The startup was successful when you see the following line: ::

   Everything OK in Certificate Installation


If you see the login page (https://sdnc-web:8453) you are good to go and can start the (simulated) network.::

   docker-compose -f network/docker-compose.yaml up -d


Usually the first ves:event gets lost. Please restart the O-DU docker container(s) to send a second ves:pnfRegistration.::

   docker-compose -f network/docker-compose.yaml restart ntsim-ng-o-du-1122
   python network/config.py


The python script configures the simulated O-DU and O-RU according to O-RAN hybrid architecture.

O-DU - NETCONF Call HOME and NETCONF notifications
O-RU - ves:pnfRegistration and ves:fault, ves:heartbeat

'True' indicated that the settings through SDN-R to the NETCONF server were
successful.

SDN-R reads the fault events from DMaaP and processes them.
Finally the fault events are visible in ODLUX.


Log files and karaf console
^^^^^^^^^^^^^^^^^^^^^^^^^^^

OpenDaylight/Apache Karaf logs::

   docker exec -it sdnr tail -f /opt/opendaylight/data/log/karaf.log

VES-collector logs::

   docker logs -f ves-collector


Verification of Solution
^^^^^^^^^^^^^^^^^^^^^^^^

On the web user interface https://sdnc-web:8453 you can login with the system user ($USER) and the default password mentioned above.
You should see 4 network function connected via IPv6 and also alarm notification via NETCONF and VES.


Terminate solution
^^^^^^^^^^^^^^^^^^

To stop all container please respect the following order::

   docker-compose -f network/docker-compose.yaml down
   docker-compose -f smo/oam/docker-compose.yaml down
   docker-compose -f smo/common/docker-compose.yaml down

Cleanup
^^^^^^^

Please be very careful with the following command, if other stopped containers are on the same system::

   docker system prune -a -f
