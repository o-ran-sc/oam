# VES Events

VES: Virtual Event Streaming (HTTP1.1/json-schema)

This document describes sending of VES events according to 
[VES 7.2.1](https://gerrit.onap.org/r/gitweb?p=dcaegen2/collectors/ves.git;a=blob;f=etc/CommonEventFormat_30.2.1_ONAP.json) 
as expected by O-RAN Operation and Maintenance Interface Specification. 

## Prerequisites

Python3 is expected to run the scripts.

```
pip3 install requests
```

## VES Domains

The syntax of a single VES event is devices into a common header and an event
specific body.

The event specific bodies are are identified by the VES domain.

### VES Domain "fault"

tbd.

### VES Domain "heartbeat",

The script simulates a VES event of domain "heartbeat" from SDN-R to DCAE VES-Collector.

The following example show the usage of this script:

```
python3 sendVesHeartbeat.py
```

### VES Domain "measurement",

tbd.

### VES Domain "mobileFlow",

tbd.

### VES Domain "notification",

The script simulates a VES event of domain "notification" from a physical 
network-function to DCAE VES-Collector.

The following example show the usage of this script:

```
python3 sendVesNotification.py --pnfId nSky
```

### VES Domain "other",

tbd.

### VES Domain "perf3gpp",

tbd.

### VES Domain "pnfRegistration",

tbd.

### VES Domain "sipSignaling",

tbd.

### VES Domain "stateChange",

The script simulates a VES event of domain "stateChange" from a physical 
network-function to DCAE VES-Collector.

The following example show the usage of this script:

```
python3 sendVesStateChange.py --pnfId nSky
```

### VES Domain "stndDefined",

tbd.

### VES Domain "syslog",

tbd.

### VES Domain "thresholdCrossingAlert",

tbd.

### VES Domain "voiceQuality"

tbd.
