#!/bin/bash

# Copyright 2023 highstreet technologies GmbH
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

# This script installs metric stack:
# - influxdb
# - grafana , including influxdb datasource with token and dashboard
set -x
export METRIC_NAMESPACE=metric
export APP=onap
sudo apt install jq
# reuse existing pv's
kubectl patch pv influxdb-storage-local-pv -p '{"spec":{"claimRef": null}}'
kubectl patch pv grafana-storage-local-pv -p '{"spec":{"claimRef": null}}'
# or create new pv's
kubectl apply -f metrics-pv.yaml -n $METRIC_NAMESPACE

# install influxdb
helm repo add influxdata https://helm.influxdata.com/
helm repo update
helm install $APP-influxdb2 influxdata/influxdb2 -n $METRIC_NAMESPACE --create-namespace -f influxdb-override.yaml
#echo $(kubectl get secret onap-influxdb2-auth -o "jsonpath={.data['admin-password']}" --namespace $METRIC_NAMESPACE | base64 --decode)

# wait for ready state, create and save access token in a secret
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=influxdb2 -n $METRIC_NAMESPACE
#kubectl exec -t -n $METRIC_NAMESPACE onap-influxdb2-0 -- sh -c 'influx auth create --token $DOCKER_INFLUXDB_INIT_ADMIN_TOKEN --org $DOCKER_INFLUXDB_INIT_ORG --json --all-access'
kubectl create secret generic -n $METRIC_NAMESPACE influxdb-grafana-token \
  --from-env-file <(kubectl exec -t -n $METRIC_NAMESPACE $APP-influxdb2-0 -- sh -c 'influx auth create --token $DOCKER_INFLUXDB_INIT_ADMIN_TOKEN --org $DOCKER_INFLUXDB_INIT_ORG --json --all-access'|jq -r "to_entries|map(\"\(.key)=\(.value|tostring)\")|.[]" )
# get the token
token=$(kubectl get secret -n $METRIC_NAMESPACE influxdb-grafana-token -o jsonpath='{.data.token}' |base64 -d; echo)
kubectl delete configmap -n $METRIC_NAMESPACE grafana-dashboards

# create dashboard configmap
kubectl create configmap -n $METRIC_NAMESPACE grafana-dashboards --from-file dashboards/  #pm-dashboard-oai.json
kubectl label configmap grafana-dashboards grafana_dashboard=1 -n $METRIC_NAMESPACE

# create datasource configmap
kubectl apply -f ./datasources/influxdb-datasource.yaml -n $METRIC_NAMESPACE

# and adjust grafana-override.yaml
# - ingress host url
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
GRAFANA_CHART_VERSION=8.5.1
helm install $APP-grafana grafana/grafana  --version $GRAFANA_CHART_VERSION -n $METRIC_NAMESPACE --create-namespace -f grafana-override.yaml   

# echo admin password for grafana
kubectl get secret --namespace $METRIC_NAMESPACE onap-grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo