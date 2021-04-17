.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. SPDX-License-Identifier: CC-BY-4.0
.. Copyright (C) 2021 highstreet technologies GmbH


Operation and Maintenance Release Notes
=======================================

This document provides the release notes for O-RAN-SC D-Release of the Operation and Maintenance (OAM) project.

.. contents::
   :depth: 3
   :local:

Version 4.0.2, 2021-04-02
--------------------------

+--------------------------------------------------------------------+-------------------------------------------------------------------------+
| Issue                                                              | Summary                                                                 |
+====================================================================+=========================================================================+
| `OAM-180     <https://jira.o-ran-sc.org/browse/OAM-180>`__         | Wrong time format in VES client scripts                                 |
+--------------------------------------------------------------------+-------------------------------------------------------------------------+
| `OAM-176     <https://jira.o-ran-sc.org/browse/OAM-176>`__         | Support of IPv6 by docker-compose                                       |
+--------------------------------------------------------------------+-------------------------------------------------------------------------+
| `OAM-175     <https://jira.o-ran-sc.org/browse/OAM-175>`__         | Update docker-compose and its configurations                            |
+--------------------------------------------------------------------+-------------------------------------------------------------------------+
| `OAM-174     <https://jira.o-ran-sc.org/browse/OAM-174>`__         | Update VES Client scripts supporting VES 7.2                            |
+--------------------------------------------------------------------+-------------------------------------------------------------------------+
| `OAM-173     <https://jira.o-ran-sc.org/browse/OAM-173>`__         | Update VES client scripts supporting https                              |
+--------------------------------------------------------------------+-------------------------------------------------------------------------+
| `OAM-170     <https://jira.o-ran-sc.org/browse/OAM-170>`__         | Delete folder 'model' from OAM repo'                                    |
+--------------------------------------------------------------------+-------------------------------------------------------------------------+
| `OAM-169     <https://jira.o-ran-sc.org/browse/OAM-169>`__         | Use case driven yang for O-DU                                           |
+--------------------------------------------------------------------+-------------------------------------------------------------------------+
| `OAM-168     <https://jira.o-ran-sc.org/browse/OAM-168>`__         | Update namespace definitions in prototype yangs of O-RAN-SC             |
+--------------------------------------------------------------------+-------------------------------------------------------------------------+
| `OAM-164     <https://jira.o-ran-sc.org/browse/OAM-164>`__         | Add WG4 november train yangs modules                                    |
+--------------------------------------------------------------------+-------------------------------------------------------------------------+
| `SDNC-1480   <https://jira.onap.org/browse/SDNC-1480>`__           | O-RAN (FrontHaul) deviceManager: support of GuiCutThrough               |
+--------------------------------------------------------------------+-------------------------------------------------------------------------+
| `CCSDK-3161  <https://jira.onap.org/browse/CCSDK-3161>`__          | O-RAN (FrontHaul) deviceManager: o-ran-fm.yang/alarm-notif to VES:fault |
+--------------------------------------------------------------------+-------------------------------------------------------------------------+
| `CCSDK-3160  <https://jira.onap.org/browse/CCSDK-3160>`__          | CallHome to VES:pnfRegistration                                         |
+--------------------------------------------------------------------+-------------------------------------------------------------------------+
| `NETCONF-766 <https://jira.opendaylight.org/browse/NETCONF-766>`__ | Logging al RESTCONF requests and responses [1]_                         |
+--------------------------------------------------------------------+-------------------------------------------------------------------------+
| `NETCONF-744 <https://jira.opendaylight.org/browse/NETCONF-744>`__ | Read whole leaf-list using get/get-config RPC [1]_                      |
+--------------------------------------------------------------------+-------------------------------------------------------------------------+
| `NETCONF-735 <https://jira.opendaylight.org/browse/NETCONF-735>`__ | Support NETCONF get/get-config with multiple selected subtrees [1]_     |
+--------------------------------------------------------------------+-------------------------------------------------------------------------+

.. [1] Patched via MAVEN repo into CCSDK as long as code is not merged into OpenDaylight master branch


Version 4.0.1, 2021-03-12
--------------------------

+--------------------------------------------------------+-------------------------------------------------------------+
| Issue                                                  | Summary                                                     |
+========================================================+=============================================================+
| `OAM-166 <https://jira.o-ran-sc.org/browse/OAM-166>`__ | Add WG4 July 2020 yang modules                              |
+--------------------------------------------------------+-------------------------------------------------------------+
| `OAM-163 <https://jira.o-ran-sc.org/browse/OAM-163>`__ | Rename yang filename to <module>@<revision> format          |
+--------------------------------------------------------+-------------------------------------------------------------+
| `OAM-160 <https://jira.o-ran-sc.org/browse/OAM-160>`__ | Modeling Repo: SIM directory not longer required            |
+--------------------------------------------------------+-------------------------------------------------------------+
| `OAM-159 <https://jira.o-ran-sc.org/browse/OAM-159>`__ | Remove yang models from Repo                                |
+--------------------------------------------------------+-------------------------------------------------------------+
| `OAM-154 <https://jira.o-ran-sc.org/browse/OAM-154>`__ | OAM tr069: Changing .gitignore for IntelliJ related files   |
+--------------------------------------------------------+-------------------------------------------------------------+
| `OAM-121 <https://jira.o-ran-sc.org/browse/OAM-121>`__ | Request to modify SMO deployment SOP                        |
+--------------------------------------------------------+-------------------------------------------------------------+
| `OAM-120 <https://jira.o-ran-sc.org/browse/OAM-120>`__ | Release dashboard image at version 2.0.3                    |
+--------------------------------------------------------+-------------------------------------------------------------+

Version 2.0.4, 2020-06-13
--------------------------

* Documentation updated
* Develop reusable OAM API such that the first consumer being a VTH can query, subscribe or publish on a DMaaP topic	Story
* Create helm deployment for SMO
* Feature split for starting devicemanagers
* Seed coder for an YANG linter
* Please see also Release Notes of `ONAP SDNC, DCAE, DMaaP, OOM <https://onap-doc.readthedocs.io/en/frankfurt/release/index.html>`_

Version 2.0.3, 2020-04-08
-------------------------

* What is an SMO?
* Provide xRAN datamodels
* Provide curl bash scripts for Software Management
* Add jenkins jobs for oam
* Add parents to model artifacts
* Add top level pom file to distribution
* Wrong image tag in nonrt-o1-controller distribution pom
* Use ONAP release parents directly
* Adjust artifact group name to ORAN naming rule
* Use ORAN parents
* Add push registry to distribution pom

Version 2.0.2, 2020-03-16
-------------------------

* Controller DeviceManager for O-RAN-SC
* Provide O1 yang modules

Version 2.0.1, 2020-02-26
-------------------------

* Develop VTH for A1 interface


Version 1.0.0, 2019-11-14
-------------------------

* Documentation added


Version 0.1.1, 2019-09-18
-------------------------

* Development environment added


Version 0.1.0, 2019-09-08
-------------------------
* Initial version
