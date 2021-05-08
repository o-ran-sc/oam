#!/bin/bash
################################################################################
#
# Copyright 2019 highstreet technologies GmbH and others
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
      domain="pnfRegistration";

declare -A mapping=(
    [controllerName]=$(hostname --fqdn)
    [domain]=$domain
    [eventId]="${pnfIdByType[$pnfType]}_${modelByType[$pnfType]}"
    [eventTime]=${eventTime}
    [eventType]=EventType5G
    [pnfId]=${pnfIdByType[$pnfType]}
    [type]=${pnfType^^}
    [model]=${modelByType[$pnfType]}
    [oamIp]=${oamIpByType[$pnfType]}
    [macAddress]=02:42:f7:d4:62:ce
    [oamIpV6]=0:0:0:0:0:ffff:a0a:0${oamIpByType[$pnfType]:(-2)}
    [vendor]=${vendorsByType[$pnfType]^^}
    [timestamp]=${timestamp}
    [eventId]="${pnfIdByType[$pnfType]}_${modelByType[$pnfType]}"
    [eventTime]=${eventTime}
    [eventType]=EventType5G
)

echo "################################################################################";
echo "# send PNF registration";
echo;
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

body="./json/examples/${pnfType^^}-${domain}.json"
sed -e "$sequence" ./json/templates/$domain.json > $body;

curl -i -k -u $basicAuthVes -X POST -d @${body} --header "Content-Type: application/json" $urlVes