#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

docker compose -f $SCRIPT_DIR/smo/common/docker-compose.yaml up -d --wait
python3 create_users.py $SCRIPT_DIR/users.csv -o $SCRIPT_DIR/smo/common/identity/authentication.json
python3 $SCRIPT_DIR/smo/common/identity/config.py
docker compose -f $SCRIPT_DIR/smo/oam/docker-compose.yaml up -d

python3 $SCRIPT_DIR/../../o-ran-deployment/generate_docker_compose_file.py \
--docker-template-path $SCRIPT_DIR/../../o-ran-deployment/docker_templates \
--network-topology-file $SCRIPT_DIR/network/o-ran-network-operational.json \
--docker-file-output-path $SCRIPT_DIR/network  \
--network-device-info-dir $SCRIPT_DIR/network



