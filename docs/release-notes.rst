.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. SPDX-License-Identifier: CC-BY-4.0
.. Copyright (C) 2025 highstreet technologies USA Corp.


Operation and Maintenance Release Notes
=======================================

This document provides the release notes for O-RAN-SC M-Release of the Operation and Maintenance (OAM) project.

M-Release, 2025-12-01
---------------------

+----------------------------------------------------------------+--------------------------------------------------------------------------+
| ID                                                             | Description                                                              |
+================================================================+==========================================================================+
| `OAM-452 <https://lf-o-ran-sc.atlassian.net/browse/OAM-452>`__ | M-Release                                                                |
+----------------------------------------------------------------+--------------------------------------------------------------------------+
| `OAM-457 <https://lf-o-ran-sc.atlassian.net/browse/OAM-457>`__ | Create oam/oam-controller repository.                                    |
+----------------------------------------------------------------+--------------------------------------------------------------------------+
| `OAM-459 <https://lf-o-ran-sc.atlassian.net/browse/OAM-459>`__ | clean up requirements.txt in root dir                                    |
+----------------------------------------------------------------+--------------------------------------------------------------------------+
| `OAM-460 <https://lf-o-ran-sc.atlassian.net/browse/OAM-460>`__ | Provide intial controller                                                |
+----------------------------------------------------------------+--------------------------------------------------------------------------+
| `OAM-461 <https://lf-o-ran-sc.atlassian.net/browse/OAM-461>`__ | Provide parents for oam-controller                                       |
+----------------------------------------------------------------+--------------------------------------------------------------------------+
| `OAM-462 <https://lf-o-ran-sc.atlassian.net/browse/OAM-462>`__ | Cleanup parents for oam-controller                                       |
+----------------------------------------------------------------+--------------------------------------------------------------------------+
| `OAM-465 <https://lf-o-ran-sc.atlassian.net/browse/OAM-465>`__ | Insufficient permissions to write to github packages                     |
+----------------------------------------------------------------+--------------------------------------------------------------------------+
| `OAM-467 <https://lf-o-ran-sc.atlassian.net/browse/OAM-467>`__ | Optimize dependencies bom in parents                                     |
+----------------------------------------------------------------+--------------------------------------------------------------------------+
| `OAM-468 <https://lf-o-ran-sc.atlassian.net/browse/OAM-468>`__ | Provide ru-fh devicemanager and odlux                                    |
+----------------------------------------------------------------+--------------------------------------------------------------------------+
| `OAM-469 <https://lf-o-ran-sc.atlassian.net/browse/OAM-469>`__ | provide oam-controller distribution to create sdnc and sdnc-web images   |
+----------------------------------------------------------------+--------------------------------------------------------------------------+
| `OAM-471 <https://lf-o-ran-sc.atlassian.net/browse/OAM-471>`__ | Solution gateway encode query ; to &                                     |
+----------------------------------------------------------------+--------------------------------------------------------------------------+
| `OAM-472 <https://lf-o-ran-sc.atlassian.net/browse/OAM-472>`__ | Include GHA workflow for building artifacts                              |
+----------------------------------------------------------------+--------------------------------------------------------------------------+
| `OAM-473 <https://lf-o-ran-sc.atlassian.net/browse/OAM-473>`__ | Update github workflows                                                  |
+----------------------------------------------------------------+--------------------------------------------------------------------------+
| `OAM-474 <https://lf-o-ran-sc.atlassian.net/browse/OAM-474>`__ | update gerrit-verify.yml                                                 |
+----------------------------------------------------------------+--------------------------------------------------------------------------+
| `OAM-475 <https://lf-o-ran-sc.atlassian.net/browse/OAM-475>`__ | Include parent pom.xml                                                   |
+----------------------------------------------------------------+--------------------------------------------------------------------------+
| `OAM-476 <https://lf-o-ran-sc.atlassian.net/browse/OAM-476>`__ | Override global settings with project specific settings.xml              |
+----------------------------------------------------------------+--------------------------------------------------------------------------+
| `OAM-477 <https://lf-o-ran-sc.atlassian.net/browse/OAM-477>`__ | Use new github action                                                    |
+----------------------------------------------------------------+--------------------------------------------------------------------------+
| `OAM-478 <https://lf-o-ran-sc.atlassian.net/browse/OAM-478>`__ | Fix github workflows                                                     |
+----------------------------------------------------------------+--------------------------------------------------------------------------+
| `OAM-479 <https://lf-o-ran-sc.atlassian.net/browse/OAM-479>`__ | Add gerrit-merge.yml                                                     |
+----------------------------------------------------------------+--------------------------------------------------------------------------+
| `OAM-480 <https://lf-o-ran-sc.atlassian.net/browse/OAM-480>`__ | Test Commit                                                              |
+----------------------------------------------------------------+--------------------------------------------------------------------------+
| `OAM-481 <https://lf-o-ran-sc.atlassian.net/browse/OAM-481>`__ | Test commit for verifying uploading of artifacts                         |
+----------------------------------------------------------------+--------------------------------------------------------------------------+
| `OAM-482 <https://lf-o-ran-sc.atlassian.net/browse/OAM-482>`__ | Test commit for verifying uploading of artifacts                         |
+----------------------------------------------------------------+--------------------------------------------------------------------------+
| `OAM-483 <https://lf-o-ran-sc.atlassian.net/browse/OAM-483>`__ | Test commit for gerrit merge testing                                     |
+----------------------------------------------------------------+--------------------------------------------------------------------------+
| `OAM-484 <https://lf-o-ran-sc.atlassian.net/browse/OAM-484>`__ | Create CVE tag example                                                   |
+----------------------------------------------------------------+--------------------------------------------------------------------------+
| `OAM-485 <https://lf-o-ran-sc.atlassian.net/browse/OAM-485>`__ | Network generation support of 1.n O-DU:O-RU                              |
+----------------------------------------------------------------+--------------------------------------------------------------------------+
| `OAM-486 <https://lf-o-ran-sc.atlassian.net/browse/OAM-486>`__ | push artifacts to nexus and nexus3                                       |
+----------------------------------------------------------------+--------------------------------------------------------------------------+
| `OAM-487 <https://lf-o-ran-sc.atlassian.net/browse/OAM-487>`__ | Remove unwanted Github workflows                                         |
+----------------------------------------------------------------+--------------------------------------------------------------------------+
| `OAM-488 <https://lf-o-ran-sc.atlassian.net/browse/OAM-488>`__ | Uncomment mandatory gerrit inputs                                        |
+----------------------------------------------------------------+--------------------------------------------------------------------------+
| `OAM-489 <https://lf-o-ran-sc.atlassian.net/browse/OAM-489>`__ | Rename gerrit-merge.yaml to check if it gets triggered                   |
+----------------------------------------------------------------+--------------------------------------------------------------------------+
| `OAM-490 <https://lf-o-ran-sc.atlassian.net/browse/OAM-490>`__ | Remove unavailable GERRIT inputs                                         |
+----------------------------------------------------------------+--------------------------------------------------------------------------+
| `OAM-491 <https://lf-o-ran-sc.atlassian.net/browse/OAM-491>`__ | Test commit for verifying gerrit merge workflow trigger                  |
+----------------------------------------------------------------+--------------------------------------------------------------------------+
| `OAM-492 <https://lf-o-ran-sc.atlassian.net/browse/OAM-492>`__ | Include new jobs in gerrit merge workflow                                |
+----------------------------------------------------------------+--------------------------------------------------------------------------+
| `OAM-494 <https://lf-o-ran-sc.atlassian.net/browse/OAM-494>`__ | Revert stripped GERRIT inputs for gerrit-merge to work                   |
+----------------------------------------------------------------+--------------------------------------------------------------------------+
| `OAM-495 <https://lf-o-ran-sc.atlassian.net/browse/OAM-495>`__ | Pass nexus secrets to github action                                      |
+----------------------------------------------------------------+--------------------------------------------------------------------------+
| `OAM-496 <https://lf-o-ran-sc.atlassian.net/browse/OAM-496>`__ | Dummy commit to trigger GHA merge                                        |
+----------------------------------------------------------------+--------------------------------------------------------------------------+
| `OAM-497 <https://lf-o-ran-sc.atlassian.net/browse/OAM-497>`__ | Prerequisites improvement for SMO deployment                             |
+----------------------------------------------------------------+--------------------------------------------------------------------------+
| `OAM-498 <https://lf-o-ran-sc.atlassian.net/browse/OAM-498>`__ | Update groupId to use oam-oam-controller instead of oam-controller       |
+----------------------------------------------------------------+--------------------------------------------------------------------------+
| `OAM-499 <https://lf-o-ran-sc.atlassian.net/browse/OAM-499>`__ | invalid groupId in oam-controller artifact                               |
+----------------------------------------------------------------+--------------------------------------------------------------------------+
| `OAM-500 <https://lf-o-ran-sc.atlassian.net/browse/OAM-500>`__ | update docker image path to include repo name                            |
+----------------------------------------------------------------+--------------------------------------------------------------------------+
| `OAM-501 <https://lf-o-ran-sc.atlassian.net/browse/OAM-501>`__ | update serverId in settings.xml                                          |
+----------------------------------------------------------------+--------------------------------------------------------------------------+
| `OAM-502 <https://lf-o-ran-sc.atlassian.net/browse/OAM-502>`__ | sdnc-web missing from deploy                                             |
+----------------------------------------------------------------+--------------------------------------------------------------------------+
| `OAM-503 <https://lf-o-ran-sc.atlassian.net/browse/OAM-503>`__ | Update workflows and versions                                            |
+----------------------------------------------------------------+--------------------------------------------------------------------------+
| `OAM-505 <https://lf-o-ran-sc.atlassian.net/browse/OAM-505>`__ | Test commit to trigger GHA workflows to push artifacts to nexus repos    |
+----------------------------------------------------------------+--------------------------------------------------------------------------+
| `OAM-506 <https://lf-o-ran-sc.atlassian.net/browse/OAM-506>`__ | Create release file for 13.0.0 version                                   |
+----------------------------------------------------------------+--------------------------------------------------------------------------+
| `OAM-509 <https://lf-o-ran-sc.atlassian.net/browse/OAM-509>`__ | sdnr container fails to start when oauth is enabled                      |
+----------------------------------------------------------------+--------------------------------------------------------------------------+
| `OAM-510 <https://lf-o-ran-sc.atlassian.net/browse/OAM-510>`__ | Build failure during creation of sdnc-web docker image                   |
+----------------------------------------------------------------+--------------------------------------------------------------------------+
| `OAM-511 <https://lf-o-ran-sc.atlassian.net/browse/OAM-511>`__ | GHA workflow - gerrit-verify.yaml - not voting on successful completion  |
+----------------------------------------------------------------+--------------------------------------------------------------------------+
| `OAM-512 <https://lf-o-ran-sc.atlassian.net/browse/OAM-512>`__ | github workflow (merge) commenting incorrectly when workflow fails       |
+----------------------------------------------------------------+--------------------------------------------------------------------------+
| `OAM-513 <https://lf-o-ran-sc.atlassian.net/browse/OAM-513>`__ | Incorporate CICD for deploy and test                                     |
+----------------------------------------------------------------+--------------------------------------------------------------------------+
| `OAM-514 <https://lf-o-ran-sc.atlassian.net/browse/OAM-514>`__ | Dummy commit to trigger GHA verify                                       |
+----------------------------------------------------------------+--------------------------------------------------------------------------+
| `OAM-515 <https://lf-o-ran-sc.atlassian.net/browse/OAM-515>`__ | fix broken gerrit-verify                                                 |
+----------------------------------------------------------------+--------------------------------------------------------------------------+
| `OAM-516 <https://lf-o-ran-sc.atlassian.net/browse/OAM-516>`__ | Dummy commit to trigger GHA verify                                       |
+----------------------------------------------------------------+--------------------------------------------------------------------------+
| `OAM-517 <https://lf-o-ran-sc.atlassian.net/browse/OAM-517>`__ | Save docker artifacts for use by CICD                                    |
+----------------------------------------------------------------+--------------------------------------------------------------------------+
| `OAM-518 <https://lf-o-ran-sc.atlassian.net/browse/OAM-518>`__ | Comma used instead of space in docker artifact list                      |
+----------------------------------------------------------------+--------------------------------------------------------------------------+
| `OAM-519 <https://lf-o-ran-sc.atlassian.net/browse/OAM-519>`__ | Workflow: Create new job for running tests                               |
+----------------------------------------------------------------+--------------------------------------------------------------------------+
| `OAM-520 <https://lf-o-ran-sc.atlassian.net/browse/OAM-520>`__ | Invalid repo name passed to github action checkout                       |
+----------------------------------------------------------------+--------------------------------------------------------------------------+
| `OAM-521 <https://lf-o-ran-sc.atlassian.net/browse/OAM-521>`__ | pydantic module missing in environment to run tests                      |
+----------------------------------------------------------------+--------------------------------------------------------------------------+
| `OAM-522 <https://lf-o-ran-sc.atlassian.net/browse/OAM-522>`__ | Fix IP Addresses of simulated devices                                    |
+----------------------------------------------------------------+--------------------------------------------------------------------------+
| `OAM-523 <https://lf-o-ran-sc.atlassian.net/browse/OAM-523>`__ | Mounting a device via VES PNF Registration is not working                |
+----------------------------------------------------------------+--------------------------------------------------------------------------+
| `OAM-524 <https://lf-o-ran-sc.atlassian.net/browse/OAM-524>`__ | Align gerrit-verify.yaml to use LF repos                                 |
+----------------------------------------------------------------+--------------------------------------------------------------------------+
| `OAM-525 <https://lf-o-ran-sc.atlassian.net/browse/OAM-525>`__ | Upgrade gerrit merge workflow to use 1password service                   |
+----------------------------------------------------------------+--------------------------------------------------------------------------+
| `OAM-526 <https://lf-o-ran-sc.atlassian.net/browse/OAM-526>`__ | Support non-default ODL ADMIN PASSWORD                                   |
+----------------------------------------------------------------+--------------------------------------------------------------------------+
| `OAM-527 <https://lf-o-ran-sc.atlassian.net/browse/OAM-527>`__ | Incomplete aaa fix                                                       |
+----------------------------------------------------------------+--------------------------------------------------------------------------+
| `OAM-528 <https://lf-o-ran-sc.atlassian.net/browse/OAM-528>`__ | Adapt ODLUX to changed netconf-topology yang for add mountpoint          |
+----------------------------------------------------------------+--------------------------------------------------------------------------+
| `OAM-529 <https://lf-o-ran-sc.atlassian.net/browse/OAM-529>`__ | update gerrit-merge workflow to replace a deprecated action              |
+----------------------------------------------------------------+--------------------------------------------------------------------------+
| `OAM-530 <https://lf-o-ran-sc.atlassian.net/browse/OAM-530>`__ | Support latest yang revision of o-ran-hardware yang model                |
+----------------------------------------------------------------+--------------------------------------------------------------------------+
| `OAM-531 <https://lf-o-ran-sc.atlassian.net/browse/OAM-531>`__ | Create M Release artifacts and images                                    |
+----------------------------------------------------------------+--------------------------------------------------------------------------+
| `OAM-532 <https://lf-o-ran-sc.atlassian.net/browse/OAM-532>`__ | Incorrect or missing release tag                                         |
+----------------------------------------------------------------+--------------------------------------------------------------------------+
| `OAM-533 <https://lf-o-ran-sc.atlassian.net/browse/OAM-533>`__ | Create minor version for M Release                                       |
+----------------------------------------------------------------+--------------------------------------------------------------------------+
| `OAM-534 <https://lf-o-ran-sc.atlassian.net/browse/OAM-534>`__ | Modify M-Release images to OAM Solution                                  |
+----------------------------------------------------------------+--------------------------------------------------------------------------+
| `OAM-536 <https://lf-o-ran-sc.atlassian.net/browse/OAM-536>`__ | Update Release Notes                                                     |
+----------------------------------------------------------------+--------------------------------------------------------------------------+

