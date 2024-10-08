#!/bin/sh

# Copyright 2024 highstreet technologies
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

SCRIPT_DIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
echo $SCRIPT_DIR
export $(grep -v '^#' $SCRIPT_DIR/../.env | xargs)
export PUBLIC_IP=${PUBLIC_IP:-${PRIVATE_IP}}
read -p "FQDN of the server (${HTTP_DOMAIN}): " DOMAIN
export DOMAIN=${DOMAIN:-${HTTP_DOMAIN}}
echo "Create SMO override file: $SCRIPT_DIR/override/onap-override-o-ran-sc-${ONAP_VERSION}.yaml"
envsubst < $SCRIPT_DIR/override/onap-override-o-ran-sc-${ONAP_VERSION}.yaml.template > $SCRIPT_DIR/override/onap-override-o-ran-sc-${ONAP_VERSION}.yaml
echo "Create grafana override file: $SCRIPT_DIR/../metrics/grafana-override.yaml"
envsubst < $SCRIPT_DIR/../metrics/grafana-override.yaml.template > $SCRIPT_DIR/../metrics/grafana-override.yaml

	