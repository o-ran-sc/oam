.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. SPDX-License-Identifier: CC-BY-4.0
.. Copyright (C) 2020 highstreet technologies and others

OAM Controller Configuration and Deployment
===========================================

This documents the configuration and deployment of the O-RAN SC O1 Controller as
part of the SMO implementations by the ONAP project.

The SMO deployment for O-RAN-SC Bronze Release bases on ONAP-Frankfurt-Release

This procedure provides:
* ONAP-DCAE
* ONAP-DMaaP
* ONAP-SDNC (single node, SMO functionality)

Limitations (wip)
-----------------
* ONAP-AAF: not yet supported

Prerequisites
-------------
* kubernetes cluster (1.13.5)
* helm installation (2.16.x)
* More details: `setup cloud environment(openstack/kubernetes) <https://docs.onap.org/en/elalto/guides/onap-developer/settingup/index.html>`_

Setup
-----

* clone oom repo from gerrit.onap.org
* fetch patchset for ONAP-SDNC

.. code-block:: RST
  :linenos:

   mkdir ~/workspace
   cd ~/workspace
   git clone -b frankfurt http://gerrit.onap.org/r/oom --recurse-submodules oom_smo
   cd oom_smo
   git fetch "https://gerrit.onap.org/r/oom" refs/changes/31/106331/6 && git checkout FETCH_HEAD
   # HEAD is now at 275f7de9 [SDNC] oom for clustered disaggregated SDN-R
   sudo cp -R ~/workspace/oom_smo/kubernetes/helm/plugins/ ~/.helm

* verifiy if local helm repo is available, otherwise follow intructions in onap setup

.. code-block:: RST
  :linenos:

  helm repo list
  #NAME    URL
  #stable  https://kubernetes-charts.storage.googleapis.com
  #local   http://127.0.0.1:8879
  
* build local onap helm repo

.. code-block:: RST
  :linenos:
 
  cd ~/workspace/oom_smo/kubernetes
  make all; make onap
  # take a coffee
  helm search onap

* create an overwrite yaml file, e.g. deploy_smo_bronce.yaml

In Kubernetes deployment, all file contents are provided by a
configuration map. Construction of Helm charts, config maps and other
Kubernetes deployment resources is beyond the scope of this document.

.. code-block:: RST
  :linenos:

  cat ~/workspace/smo/deploy_smo_bronce.yaml
  # Copyright © 2020 Amdocs, Bell Canada, highstreet technologies GmbH
  #
  # Licensed under the Apache License, Version 2.0 (the "License");
  # you may not use this file except in compliance with the License.
  # You may obtain a copy of the License at
  #
  #       http://www.apache.org/licenses/LICENSE-2.0
  #
  # Unless required by applicable law or agreed to in writing, software
  # distributed under the License is distributed on an "AS IS" BASIS,
  # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  # See the License for the specific language governing permissions and
  # limitations under the License.
   
  ###################################################################
  # This override file enables helm charts for all ONAP applications.
  ###################################################################
  global:
    aafEnabled: false
    masterPassword: Berlin1234!
  cassandra:
    enabled: false
  mariadb-galera:
    enabled: true
  aaf:
    enabled: false
  aai:
    enabled: false
  appc:
    enabled: false
  clamp:
    enabled: false
  cli:
    enabled: false
  consul:
    enabled: true
  contrib:
    enabled: false
  dcaegen2:
    enabled: true
  dmaap:
    enabled: true
  esr:
    enabled: false
  log:
    enabled: false
  sniro-emulator:
    enabled: false
  oof:
    enabled: false
  msb:
    enabled: true
  multicloud:
    enabled: false
  nbi:
    enabled: false
  policy:
    enabled: false
  pomba:
    enabled: false
  portal:
    enabled: false
  robot:
    enabled: false
  sdc:
    enabled: false
  sdnc:
    enabled: true
    replicaCount: 1
    config:
      sdnr:
        sdnrwt: true 
        sdnronly: true
        sdnrmode: dm
        mountpointRegistrarEnabled: true
        mountpointStateProviderEnabled: true
    cds:
      enabled: false
    dmaap-listener:
      enabled: false
    ueb-listener:
      enabled: false
    sdnc-portal:
      enabled: false
    sdnc-ansible-server:
      enabled: false
    dgbuilder:
      enabled: false
    sdnc-web:
      enabled: false
  so:
    enabled: false
  uui:
    enabled: false
  vfc:
    enabled: false
  vid:
    enabled: false
  vnfsdk:
    enabled: false
  modeling:
    enabled: false


* deploy smo

.. code-block:: RST
  :linenos:

  helm -n dev-smo local/onap -f ~/workspace/smo/deploy_smo_bronce.yaml --namespace onap --timeout 900

* verifiy deployment

.. code-block:: RST
  :linenos:

  helm ls

* verifiy pnf-registration, fault notification use case

Please open the O1 Dashboard: http://localhost:8181/odlux/index.html