Please see related release notes in `O-RAN-SC OAM <https://lf-o-ran-sc.atlassian.net/wiki/spaces/OAM/pages/674070651/M-Release+-+Release+Notes>`__ 
and `OpenDaylight <https://docs.opendaylight.org/en/stable-scandium/release-notes/>`__ .


L-Release, 2025-06-10
---------------------

+-----------------------------------------------------------------+---------------------------------------------------------------------------------------------+
| Issue                                                           | Summary                                                                                     |
+=================================================================+=============================================================================================+
| `OAM-464  <https://lf-o-ran-sc.atlassian.net/browse/OAM-464>`__ | Update release notes for L-Release in documentation                                         |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------------------+
| `OAM-458  <https://lf-o-ran-sc.atlassian.net/browse/OAM-458>`__ | Remove DMaaP from the solution                                                              |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------------------+
| `OAM-456  <https://lf-o-ran-sc.atlassian.net/browse/OAM-456>`__ | Roles in keycloak client - causing SDNR Oauth authentication to fail                        |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------------------+
| `OAM-455  <https://lf-o-ran-sc.atlassian.net/browse/OAM-455>`__ | Provision grafana resources automatically during grafana startup                            |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------------------+
| `OAM-454  <https://lf-o-ran-sc.atlassian.net/browse/OAM-454>`__ | Accessing /apidoc in SDNR fails with 401 Unauthorized error                                 |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------------------+
| `OAM-453  <https://lf-o-ran-sc.atlassian.net/browse/OAM-453>`__ | Use grafana for dashboards and integrate with keycloak for authentication and authorization |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------------------+
| `OAM-451  <https://lf-o-ran-sc.atlassian.net/browse/OAM-451>`__ | kafka-ui logout not working                                                                 |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------------------+
| `OAM-450  <https://lf-o-ran-sc.atlassian.net/browse/OAM-450>`__ | kafka-ui should use keycloak for authentication                                             |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------------------+
| `OAM-449  <https://lf-o-ran-sc.atlassian.net/browse/OAM-449>`__ | Upgrade identity server (keycloak) to a recent stable version                               |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------------------+
| `OAM-448  <https://lf-o-ran-sc.atlassian.net/browse/OAM-448>`__ | Fix docs build process                                                                      |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------------------+
| `OAM-447  <https://lf-o-ran-sc.atlassian.net/browse/OAM-447>`__ | Align Cell generation in ietf-topo with geo.json                                            |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------------------+
| `OAM-446  <https://lf-o-ran-sc.atlassian.net/browse/OAM-446>`__ | Clean-up Docker-Compose Network                                                             |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------------------+
| `OAM-445  <https://lf-o-ran-sc.atlassian.net/browse/OAM-445>`__ | Update docker images of Kafka and Zookeeper services                                        |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------------------+
| `OAM-444  <https://lf-o-ran-sc.atlassian.net/browse/OAM-444>`__ | Generate GeoJSON for topology                                                               |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------------------+
| `OAM-443  <https://lf-o-ran-sc.atlassian.net/browse/OAM-443>`__ | Allow creation of several instances.                                                        |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------------------+
| `OAM-442  <https://lf-o-ran-sc.atlassian.net/browse/OAM-442>`__ | Add a disabledREsourcesProfile to the configuration schema and configurations.              |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------------------+
| `OAM-441  <https://lf-o-ran-sc.atlassian.net/browse/OAM-441>`__ | Modify the o-ran-sc topology augmentation                                                   |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------------------+
| `OAM-440  <https://lf-o-ran-sc.atlassian.net/browse/OAM-440>`__ | Make topo-generation more flexible                                                          |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------------------+
| `OAM-439  <https://lf-o-ran-sc.atlassian.net/browse/OAM-439>`__ | fix ves stndDefined schema references according to VES-image-configured                     |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------------------+
| `OAM-438  <https://lf-o-ran-sc.atlassian.net/browse/OAM-438>`__ | Hide "CoreModel" columns in ODLUX                                                           |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------------------+
| `OAM-437  <https://lf-o-ran-sc.atlassian.net/browse/OAM-437>`__ | Use project docker images                                                                   |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------------------+
| `OAM-436  <https://lf-o-ran-sc.atlassian.net/browse/OAM-436>`__ |  Create topics on kafka with solution                                                       |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------------------+
| `OAM-435  <https://lf-o-ran-sc.atlassian.net/browse/OAM-435>`__ |  Inject RANPM function into solution                                                        |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------------------+
| `OAM-434  <https://lf-o-ran-sc.atlassian.net/browse/OAM-434>`__ |  Remove DMaaP from solution                                                                 |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------------------+
| `OAM-433  <https://lf-o-ran-sc.atlassian.net/browse/OAM-433>`__ |  Fix About issue in ODLUX                                                                   |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------------------+
| `OAM-431  <https://lf-o-ran-sc.atlassian.net/browse/OAM-431>`__ |  Integrate PM flow into docker-compose solution                                             |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------------------+
| `OAM-430  <https://lf-o-ran-sc.atlassian.net/browse/OAM-430>`__ |  Update docs for solution deployment                                                        |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------------------+
| `OAM-428  <https://lf-o-ran-sc.atlassian.net/browse/OAM-428>`__ |  Clean-up solution                                                                          |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------------------+
| `OAM-422  <https://lf-o-ran-sc.atlassian.net/browse/OAM-422>`__ |  Solution: add new parameter to controller                                                  |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------------------+
| `OAM-404  <https://lf-o-ran-sc.atlassian.net/browse/OAM-404>`__ |  Generate day0 configuration for deployment of the topology.                                |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------------------+

