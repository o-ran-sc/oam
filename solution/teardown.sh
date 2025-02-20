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

docker compose -f $SCRIPT_DIR/network/docker-compose.yaml down
docker compose -f $SCRIPT_DIR/smo/apps/docker-compose.yaml down
docker compose -f $SCRIPT_DIR/smo/oam/docker-compose.yaml down
docker compose -f $SCRIPT_DIR/smo/common/docker-compose.yaml down
docker compose -f $SCRIPT_DIR/infra/docker-compose.yaml down
