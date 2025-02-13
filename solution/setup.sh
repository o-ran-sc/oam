################################################################################
# Copyright 2025 highstreet technologies USA Corp.
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

#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

cat /etc/os-release | grep PRETTY_NAME
docker --version
docker compose version
python3 --version

docker compose -f $SCRIPT_DIR/infra/docker-compose.yaml up -d
docker compose -f $SCRIPT_DIR/smo/common/docker-compose.yaml up -d
python3 $SCRIPT_DIR/smo/common/identity/config.py
docker compose -f $SCRIPT_DIR/smo/oam/docker-compose.yaml up -d
# docker compose -f $SCRIPT_DIR/smo/apps/docker-compose.yaml up -d

# simulated network - once manually build
# docker compose -f network/docker-compose.yaml up -d
# docker compose -f network/docker-compose.yaml restart pynts-o-du-o1