Please see related release notes in `O-RAN-SC OAM <https://lf-o-ran-sc.atlassian.net/wiki/spaces/OAM/pages/451248134/L-Release+-+Release+Notes>`__ , `ONAP SDNC <https://docs.onap.org/en/latest/release/index.html>`__
and `OpenDaylight <https://docs.opendaylight.org/en/stable-potassium/release-notes/>`__ .


K-Release, 2024-12-28
---------------------

+-----------------------------------------------------------------+------------------------------------------------------------+
| Issue                                                           | Summary                                                    |
+=================================================================+============================================================+
| `OAM-425  <https://lf-o-ran-sc.atlassian.net/browse/OAM-425>`__ | Analyse what needs to happen                               |
+-----------------------------------------------------------------+------------------------------------------------------------+
| `OAM-424  <https://lf-o-ran-sc.atlassian.net/browse/OAM-424>`__ | Add karaf-ui to smo/common                                 |
+-----------------------------------------------------------------+------------------------------------------------------------+
| `OAM-423  <https://lf-o-ran-sc.atlassian.net/browse/OAM-423>`__ | Create Deployment Guideline for INT                        |
+-----------------------------------------------------------------+------------------------------------------------------------+
| `OAM-418  <https://lf-o-ran-sc.atlassian.net/browse/OAM-418>`__ | Integrate an NRCellDU into the topology                    |
+-----------------------------------------------------------------+------------------------------------------------------------+
| `OAM-417  <https://lf-o-ran-sc.atlassian.net/browse/OAM-417>`__ | Topo: Add supported-tps to logical TPs                     |
+-----------------------------------------------------------------+------------------------------------------------------------+
| `OAM-413  <https://lf-o-ran-sc.atlassian.net/browse/OAM-413>`__ | Add O-RAN-SC specific extensions to ietf-network- topology |
+-----------------------------------------------------------------+------------------------------------------------------------+
| `OAM-412  <https://lf-o-ran-sc.atlassian.net/browse/OAM-412>`__ | Rename topology in schema and config to SDO ref            |
+-----------------------------------------------------------------+------------------------------------------------------------+

