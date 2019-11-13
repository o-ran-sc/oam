.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. SPDX-License-Identifier: CC-BY-4.0
.. Copyright (C) 2019 highstreet technologies GmbH


Operation and Maintenance Release Notes
=======================================

This document provides the release notes for O-RAN-SC Amber release of the Operation and Maintenance (OAM) project. 

.. contents::
   :depth: 3
   :local:


Version history
---------------

+--------------------+--------------------+--------------------+--------------------+
| **Date**           | **Ver.**           | **Author**         | **Comment**        |
|                    |                    |                    |                    |
+--------------------+--------------------+--------------------+--------------------+
| 2019-09-08         | 0.1.0              |                    | Initial Version    |
|                    |                    |                    |                    |
+--------------------+--------------------+--------------------+--------------------+
| 2019-09-18         | 0.1.1              |                    | Initial Version    |
|                    |                    |                    | DEV environment    |
+--------------------+--------------------+--------------------+--------------------+
| 2019-11-14         | 1.0                |                    | Docs added         |
|                    |                    |                    |                    |
+--------------------+--------------------+--------------------+--------------------+


Summary
-------

According to the O-RAN-SC-OAM-Architecture document all ManagedElements 
(near-real-time-RIC, O-CU-CP, O-CU-UP, O-DU and O-RU) implement the O1-interface.

The O-RAN-OAM-interface specification defines

a NetConf-Server for Configuration Management (CM) and
a http-client for Fault Managment (FM), Performance Management (PM) and other events
on each Management-Service-Provider (MnS-Provider) running on the ManagedElement (ME).



The O-RAN-SC-OAM project provides reference implementation according to the O-RAN OAM (WG1) documents. 
In addition we provide a common MnS-Consumer for development and module test purposes. 
The assumption is that the projects for the ManagedElements can concentrate on the more important user-plane.
