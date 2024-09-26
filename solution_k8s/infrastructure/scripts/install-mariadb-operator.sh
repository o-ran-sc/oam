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
# mariadb-operator
SCRIPT_DIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
export $(grep -v '^#' $SCRIPT_DIR/../../.env | xargs)
MARIADB_OPERATOR_VERSION=${MARIADB_OPERATOR_VERSION:-0.28.1}
kubectl create namespace mariadb-operator
kubectl label namespace mariadb-operator istio-injection=enabled
helm repo add mariadb-operator https://mariadb-operator.github.io/mariadb-operator
helm repo update mariadb-operator
# helm install mariadb-operator --namespace mariadb-operator \
#   mariadb-operator/mariadb-operator --set ha.enabled=true  \
#   --set metrics.enabled=true --set webhook.certificate.certManager=true \
#   --version=$MARIADB_OPERATOR_VERSION

helm install mariadb-operator --namespace mariadb-operator \
  mariadb-operator/mariadb-operator   \
  --version=$MARIADB_OPERATOR_VERSION
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=mariadb-operator -n mariadb-operator --timeout=180s

#kubectl get po -n mariadb-operator -w

