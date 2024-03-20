#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
docker compose -f $SCRIPT_DIR/smo/oam/docker-compose.yaml down
docker compose -f $SCRIPT_DIR/smo/common/docker-compose.yaml down
