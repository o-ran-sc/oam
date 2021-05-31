#!/usr/bin/env bash
###############################################################################
# Copyright 2017 Huawei Technologies Co., Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Modifications copyright (c) 2021 Nordix Foundation
#
###############################################################################

unset http_proxy https_proxy
SHELL_FOLDER=$(cd "$(dirname "$0")";pwd)
docker stop $(docker ps -aq)
docker system prune -f
docker network create oam
docker network create smo

cd ${SHELL_FOLDER}/../config/pms/
cp application_configuration.json.nosdnc application_configuration.json

cd ${SHELL_FOLDER}/../

# start NONRTRIC containers with docker compose and configuration from docker-compose.yml
docker-compose up -d

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
checkStatus "curl -skw %{http_code} http://localhost:8091/status" "hunky dory200" "PMS"

# check ECS status
echo "check ECS status:"
checkStatus "curl -skw %{http_code} http://localhost:8083/status" '{"status":"hunky dory","no_of_producers":0,"no_of_types":0,"no_of_jobs":0}200' "ECS"

echo "NONRTRIC health check passed."