Please see related release notes in `O-RAN-SC OAM <https://lf-o-ran-sc.atlassian.net/wiki/spaces/OAM/pages/241467395/K-Release+-+Release+Notes>`__ , `ONAP SDNC <https://docs.onap.org/projects/onap-sdnc-oam/en/montreal/release-notes.html>`__
and `OpenDaylight <https://docs.opendaylight.org/en/stable-potassium/release-notes/>`__ .


J-Release, 2024-06-28
---------------------

+-----------------------------------------------------------------+---------------------------------------------------------------------+
| Issue                                                           | Summary                                                             |
+=================================================================+=====================================================================+
| `OAM-408  <https://lf-o-ran-sc.atlassian.net/browse/OAM-408>`__ | Add to_directory method to relevant object classes                  |
+-----------------------------------------------------------------+---------------------------------------------------------------------+
| `OAM-407  <https://lf-o-ran-sc.atlassian.net/browse/OAM-407>`__ | typing-extensions to python requirements                            |
+-----------------------------------------------------------------+---------------------------------------------------------------------+
| `OAM-406  <https://lf-o-ran-sc.atlassian.net/browse/OAM-406>`__ | Add "network_dir" option in config file                             |
+-----------------------------------------------------------------+---------------------------------------------------------------------+
| `OAM-405  <https://lf-o-ran-sc.atlassian.net/browse/OAM-405>`__ | Create python environment for oam                                   |
+-----------------------------------------------------------------+---------------------------------------------------------------------+
| `OAM-402  <https://lf-o-ran-sc.atlassian.net/browse/OAM-402>`__ | Solution: ves-collector support different paths for schemaReference |
+-----------------------------------------------------------------+---------------------------------------------------------------------+
| `OAM-401  <https://lf-o-ran-sc.atlassian.net/browse/OAM-401>`__ | Make oAuth configurable                                             |
+-----------------------------------------------------------------+---------------------------------------------------------------------+
| `OAM-399  <https://lf-o-ran-sc.atlassian.net/browse/OAM-399>`__ | Solution: provide env SDNC_ENABLE_OAUTH for controller and web      |
+-----------------------------------------------------------------+---------------------------------------------------------------------+

Please see related release notes in `O-RAN-SC OAM <https://lf-o-ran-sc.atlassian.net/wiki/spaces/OAM/pages/241500162/Release+Notes>`__ , `ONAP SDNC <https://docs.onap.org/projects/onap-sdnc-oam/en/london/release-notes.html>`__
and `OpenDaylight <https://docs.opendaylight.org/en/stable-calcium/release-notes/>`__ .



Version 6.0.0, 2022-06-28
-------------------------

