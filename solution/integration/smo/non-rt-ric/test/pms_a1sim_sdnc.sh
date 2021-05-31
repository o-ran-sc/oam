#!/bin/bash

#  ============LICENSE_START===============================================
#  Copyright (C) 2021 Nordix Foundation. All rights reserved.
#  ========================================================================
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#  ============LICENSE_END=================================================

unset http_proxy https_proxy
SHELL_FOLDER=$(cd "$(dirname "$0")";pwd)
docker stop $(docker ps -aq)
docker system prune -f
source ${SHELL_FOLDER}/setup.sh

cd ${SHELL_FOLDER}/../config
cp application_configuration.json.sdnc application_configuration.json

cd ${SHELL_FOLDER}/../
docker-compose -f docker-compose.yml -f sdnc/docker-compose.yml up -d

checkStatus(){
    for i in {1..60}; do
        res=$($1)
        echo "$res"
        expect=$2
        if [ "$res" == "$expect" ]; then
            echo -e "$3 is alive!\n"
            break;
        else
            sleep $i
        fi
    done
}
# Healthcheck docker containers

# check SIM1 status
echo "check SIM1 status:"
checkStatus "curl -skw %{http_code} http://localhost:30001/" "OK200" "SIM1"

# check SIM2 status
echo "check SIM2 status:"
checkStatus "curl -skw %{http_code} http://localhost:30003/" "OK200" "SIM2"

# check SIM3 status
echo "check SIM3 status:"
checkStatus "curl -skw %{http_code} http://localhost:30005/" "OK200" "SIM3"

# check PMS status
echo "check PMS status:"
checkStatus "curl -skw %{http_code} http://localhost:8081/status" "hunky dory200" "PMS"

# check SDNC status
echo "check SDNC status:"
checkStatus "curl -s -o /dev/null -I -w %{http_code} http://localhost:8282/apidoc/explorer/" "200" "SDNC"

cd ${SHELL_FOLDER}/../data
./preparePmsData.sh

