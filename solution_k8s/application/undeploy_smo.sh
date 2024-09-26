#!/bin/bash

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

# This script undeploys smo

export NAMESPACE=onap
set -x
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

helm undeploy onap -n $NAMESPACE
for topic in $(kubectl get kafkatopic -n $NAMESPACE -o name); do   kubectl patch $topic -n $NAMESPACE --type=json -p '[{"op": "remove", "path": "/metadata/finalizers"}]'; done
sudo rm -rf /dockerdata/onap
kubectl delete ns $NAMESPACE