+-----------------------------------------------------------------+---------------------------------------------------------------------------------+
| Issue                                                           | Summary                                                                         |
+=================================================================+=================================================================================+
| `OAM-271  <https://lf-o-ran-sc.atlassian.net/browse/OAM-271>`__ | Deployment: sdnc-web is not coming up                                           |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------+
| `OAM-270  <https://lf-o-ran-sc.atlassian.net/browse/OAM-270>`__ | O-DUs must not be affected by a disaster for June 2022                          |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------+
| `OAM-269  <https://lf-o-ran-sc.atlassian.net/browse/OAM-269>`__ | Correct E2 protocol                                                             |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------+
| `OAM-268  <https://lf-o-ran-sc.atlassian.net/browse/OAM-268>`__ | create topologies for 2022-06 OTIC PoCfest                                      |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------+
| `OAM-266  <https://lf-o-ran-sc.atlassian.net/browse/OAM-266>`__ | Create additional information model for topology                                |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------+
| `OAM-265  <https://lf-o-ran-sc.atlassian.net/browse/OAM-265>`__ | Deployment: jenkins pod not coming up, missing pv                               |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------+
| `OAM-264  <https://lf-o-ran-sc.atlassian.net/browse/OAM-264>`__ | Deployment:  Minor corrections in README.md                                     |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------+
| `OAM-263  <https://lf-o-ran-sc.atlassian.net/browse/OAM-263>`__ | Create more VES stndDefined Examples                                            |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------+
| `OAM-262  <https://lf-o-ran-sc.atlassian.net/browse/OAM-262>`__ | Define Wireshark configuration                                                  |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------+
| `OAM-261  <https://lf-o-ran-sc.atlassian.net/browse/OAM-261>`__ | Update README to document new Wireshark function                                |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------+
| `OAM-260  <https://lf-o-ran-sc.atlassian.net/browse/OAM-260>`__ | Add Wireshark to docker-compose                                                 |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------+
| `OAM-259  <https://lf-o-ran-sc.atlassian.net/browse/OAM-259>`__ | Add Wireshark to the solution                                                   |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------+
| `OAM-258  <https://lf-o-ran-sc.atlassian.net/browse/OAM-258>`__ | Ues json file names as expected by o-ran-sc-topology service                    |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------+
| `OAM-257  <https://lf-o-ran-sc.atlassian.net/browse/OAM-257>`__ | Use inline css styles for SVG                                                   |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------+
| `OAM-256  <https://lf-o-ran-sc.atlassian.net/browse/OAM-256>`__ | ADD N1, N2 N3 interfacing to topology generation                                |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------+
| `OAM-255  <https://lf-o-ran-sc.atlassian.net/browse/OAM-255>`__ | Add nodes, function and protocols for N1, N2 and N3 interfacing                 |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------+
| `OAM-254  <https://lf-o-ran-sc.atlassian.net/browse/OAM-254>`__ | Create topology-parser tool                                                     |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------+
| `OAM-253  <https://lf-o-ran-sc.atlassian.net/browse/OAM-253>`__ | remove dependency to unused tile-server                                         |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------+
| `OAM-252  <https://lf-o-ran-sc.atlassian.net/browse/OAM-252>`__ | Update nexus port to 10001 for VES Collector images as it is now released.      |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------+
| `OAM-251  <https://lf-o-ran-sc.atlassian.net/browse/OAM-251>`__ | Align docker-compose with SIM topology-service                                  |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------+
| `OAM-250  <https://lf-o-ran-sc.atlassian.net/browse/OAM-250>`__ | Add LayerProtocolQualifier                                                      |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------+
| `OAM-249  <https://lf-o-ran-sc.atlassian.net/browse/OAM-249>`__ | Create a script to generate a Topology                                          |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------+
| `OAM-248  <https://lf-o-ran-sc.atlassian.net/browse/OAM-248>`__ | Create O-RAN-SC extension to TAPI Topology v2.1.3                               |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------+
| `OAM-247  <https://lf-o-ran-sc.atlassian.net/browse/OAM-247>`__ | Remove highstreet from simulated Network Functions names                        |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------+
| `OAM-246  <https://lf-o-ran-sc.atlassian.net/browse/OAM-246>`__ | Modify docker-compose configuration                                             |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------+
| `OAM-245  <https://lf-o-ran-sc.atlassian.net/browse/OAM-245>`__ | Correct pm-streaming model                                                      |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------+
| `OAM-244  <https://lf-o-ran-sc.atlassian.net/browse/OAM-244>`__ | Add known issue section to release notes                                        |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------+
| `OAM-243  <https://lf-o-ran-sc.atlassian.net/browse/OAM-243>`__ | Network slicing event support by OAM (Simulator)                                |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------+
| `OAM-211  <https://lf-o-ran-sc.atlassian.net/browse/OAM-211>`__ | Update to Java 11                                                               |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------+
| `OAM-172  <https://lf-o-ran-sc.atlassian.net/browse/OAM-172>`__ | Update Deployment                                                               |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------+
| `OAM-143  <https://lf-o-ran-sc.atlassian.net/browse/OAM-143>`__ | 1852,Provide ONAP Guilin based nonrtric-o1-controller image                     |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------+
| `OAM-132  <https://lf-o-ran-sc.atlassian.net/browse/OAM-132>`__ | ONAP Guilin SDN-R based nonrtric-o1-controller                                  |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------+
| `OAM-130  <https://lf-o-ran-sc.atlassian.net/browse/OAM-130>`__ | SPV is failing if Admin state and another parameter present in single request   |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------+
| `OAM-129  <https://lf-o-ran-sc.atlassian.net/browse/OAM-129>`__ | Adding Copyright license for missing files                                      |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------+
| `OAM-127  <https://lf-o-ran-sc.atlassian.net/browse/OAM-127>`__ | Support of heartbeat and Software management Code delivery                      |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------+
| `OAM-123  <https://lf-o-ran-sc.atlassian.net/browse/OAM-123>`__ | Yang model files should be part of scp/oam/modeling                             |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------+
| `OAM-117  <https://lf-o-ran-sc.atlassian.net/browse/OAM-117>`__ | License.txt should update with latest 3rd party software list                   |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------+
| `OAM-115  <https://lf-o-ran-sc.atlassian.net/browse/OAM-115>`__ | Remove unused directories                                                       |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------+
| `OAM-35   <https://lf-o-ran-sc.atlassian.net/browse/OAM-35>`__  | User plane Topology View                                                        |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------+
| `OAM-34   <https://lf-o-ran-sc.atlassian.net/browse/OAM-34>`__  | Control Plane Topology View                                                     |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------+
| `OAM-33   <https://lf-o-ran-sc.atlassian.net/browse/OAM-33>`__  | O1 Topology View                                                                |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------+
| `OAM-32   <https://lf-o-ran-sc.atlassian.net/browse/OAM-32>`__  | A1/E2 Topology View                                                             |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------+

Please see related release notes in `ONAP SDNC <https://docs.onap.org/projects/onap-sdnc-oam/en/jakarta/release-notes.html>`__
and `OpenDaylight <https://docs.opendaylight.org/en/stable-phosphorus/release-notes/index.html>`__ .

Version 5.1.0, 2022-01-31
-------------------------

