#!/bin/bash
################################################################################
#
# Copyright 2022 highstreet technologies GmbH and others
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

################################################################################
# Script to send an VES Message Event to DCAE

. config;
      pnfType=${1,,};
    alarmType=$2;
     severity=$3;
       raised=$4;
       domain="stndDefined";

# exception for controller alarms
if [ "${pnfType^^}" == "SDNR" ]
  then
    eventType="ONAP_SDNR_Controller";
fi

if [ "${raised,,}" != "cleared" ]
  then
    raised="new";
fi

declare -A mapping=(
    [domain]=$domain
    [controllerName]=$(hostname --fqdn)
    [pnfId]=${pnfIdByType[$pnfType]}
    [eventId]="${pnfIdByType[$pnfType]}_${interfaceByType[$pnfType]}_${alarmType}"
    [eventType]=${eventType}
    [type]=${pnfType^^}
    [interface]=${interfaceByType[$pnfType]}
    [alarm]=${alarmType}
    [severity]=${severity}
    [timestamp]=${timestamp}
    [eventTime]=${eventTime}
    [vendor]=${vendorsByType[$pnfType]^^}
    [model]=${modelByType[$pnfType]}
)

echo "################################################################################";
echo "# send NotifyNewAlarm or NotifyClearedAlarm";
echo;
echo "  alarmEventType: $raised"
for key in "${!mapping[@]}"
do
  #label=${${"$spaces$i"}:(-14)};
  label=$spaces$key;
  label=${label:(-16)};
  echo "$label: ${mapping[$key]}";
  if [ $key = "timestamp" ]; then
      sequence="$sequence s/\"@$key@\"/${mapping[$key]}/g; "
  else
      sequence="$sequence s/@$key@/${mapping[$key]}/g; "
  fi
done
echo;

body="./json/examples/${pnfType^^}-${alarmType}-${severity}-${raised,,}-${domain}.json"
template="./json/templates/$domain-r16-notify-${raised,,}-alarm.json"
sed -e "$sequence" $template > $body;

curl -i -k -u $basicAuthVes -X POST -d @${body} --header "Content-Type: application/json" $urlVes
