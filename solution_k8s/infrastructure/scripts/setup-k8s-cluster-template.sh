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
export $(grep -v '^#' $SCRIPT_DIR/../../.env | xargs)
ip=$(hostname -I| cut -d" " -f 1)
read -p "VMs internal IP ($ip): " PRIVATE_IP
PRIVATE_IP=${PUBLIC_IP:-${ip}}
read -p "VMs external IP ($PRIVATE_IP): " PUBLIC_IP
export PRIVATE_IP=$PRIVATE_IP
export PUBLIC_IP=$PUBLIC_IP
export PUBLIC_IP=${PUBLIC_IP:-${PRIVATE_IP}}

envsubst < $SCRIPT_DIR/kubeone.yaml.template > $SCRIPT_DIR/../kubeone.yaml

cat $SCRIPT_DIR/../kubeone.yaml