+-----------------------------------------------------------------+---------------------------------------------------------------------------------+
| Issue                                                           | Summary                                                                         |
+=================================================================+=================================================================================+
| `OAM-48   <https://lf-o-ran-sc.atlassian.net/browse/OAM-48>`__  | Bug fixes in o-ran-sc-du-hello-world yang                                       |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------+
| `OAM-237  <https://lf-o-ran-sc.atlassian.net/browse/OAM-237>`__ | Bug fixes in o-ran-sc-du-hello-world yang                                       |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------+
| `OAM-240  <https://lf-o-ran-sc.atlassian.net/browse/OAM-240>`__ | Late updates on integration deployment                                          |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------+
| `OAM-241  <https://lf-o-ran-sc.atlassian.net/browse/OAM-241>`__ | OAM - VES sender script improvement                                             |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------+

Known issues
------------

+----------------------------------------------------------------------------+---------------------------------------------------------------------------------+
| Issue                                                                      | Summary                                                                         |
+============================================================================+=================================================================================+
| `NETCONF-845 <https://lf-opendaylight.atlassian.net/browse/NETCONF-845>`__ | Support of namespace for referred yang-identity values.                         |
+----------------------------------------------------------------------------+---------------------------------------------------------------------------------+

Version 5.0.0, 2021-11-29
-------------------------

+-----------------------------------------------------------------+---------------------------------------------------------------------------------+
| Issue                                                           | Summary                                                                         |
+=================================================================+=================================================================================+
| `OAM-221  <https://lf-o-ran-sc.atlassian.net/browse/OAM-221>`__ | Wrong value format in measurement ves example                                   |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------+
| `OAM-222  <https://lf-o-ran-sc.atlassian.net/browse/OAM-222>`__ | OAM Deployment enhancements                                                     |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------+
| `OAM-223  <https://lf-o-ran-sc.atlassian.net/browse/OAM-223>`__ | update from stating to released                                                 |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------+
| `OAM-226  <https://lf-o-ran-sc.atlassian.net/browse/OAM-226>`__ | Create yang model for CM according to the requirements by O-DU and the use case |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------+
| `OAM-227  <https://lf-o-ran-sc.atlassian.net/browse/OAM-227>`__ | Create VES stndDefined extension for PM-streaming                               |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------+
| `OAM-228  <https://lf-o-ran-sc.atlassian.net/browse/OAM-228>`__ | Update O-RAN-SC-Du Hello-world yang for CM                                      |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------+
| `OAM-229  <https://lf-o-ran-sc.atlassian.net/browse/OAM-229>`__ | Update header of o-ran-sc-du-hello-world                                        |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------+
| `OAM-230  <https://lf-o-ran-sc.atlassian.net/browse/OAM-230>`__ | Consider CM in o-ran-sc-du-hello-world.yang                                     |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------+
| `OAM-231  <https://lf-o-ran-sc.atlassian.net/browse/OAM-231>`__ | Add slice management to o-ran-sc-du-hello-world.yang                            |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------+
| `OAM-232  <https://lf-o-ran-sc.atlassian.net/browse/OAM-232>`__ | Add performance measurement job management to o-ran-sc-du-hello-world.yang      |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------+
| `OAM-233  <https://lf-o-ran-sc.atlassian.net/browse/OAM-233>`__ | Add subscription management to o-ran-sc-du-hello-world.yang                     |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------+
| `OAM-234  <https://lf-o-ran-sc.atlassian.net/browse/OAM-234>`__ | Create VES stndDefined PM streaming OpenAPI                                     |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------+
| `OAM-235  <https://lf-o-ran-sc.atlassian.net/browse/OAM-235>`__ | Create a Yang notification syntax                                               |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------+
| `OAM-237  <https://lf-o-ran-sc.atlassian.net/browse/OAM-237>`__ | Bug fixes in o-ran-sc-du-hello-world yang                                       |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------+
| `OAM-238  <https://lf-o-ran-sc.atlassian.net/browse/OAM-238>`__ | Update O-RAN-SC wiki release page                                               |
+-----------------------------------------------------------------+---------------------------------------------------------------------------------+


Version 4.0.4, 2021-05-22
-------------------------

+--------------------------------------------------------------------+-------------------------------------------------------------------------+
| Issue                                                              | Summary                                                                 |
+====================================================================+=========================================================================+
| `OAM-177 <https://lf-o-ran-sc.atlassian.net/browse/OAM-177>`__     | Update Documentation for docker supporting IPv6                         |
+--------------------------------------------------------------------+-------------------------------------------------------------------------+
| `OAM-188 <https://lf-o-ran-sc.atlassian.net/browse/OAM-188>`__     | Provide OpenAPI                                                         |
+--------------------------------------------------------------------+-------------------------------------------------------------------------+
| `OAM-191 <https://lf-o-ran-sc.atlassian.net/browse/OAM-191>`__     | O-RU on-boarding                                                        |
+--------------------------------------------------------------------+-------------------------------------------------------------------------+
| `OAM-192 <https://lf-o-ran-sc.atlassian.net/browse/OAM-192>`__     | O-DU on-boarding                                                        |
+--------------------------------------------------------------------+-------------------------------------------------------------------------+
| `OAM-193 <https://lf-o-ran-sc.atlassian.net/browse/OAM-192>`__     | Test environment                                                        |
+--------------------------------------------------------------------+-------------------------------------------------------------------------+
| `OAM-194 <https://lf-o-ran-sc.atlassian.net/browse/OAM-194>`__     | O-RU closed loop recovery                                               |
+--------------------------------------------------------------------+-------------------------------------------------------------------------+
| `OAM-195 <https://lf-o-ran-sc.atlassian.net/browse/OAM-195>`__     | Documentation                                                           |
+--------------------------------------------------------------------+-------------------------------------------------------------------------+
| `OAM-212 <https://lf-o-ran-sc.atlassian.net/browse/OAM-212>`__     | Add section referencing O-RAN specifications                            |
+--------------------------------------------------------------------+-------------------------------------------------------------------------+
| `OAM-213 <https://lf-o-ran-sc.atlassian.net/browse/OAM-213>`__     | Update Deployment docs                                                  |
+--------------------------------------------------------------------+-------------------------------------------------------------------------+

Version 4.0.3, 2021-04-23
-------------------------

