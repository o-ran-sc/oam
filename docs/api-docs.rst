.. ===============LICENSE_START=======================================================
.. ORAN-OSC CC-BY-4.0
.. ===================================================================================
.. Copyright (C) 2019 highstreet technologies GmbH. All rights reserved.
.. ===================================================================================
.. This ORAN-OSC documentation file is distributed by highstreet technologies GmbH
.. under the Creative Commons Attribution 4.0 International License (the "License");
.. you may not use this file except in compliance with the License.
.. You may obtain a copy of the License at
..
..      http://creativecommons.org/licenses/by/4.0
..
.. This file is distributed on an "AS IS" BASIS,
.. WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
.. See the License for the specific language governing permissions and
.. limitations under the License.
.. ===============LICENSE_END=========================================================

.. contents::
   :depth: 3
   :local:

API-docs
============

The Operation and Maintenance (OAM) project implements artifacts of the O-RAN Aliance O1 Archtecture and Interface specufication.

API Introduction
---------------

According to the O-RAN Operation and Maintenance Archtecture and Interface specification the O1 interface uses the protocol and feature set of NetConf for configuration operations, while all kind of notifications are send from the O-RAN compomnents (ManagedElements) to the Service Management and Orchestion Framework (SMO) are REST with a json body as defined by VES. 

API Functions
---------------

The O1 interface allows the user and other applications to read and modify the configuration, to read status and capabilites from the ManagedElements and to infom user and/or application about important changes of the configuration and functions of the ManagedElements (FCAPS).

