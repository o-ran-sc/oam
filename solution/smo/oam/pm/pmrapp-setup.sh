#!/bin/bash

#  ============LICENSE_START===============================================
#  Copyright (C) 2023 Nordix Foundation. All rights reserved.
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
#

. scripts/get_influxdb2_token.sh
. scripts/populate_keycloak.sh

print_usage() {
    echo "Usage: pmrapp-setup.sh"
    exit 1
}

check_error() {
    if [ $1 -ne 0 ]; then
        echo "Failed $2"
        echo "Exiting..."
        exit 1
    fi
}

setup_init() {
echo "Cleaning previously started containers..."
./pmrapp-tear-down.sh
}

check_images(){
export PMRAPP_IMAGE="pm-rapp:latest"
}

create_topic() {
TOPIC="pmreports"
retcode=1
rt=43200000
echo "Creating topic $TOPIC with retention $(($rt/1000)) seconds"
while [ $retcode -ne 0 ]; do
    cmd_output=$(docker exec -it kafka ./bin/kafka-topics.sh \
	    --create --topic $TOPIC --config retention.ms=$rt  --bootstrap-server kafka:9092)
    retcode=$?
    test_string="Topic 'pmreports' already exists"
    if [[ $cmd_output == *${test_string}* ]]; then
      echo $test_string
      retcode=0
    fi
done
}

setup_pmrapp() {
create_topic

cid="pm-rapp"
create_clients nonrtric-realm $cid
check_error $?
generate_client_secrets nonrtric-realm $cid
check_error $?

export PMRAPP_CLIENT_SECRET=$(< .sec_nonrtric-realm_$cid)
envsubst < docker-compose-pmrapp.yaml > docker-compose-pmrapp_gen.yaml
docker compose -p pmrapp -f docker-compose-pmrapp_gen.yaml up -d
}
## Main ##
setup_init

check_images

setup_pmrapp
check_error $?