+--------------------------------------------------------------------+-------------------------------------------------------------------------+
| Issue                                                              | Summary                                                                 |
+====================================================================+=========================================================================+
| `OAM-150 <https://lf-o-ran-sc.atlassian.net/browse/OAM-150>`__     | Provide settings.xml                                                    |
+--------------------------------------------------------------------+-------------------------------------------------------------------------+
| `OAM-171 <https://lf-o-ran-sc.atlassian.net/browse/OAM-171>`__     | Update docs OAM architecture diagram                                    |
+--------------------------------------------------------------------+-------------------------------------------------------------------------+
| `OAM-178 <https://lf-o-ran-sc.atlassian.net/browse/OAM-178>`__     | Creation of use case docker-compose                                     |
+--------------------------------------------------------------------+-------------------------------------------------------------------------+
| `OAM-179 <https://lf-o-ran-sc.atlassian.net/browse/OAM-179>`__     | Remove unused folders                                                   |
+--------------------------------------------------------------------+-------------------------------------------------------------------------+
| `OAM-181 <https://lf-o-ran-sc.atlassian.net/browse/OAM-181>`__     | Update docker-compose to onap-sdnc:2.1.3                                |
+--------------------------------------------------------------------+-------------------------------------------------------------------------+
| `OAM-182 <https://lf-o-ran-sc.atlassian.net/browse/OAM-182>`__     | Create dev example for additional ves domains                           |
+--------------------------------------------------------------------+-------------------------------------------------------------------------+
| `OAM-183 <https://lf-o-ran-sc.atlassian.net/browse/OAM-183>`__     | Create VES client example for domain 'notification'                     |
+--------------------------------------------------------------------+-------------------------------------------------------------------------+
| `OAM-184 <https://lf-o-ran-sc.atlassian.net/browse/OAM-184>`__     | Create VES client example for domain 'stateChange'                      |
+--------------------------------------------------------------------+-------------------------------------------------------------------------+
| `OAM-185 <https://lf-o-ran-sc.atlassian.net/browse/OAM-185>`__     | Create VES client example for domain 'stndDefined'                      |
+--------------------------------------------------------------------+-------------------------------------------------------------------------+
| `OAM-187 <https://lf-o-ran-sc.atlassian.net/browse/OAM-187>`__     | Update Jenkins Jobs                                                     |
+--------------------------------------------------------------------+-------------------------------------------------------------------------+
| `OAM-189 <https://lf-o-ran-sc.atlassian.net/browse/OAM-189>`__     | Remove builder jobs of project oam                                      |
+--------------------------------------------------------------------+-------------------------------------------------------------------------+


Version 4.0.3, 2021-04-23
-------------------------

+--------------------------------------------------------------------+-------------------------------------------------------------------------+
| Issue                                                              | Summary                                                                 |
+====================================================================+=========================================================================+
| `OAM-150 <https://lf-o-ran-sc.atlassian.net/browse/OAM-150>`__     | Provide settings.xml                                                    |
+--------------------------------------------------------------------+-------------------------------------------------------------------------+
| `OAM-171 <https://lf-o-ran-sc.atlassian.net/browse/OAM-171>`__     | Update docs OAM architecture diagram                                    |
+--------------------------------------------------------------------+-------------------------------------------------------------------------+
| `OAM-178 <https://lf-o-ran-sc.atlassian.net/browse/OAM-178>`__     | Creation of use case docker-compose                                     |
+--------------------------------------------------------------------+-------------------------------------------------------------------------+
| `OAM-179 <https://lf-o-ran-sc.atlassian.net/browse/OAM-179>`__     | Remove unused folders                                                   |
+--------------------------------------------------------------------+-------------------------------------------------------------------------+
| `OAM-181 <https://lf-o-ran-sc.atlassian.net/browse/OAM-181>`__     | Update docker-compose to onap-sdnc:2.1.3                                |
+--------------------------------------------------------------------+-------------------------------------------------------------------------+
| `OAM-182 <https://lf-o-ran-sc.atlassian.net/browse/OAM-182>`__     | Create dev example for additional ves domains                           |
+--------------------------------------------------------------------+-------------------------------------------------------------------------+
| `OAM-183 <https://lf-o-ran-sc.atlassian.net/browse/OAM-183>`__     | Create VES client example for domain 'notification'                     |
+--------------------------------------------------------------------+-------------------------------------------------------------------------+
| `OAM-184 <https://lf-o-ran-sc.atlassian.net/browse/OAM-184>`__     | Create VES client example for domain 'stateChange'                      |
+--------------------------------------------------------------------+-------------------------------------------------------------------------+
| `OAM-185 <https://lf-o-ran-sc.atlassian.net/browse/OAM-185>`__     | Create VES client example for domain 'stndefined'                       |
+--------------------------------------------------------------------+-------------------------------------------------------------------------+
| `OAM-187 <https://lf-o-ran-sc.atlassian.net/browse/OAM-187>`__     | Update Jenkins Jobs                                                     |
+--------------------------------------------------------------------+-------------------------------------------------------------------------+
| `OAM-189 <https://lf-o-ran-sc.atlassian.net/browse/OAM-189>`__     | Remove builder jobs of project oam                                      |
+--------------------------------------------------------------------+-------------------------------------------------------------------------+


Version 4.0.3, 2021-04-23
-------------------------

+--------------------------------------------------------------------+-------------------------------------------------------------------------+
| Issue                                                              | Summary                                                                 |
+====================================================================+=========================================================================+
| `OAM-150 <https://lf-o-ran-sc.atlassian.net/browse/OAM-150>`__     | Provide settings.xml                                                    |
+--------------------------------------------------------------------+-------------------------------------------------------------------------+
| `OAM-171 <https://lf-o-ran-sc.atlassian.net/browse/OAM-171>`__     | Update docs OAM architecture diagram                                    |
+--------------------------------------------------------------------+-------------------------------------------------------------------------+
| `OAM-178 <https://lf-o-ran-sc.atlassian.net/browse/OAM-178>`__     | Creation of use case docker-compose                                     |
+--------------------------------------------------------------------+-------------------------------------------------------------------------+
| `OAM-179 <https://lf-o-ran-sc.atlassian.net/browse/OAM-179>`__     | Remove unused folders                                                   |
+--------------------------------------------------------------------+-------------------------------------------------------------------------+
| `OAM-181 <https://lf-o-ran-sc.atlassian.net/browse/OAM-181>`__     | Update docker-compose to onap-sdnc:2.1.3                                |
+--------------------------------------------------------------------+-------------------------------------------------------------------------+
| `OAM-182 <https://lf-o-ran-sc.atlassian.net/browse/OAM-182>`__     | Create dev example for additional ves domains                           |
+--------------------------------------------------------------------+-------------------------------------------------------------------------+
| `OAM-183 <https://lf-o-ran-sc.atlassian.net/browse/OAM-183>`__     | Create VES client example for domain 'notification'                     |
+--------------------------------------------------------------------+-------------------------------------------------------------------------+
| `OAM-184 <https://lf-o-ran-sc.atlassian.net/browse/OAM-184>`__     | Create VES client example for domain 'stateChange'                      |
+--------------------------------------------------------------------+-------------------------------------------------------------------------+
| `OAM-185 <https://lf-o-ran-sc.atlassian.net/browse/OAM-185>`__     | Create VES client example for domain 'stndDefined'                      |
+--------------------------------------------------------------------+-------------------------------------------------------------------------+
| `OAM-187 <https://lf-o-ran-sc.atlassian.net/browse/OAM-187>`__     | Update Jenkins Jobs                                                     |
+--------------------------------------------------------------------+-------------------------------------------------------------------------+
| `OAM-189 <https://lf-o-ran-sc.atlassian.net/browse/OAM-189>`__     | Remove builder jobs of project oam                                      |
+--------------------------------------------------------------------+-------------------------------------------------------------------------+


