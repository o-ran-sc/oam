# Standalone VES Test Collector

This solution is intended to test VES messages with different format versions.

## Customizing

define within '.env' file

```
EXT_VES_PORT=30007
VES_API=7
VES_FORMAT_FILE=CommonEventFormat_30.1_ONAP.json
LOCAL_VES_MOUNT=/var/tmp/ves-v7
```

this would mean:

 *  ves-testcollector URL is <ip_host>:30007/eventListener/v7
 *  logs are stored on docker host  /var/tmp/VES.V7/logs
 *  VES format file is 'CommonEventFormat_30.1_ONAP.json'
 *  
 ## USAGE

```
docker-compose up -d
cd /var/tmp/ves-v7/logs
tail -f evel-output.log

```