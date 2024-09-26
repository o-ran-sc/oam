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
helm repo add strimzi https://strimzi.io/charts/
export $(grep -v '^#' $SCRIPT_DIR/../../.env | xargs)
export STRIMZI_VERSION=${STRIMZI_VERSION:-0.41.0}
STRIMZI_NAMESPACE=strimzi-system
helm install strimzi-kafka-operator strimzi/strimzi-kafka-operator --namespace strimzi-system --version $STRIMZI_VERSION --set watchAnyNamespace=true --create-namespace
kubectl wait --for=condition=ready pod -l name=strimzi-cluster-operator -n $STRIMZI_NAMESPACE --timeout=180s
#kubectl get po -n strimzi-system -w