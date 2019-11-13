.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. SPDX-License-Identifier: CC-BY-4.0
.. Copyright (C) 2019 highstreet technologies and others

OAM Operation and Maintenance Overview
======================================

The O-RAN SC OAM provides administrative and operator
functions for O-RAN components, such as Near-Realtime-RAN-Inelegent-Controller,
O-RAN Centralized Unit, O-RAN Distributed Unit and O-RAN Radio Unit. 

The project follows the specifications for the O1 interface as provided by
O-RAN Working Group1. 


Project Resources
-----------------

The source code is available from the Linux Foundation Gerrit server:

    `<https://gerrit.o-ran-sc.org/r/admin/repos/oam>`_

The build (CI) jobs are in the Linux Foundation Jenkins server:

    `<https://jenkins.o-ran-sc.org/view/oam/>`_

Issues are tracked in the Linux Foundation Jira server:

    `<https://jira.o-ran-sc.org/projects/OAM/>`_

Project information is available in the Linux Foundation Wiki:

    `<https://wiki.o-ran-sc.org/display/OAM/Operations+and+Maintenance>`_


Scope
-----

According to the O-RAN-SC-OAM-Architecture document all ManagedElements 
(near-real-time-RIC, O-CU-CP, O-CU-UP, O-DU and O-RU) implement the 
O1-interface.

The O-RAN-OAM-interface specification defines

- a NetConf-Server for Configuration Management (CM) and
- a http-client for Fault Managment (FM), Performance Management (PM) and other 
  events on each Management-Service-Provider (MnS-Provider) running on the 
  ManagedElement (ME).

THe O-RAN-SC-OAM project provides reference implementation according to the 
O-RAN OAM (WG1) documents. In addition we provide a common MnS-Consumer for 
development and module test purposes.  The assumption is that the projects 
for the ManagedElements can concentrate on the more important user-plane.

Of cause each project needs its own OAM repo to address the specific needs 
of the ManagedElement.
