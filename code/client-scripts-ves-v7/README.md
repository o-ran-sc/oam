# O-RAN Components interfacing with VES-Collector

Test scripts for interfacing with DCAE.

ONAP Honolulu DCAE VES-Collector supports the interface definition  [CommonEventFormat_30.2.1_ONAP.json](https://gerrit.onap.org/r/gitweb?p=dcaegen2/collectors/ves.git;a=blob;f=etc/CommonEventFormat_30.2.1_ONAP.json).

The ONAP VES version is described in [ONAP documentation](https://docs.onap.org/projects/onap-vnfrqts-requirements/en/latest/Chapter8/ves_7_2/ves_event_listener_7_2.html?highlight=dcae%20ves%20header#).

VES domain 'stndDefined' offers the capability to inject external schema definitions of the VES.
This way the 3GPP notification syntax can be transported. Please see [SA88-Rel16 schema](https://forge.3gpp.org/rep/sa5/MnS/tree/SA88-Rel16/OpenAPI).


## Prerequisites

This git project must be cloned on a ubuntu machine in order to execute the bash scripts.
DCAE provide REST interfaces. In order to perform HTTP request [cURL](https://curl.haxx.se/) is used.

In case cURL needs to be please use the following command in a terminal.

```
sudo apt install curl
```

Python3 is expected to run some scripts.

```
pip3 install requests
```

It is necessary to configure the DCAE servers for valid execution of the bash scripts.
Please update the variables in [config](-/config) accordingly to the test environment.

```
urlVes=http://localhost:8443/eventListener/v7
basicAuthVes=sample1:sample1
```

## Concept

Several tests scripts are available in the root of this project.
The bash and python scripts will perform an HTTPS-POST request to a VES-Collector.

## VES Domains

The syntax of a single VES event is devices into a common header and an event
specific body.

The event specific bodies are are identified by the VES domain.

### VES Domain "fault"

This script 'sendFault' sends a VES message of domain "fault" to DCAE. It requires three command line parameters:

1. **equipmentType**: Valid equipment types for 1806 and 1810 are [pnf2, FYNG, R2D2, 7DEV, nSky, 1OSF] according to document "295672 SDN-R System Requirements".

2. **alarmType**: or alarm name. Any string which references a supported alarm name of the equipment type.

3. **severity**: The severity of tha alarm as defined by [VES schema](https://gerrit.onap.org/r/gitweb?p=dcaegen2/collectors/ves.git;a=blob;f=etc/CommonEventFormat_30.2.1_ONAP.json).

The following example show the usage of this script. The alarm "lossOfSignal" for equipment type "nSky" with severity "CRITICAL" will be send.

```
./sendFault.sh nSky lossOfSignal CRITICAL
```

### VES Domain "heartbeat",

The script 'sendVesHeartbeat' simulates a VES event of domain "heartbeat" from SDN-R to DCAE VES-Collector.

The following example show the usage of this script:

```
python3 sendVesHeartbeat.py
```

### VES Domain "measurement",

This script 'send15minPm' sends a VES message of domain "measurementsForVfScaling" to DCAE. The script requires one input parameter. This parameter defines the equipment type. Valid equipment types for 1806 and 1810 are [pnf2, FYNG, R2D2, 7DEV, nSky, 1OSF] according to document "295672 SDN-R System Requirements".

```
./send15minPm.sh FYNG
```

### VES Domain "mobileFlow",

Not required by O-RAN Alliance OAM specification.

### VES Domain "notification",

The script 'sendVesNotification' simulates a VES event of domain "notification" from a network-function to DCAE VES-Collector.

The following example show the usage of this script:

```
python3 sendVesNotification.py --pnfId nSky
```

### VES Domain "other",

Not required by O-RAN Alliance OAM specification.

### VES Domain "perf3gpp",

Not required by O-RAN Alliance OAM specification.

### VES Domain "pnfRegistration",

The script 'pnfRegister' creates a PNF object in A&AI. The script requires one input parameter. This parameter defines the equipment type. Valid equipment types for 1806 and 1810 are [pnf2, FYNG, R2D2, 7DEV, nSky, 1OSF] according to document "295672 SDN-R System Requirements".

```
./pnfRegister.sh 7DEV
```
### VES Domain "sipSignaling",

Not required by O-RAN Alliance OAM specification.

### VES Domain "stateChange",

The script 'sendVesStateChange' simulates a VES event of domain "stateChange" from a network-function to DCAE VES-Collector.

The following example show the usage of this script:

```
python3 sendVesStateChange.py --pnfId nSky
```

### VES Domain "stndDefined",

The script 'sendVesStndDefined' simulates a VES event of domain "stateChange" from a network-function to DCAE VES-Collector. Four schema definitions by 3GPP are supported:

- 3GPP-FaultSupervision
- 3GPP-Heartbeat
- 3GPP-PerformanceAssurance
- 3GPP-Provisioning

The following examples show the usage of this script:

```
python sendVesStndDefined.py --pnfId nSky --body 3GPP-FaultSupervision
python sendVesStndDefined.py --pnfId nSky --body 3GPP-Heartbeat
python sendVesStndDefined.py --pnfId nSky --body 3GPP-PerformanceAssurance
python sendVesStndDefined.py --pnfId nSky --body 3GPP-Provisioning
 ```

### VES Domain "syslog",

Not required by O-RAN Alliance OAM specification.

### VES Domain "thresholdCrossingAlert",

This script 'sendTca' sends a VES message of domain "thresholdCrossingAlert" to DCAE. It requires three command line parameters:

1. **equipmentType**: Valid equipment types for 1806 and 1810 are [pnf2, FYNG, R2D2, 7DEV, nSky, 1OSF] according to document "295672 SDN-R System Requirements".

2. **alarmType**: or alarm name. Any string which references a supported alarm name (TCA) of the equipment type.

3. **alertAction**: The action of TCA as defined by [VES schema](https://gerrit.onap.org/r/gitweb?p=dcaegen2/collectors/ves.git;a=blob;f=etc/CommonEventFormat_30.2.1_ONAP.json).

The following example show the usage of this script. The TCA with name "TCA" for equipment type "pnf2" with alarmAction "SET" will be send.

```
./sendTca.sh pnf2 TCA SET
```

### VES Domain "voiceQuality"

Not required by O-RAN Alliance OAM specification.

### Sending a VES event list

This script send a VES message of domain "fault" AND "heartbeat" as event list to DCAE. It requires three command line parameters:

1. **equipmentType**: Valid equipment types for 1806 and 1810 are [pnf2, FYNG, R2D2, 7DEV, nSky, 1OSF] according to document "295672 SDN-R System Requirements".

2. **alarmType**: or alarm name. Any string which references a supported alarm name of the equipment type.

3. **severity**: The severity of tha alarm as defined by [VES schema](https://gerrit.onap.org/r/gitweb?p=dcaegen2/collectors/ves.git;a=blob;f=etc/CommonEventFormat_30.2.1_ONAP.json).

The following example show the usage of this script. The alarm "lossOfSignal" for equipment type "nSky" with severity "CRITICAL" will be send.

```
./sendEventList.sh pnf2 lossOfSignal CRITICAL
```
