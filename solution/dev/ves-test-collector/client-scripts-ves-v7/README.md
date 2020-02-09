# O-RAN Components interfaceing with VES-Collector

Test scripts for interfaceing with DCAE.

For ONAP Frankfurt the interface definition with DCAE is: [CommonEventFormat_30.1_ONAP.json](./json/schema/CommonEventFormat_30.1_ONAP.json).
The ONAP VES version are described in [ONAP documentation](https://onap.readthedocs.io/en/latest/submodules/vnfrqts/requirements.git/docs/Chapter8/ves7_1spec.html).

For ONAP Frankfurt the interface definition with A&AI is: [add link when known]().

## Prerequisites

This git project must be cloned on a ubuntu maschine in order to execute the bash scripts.
DCAE provide REST interfaces. In order to perform HTTP request [cURL](https://curl.haxx.se/) is used. 

In case cURL needs to be please use the following command in a terminal.

```
sudo apt-get install curl 
```

For interfacing with cert (https) and key must be extracted acoording to
https://wiki.web.att.com/pages/viewpage.action?spaceKey=SDNCDEV&title=Query+AAI+Using+Postman.
```
./_extractCertAndKey.sh
```
You will be ask to enter the "Input Password". 
The password must not be shared here, please ask your admin.

It is nessary to configure the DCAE servers for valid excecution of the bash scripts.
Please update the varables in [config](-/config) accordintly to the test enviroment.

```
urlVes=http://localhost:8443/eventListener/v7
basicAuthVes=ves:ves
```

## Concept

Several tests scripts are avialable in the root of this project. 
The bash scripts will perform a cURL command to send a REST request to the A&AI or DCAE server.

![SDN-R NBIs](images/sndr-nbis.png "SDN-R NBIs" )

## Scripts

This chapter descibes the several test scripts its usage and functions.

### _example

This scripts calls all the other scripts in order to give valid examples and to expain by examples the usage ot the other scripts.

```
./_example.sh 
```

Please see valid examples using the followfing command (or continue reading):

```
cat _example.sh 
```

### createPnf

The script creates a PNF object in A&AI. The script requires one input parameter. This parameter defines the equipment type. Valid equipment types for 1806 and 1810 are [1234, FYNG, R2D2, 7DEV, nSky, 1OSF] according to document "295672 SDN-R System Requirements".

```
./createPnf.sh 7DEV
```

### sendHeartbeat

The script sends a "heardbeat" from SDN-R to DCAE.

The following example show the usage of this script:
```
./sendHeartbeat.sh
```


### sendFault

This script send a VES message of domain "fault" to DCAE. It requires three command line parameters:

1. **equipmentType**: Valid equipment types for 1806 and 1810 are [1234, FYNG, R2D2, 7DEV, nSky, 1OSF] according to document "295672 SDN-R System Requirements".

2. **alarmType**: or alarm name. Any string which references a supported alarm name of the equipment type.

3. **severity**: The severity of tha alarm as defined by [VES schema](./json/schema/CommonEventFormat_30.1_ONAP.json). 

The following example show the usage of this script. The alarm "lossOfSignal" for equipment type "nSky" with severtiy "CRITICAL" will be send.

```
./sendFault.sh nSky lossOfSignal CRITICAL
```


### sendTca

This script send a VES message of domain "thresholdCrossingAlert" to DCAE. It requires three command line parameters:

1. **equipmentType**: Valid equipment types for 1806 and 1810 are [1234, FYNG, R2D2, 7DEV, nSky, 1OSF] according to document "295672 SDN-R System Requirements".

2. **alarmType**: or alarm name. Any string which references a supported alarm name (TCA) of the equipment type.

3. **alertAction**: The action of TCA as defined by [VES schema](./json/schema/CommonEventFormat_28.4.1.json). 

The following example show the usage of this script. The TCA with name "TCA" for equipment type "1234" with alarmAction "SET" will be send.

```
./sendTca.sh 1234 TCA SET
```


### send15minPm

This script send a VES message of domain "measurementsForVfScaling" to DCAE. The script requires one input parameter. This parameter defines the equipment type. Valid equipment types for 1806 and 1810 are [1234, FYNG, R2D2, 7DEV, nSky, 1OSF] according to document "295672 SDN-R System Requirements".

```
./send15minPm.sh FYNG
```

### sendEventList

This script send a VES message of domain "fault" AND "heartbeat" as event list to DCAE. It requires three command line parameters:

1. **equipmentType**: Valid equipment types for 1806 and 1810 are [1234, FYNG, R2D2, 7DEV, nSky, 1OSF] according to document "295672 SDN-R System Requirements".

2. **alarmType**: or alarm name. Any string which references a supported alarm name of the equipment type.

3. **severity**: The severity of tha alarm as defined by [VES schema](./json/schema/CommonEventFormat_30.1_ONAP.json). 

The following example show the usage of this script. The alarm "lossOfSignal" for equipment type "nSky" with severtiy "CRITICAL" will be send.

```
./sendEventList.sh 1234 lossOfSignal CRITICAL
```
