.. contents::
   :depth: 3
..

SDN-R Docker Image configuration
================================

Introduction
~~~~~~~~~~~~

ONAP SDN-R is running in a docker container using ONAP/SDN-C image
"onap/sdnc".

The container is available as Alpine and Ubuntu version. The description
uses examples for the Alpine version.

The alpine based sdnc docker imanges are stored in \ `ONAP Nexus sdnc
image <https://nexus3.onap.org:10001/v2/onap/sdnc-image/tags/list>`__.

The docker image contains a Opendaylight distribution in a standard
configuration and ONAP/SDN-R specific microservices.

The Root location of ODL Karaf directory structure
is \ *ODL\_HOME=/opt/opendaylight.*

During container provisioning the installation of the feature is done,
according to the provided configuration setting.

The docker image configuration is done by

-  Specific Environment variables settings

-  Files that are provided

Container startup parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The SDN-R specific configurations are provided during container start. 

Different SDN-R services are using different parameter to be installed.

+------------------+---------------------+-------------------------------------------------------------------------------------------------------------------------+
| **Parameter**    | **Content**         | **Description**                                                                                                         |
+==================+=====================+=========================================================================================================================+
| SDNRWT           | true\|\ **false**   | Set true to activate sdnr wt featureset. Set this during container start.                                               |
|                  |                     |                                                                                                                         |
|                  |                     | Devicemanager configuration is provided via *$ODL\_HOME/etc/devicemanager.properties*                                   |
|                  |                     |                                                                                                                         |
|                  |                     | See  `SDN-R WT Service Configuration parameters <sdnr_WT_Service_Configuration_parameters.html>`__			   |
+------------------+---------------------+-------------------------------------------------------------------------------------------------------------------------+
| SDNRNORTHBOUND   | true\|\ **false**   | Set true to activate sdnr oofpci service.                                                                               |
+------------------+---------------------+-------------------------------------------------------------------------------------------------------------------------+
