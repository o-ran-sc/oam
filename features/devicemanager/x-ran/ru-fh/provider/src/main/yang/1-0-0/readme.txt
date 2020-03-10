xRAN Forum YANG Models

xRAN has defined an open, interoperable and efficient fronthaul interface.
The definition of this interface includes the xRAN control, user and
synchronization (CUS) plane specification .

To complement the CUS plane specification, xRAN has also defined the management
plane specification . Significantly, the management plane specification uses
NETCONF/YANG as the network management protocol and data modelling language.

The M-Plane specification describes how to use a set of xRAN defined YANG models
for managing the xRAN defined RU. This zip file contains the YANG models for
the xRAN defined Radio Unit (RU).

Directory of YANG models

All revisions of YANG models are available in this directory, with the revision
being embedded in the path for a particular model. For example all v1.0.0 models
are available using the directory path 

http://www.xran.org/resources/yang/1-0-0/

Under the directory, the is a zip file that contains several sub-directories
used to organize the models according to the functionality they support:

         Interfaces: Covering models for handling the RU’s Ethernet and IP
                     interfaces
         Operations: Covering models for operational aspects, including S/W,
                     performance and file management
         Radio:      Covering models used to support the CU Plane lower PHY
                     functionality
         Sync:       Covering models for synchronisation, including GNSS, PTP
                     and SyncE
         System:     Covering models for hardware management, NETCONF
                     supervision, user account management and fan operation

Validation

The YANG files have been tested for compilation with pyang version 1.7.4.

Known Issues

A list of functionalities not currently supported by these YANG models is
defined in the M-Plane specification.

Future Revisions

Revisions to these YANG models are expected to be made to correct errors and
enable support for new functionalities. The YANG revisions statement will be
used to describe those changes to the YANG model that are backwards compatible.
Backwards incompatible changes will be addressed by using a major version number
as part of the model name and namespace.