Version 4.0.2, 2021-04-02
--------------------------

+----------------------------------------------------------------------------+-------------------------------------------------------------------------+
| Issue                                                                      | Summary                                                                 |
+============================================================================+=========================================================================+
| `OAM-180 <https://lf-o-ran-sc.atlassian.net/browse/OAM-180>`__             | Wrong time format in VES client scripts                                 |
+----------------------------------------------------------------------------+-------------------------------------------------------------------------+
| `OAM-176 <https://lf-o-ran-sc.atlassian.net/browse/OAM-176>`__             | Support of IPv6 by docker-compose                                       |
+----------------------------------------------------------------------------+-------------------------------------------------------------------------+
| `OAM-175 <https://lf-o-ran-sc.atlassian.net/browse/OAM-175>`__             | Update docker-compose and its configurations                            |
+----------------------------------------------------------------------------+-------------------------------------------------------------------------+
| `OAM-174 <https://lf-o-ran-sc.atlassian.net/browse/OAM-174>`__             | Update VES Client scripts supporting VES 7.2                            |
+----------------------------------------------------------------------------+-------------------------------------------------------------------------+
| `OAM-173 <https://lf-o-ran-sc.atlassian.net/browse/OAM-173>`__             | Update VES client scripts supporting https                              |
+----------------------------------------------------------------------------+-------------------------------------------------------------------------+
| `OAM-170 <https://lf-o-ran-sc.atlassian.net/browse/OAM-170>`__             | Delete folder 'model' from OAM repo'                                    |
+----------------------------------------------------------------------------+-------------------------------------------------------------------------+
| `OAM-169 <https://lf-o-ran-sc.atlassian.net/browse/OAM-169>`__             | Use case driven yang for O-DU                                           |
+----------------------------------------------------------------------------+-------------------------------------------------------------------------+
| `OAM-168 <https://lf-o-ran-sc.atlassian.net/browse/OAM-168>`__             | Update namespace definitions in prototype yangs of O-RAN-SC             |
+----------------------------------------------------------------------------+-------------------------------------------------------------------------+
| `OAM-164 <https://lf-o-ran-sc.atlassian.net/browse/OAM-164>`__             | Add WG4 november train yangs modules                                    |
+----------------------------------------------------------------------------+-------------------------------------------------------------------------+
| `SDNC-1480   <https://lf-onap.atlassian.net/browse/SDNC-1480>`__           | O-RAN (FrontHaul) deviceManager: support of GuiCutThrough               |
+----------------------------------------------------------------------------+-------------------------------------------------------------------------+
| `CCSDK-3161  <https://lf-onap.atlassian.net/browse/CCSDK-3161>`__          | O-RAN (FrontHaul) deviceManager: o-ran-fm.yang/alarm-notif to VES:fault |
+----------------------------------------------------------------------------+-------------------------------------------------------------------------+
| `CCSDK-3160  <https://lf-onap.atlassian.net/browse/CCSDK-3160>`__          | CallHome to VES:pnfRegistration                                         |
+----------------------------------------------------------------------------+-------------------------------------------------------------------------+
| `NETCONF-766 <https://lf-opendaylight.atlassian.net/browse/NETCONF-766>`__ | Logging al RESTCONF requests and responses [1]_                         |
+----------------------------------------------------------------------------+-------------------------------------------------------------------------+
| `NETCONF-744 <https://lf-opendaylight.atlassian.net/browse/NETCONF-744>`__ | Read whole leaf-list using get/get-config RPC [1]_                      |
+----------------------------------------------------------------------------+-------------------------------------------------------------------------+
| `NETCONF-735 <https://lf-opendaylight.atlassian.net/browse/NETCONF-735>`__ | Support NETCONF get/get-config with multiple selected subtrees [1]_     |
+----------------------------------------------------------------------------+-------------------------------------------------------------------------+

.. [1] Patched via MAVEN repo into CCSDK as long as code is not merged into OpenDaylight master branch


Version 4.0.1, 2021-03-12
--------------------------

+----------------------------------------------------------------+-------------------------------------------------------------+
| Issue                                                          | Summary                                                     |
+================================================================+=============================================================+
| `OAM-166 <https://lf-o-ran-sc.atlassian.net/browse/OAM-166>`__ | Add WG4 July 2020 yang modules                              |
+----------------------------------------------------------------+-------------------------------------------------------------+
| `OAM-163 <https://lf-o-ran-sc.atlassian.net/browse/OAM-163>`__ | Rename yang filename to <module>@<revision> format          |
+----------------------------------------------------------------+-------------------------------------------------------------+
| `OAM-160 <https://lf-o-ran-sc.atlassian.net/browse/OAM-160>`__ | Modeling Repo: SIM directory not longer required            |
+----------------------------------------------------------------+-------------------------------------------------------------+
| `OAM-159 <https://lf-o-ran-sc.atlassian.net/browse/OAM-159>`__ | Remove yang models from Repo                                |
+----------------------------------------------------------------+-------------------------------------------------------------+
| `OAM-154 <https://lf-o-ran-sc.atlassian.net/browse/OAM-154>`__ | OAM tr069: Changing .gitignore for IntelliJ related files   |
+----------------------------------------------------------------+-------------------------------------------------------------+
| `OAM-121 <https://lf-o-ran-sc.atlassian.net/browse/OAM-121>`__ | Request to modify SMO deployment SOP                        |
+----------------------------------------------------------------+-------------------------------------------------------------+
| `OAM-120 <https://lf-o-ran-sc.atlassian.net/browse/OAM-120>`__ | Release dashboard image at version 2.0.3                    |
+----------------------------------------------------------------+-------------------------------------------------------------+

Version 2.0.4, 2020-06-13
--------------------------

* Documentation updated
* Develop reusable OAM API such that the first consumer being a VTH can query, subscribe or publish on a DMaaP topic	Story
* Create helm deployment for SMO
* Feature split for starting devicemanagers
* Seed coder for an YANG linter
* Please see also Release Notes of `ONAP SDNC, DCAE, DMaaP, OOM <https://docs.onap.org/en/latest/release/index.html>`_

Version 2.0.3, 2020-04-08
-------------------------

* What is an SMO?
* Provide xRAN data-models
* Provide curl bash scripts for Software Management
* Add jenkins jobs for oam
* Add parents to model artifacts
* Add top level pom file to distribution
* Wrong image tag in non-rt-ric-o1-controller distribution pom
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
