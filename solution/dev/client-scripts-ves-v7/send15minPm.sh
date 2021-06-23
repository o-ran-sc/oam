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
              domain="measurement";
   collectionEndTime=$(( $timeInS - $(($timeInS % 900))));
 collectionStartTime=$(( collectionEndTime - 900 ));
         granularity="PM15min";
 
declare -A mapping=(
    [domain]=$domain
    [controllerName]=$(hostname --fqdn)
    [pnfId]=${pnfIdByType[$pnfType]}
    [granularity]=$granularity
    [eventId]="${pnfIdByType[$pnfType]}_${collectionEndTime}_${granularity}"
    [eventType]=${eventType}
    [type]=${pnfType^^}
    [interface]=${interfaceByType[$pnfType]}
    [timestamp]=${timestamp}
    [eventTime]=${eventTime}
    [collectionStartTime]=${collectionStartTime}000000
    [collectionEndTime]=${collectionEndTime}000000
    [intervalStartTime]=$(date -u -R -d @$collectionStartTime )
    [intervalEndTime]=$(date -u -R -d @$collectionEndTime )
    [vendor]=${vendorsByType[$pnfType]^^}
    [model]=${modelByType[$pnfType]}
)

echo "################################################################################";
echo "# send 15min performance values";
echo
for key in "${!mapping[@]}"
do
  label=$spaces$key;
  label=${label:(-20)};
  echo "$label: ${mapping[$key]}";
  if [ $key = "collectionStartTime" ] || [ $key = "collectionEndTime" ]; then
      sequence="$sequence s/\"@$key@\"/${mapping[$key]}/g; "
  else
      sequence="$sequence s/@$key@/${mapping[$key]}/g; "
  fi  
done
echo;

body=./json/examples/${pnfType^^}-${domain}.json
sed -e "$sequence" ./json/templates/$domain.json > $body

curl -i -k -u $basicAuthVes -X POST -d  @${body} --header "Content-Type: application/json" $urlVes