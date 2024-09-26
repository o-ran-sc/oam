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

# This script uninstalls metric stack:
# - influxdb
# - grafana , including influxdb datasource with token and dashboard
set -x
export METRIC_NAMESPACE=metric
export APP=onap
helm uninstall $APP-grafana  -n $METRIC_NAMESPACE

# patch pv to resuse persisistent volume and data
kubectl patch pv grafana-storage-local-pv -p '{"spec":{"claimRef": null}}'
# or delete pv and directory
kubectl delete pv  grafana-storage-local-pv
sudo rm -rf /dockerdata-nfs/grafana/

helm uninstall $APP-influxdb2  -n $METRIC_NAMESPACE
kubectl delete secret -n $METRIC_NAMESPACE influxdb-grafana-token
kubectl delete pvc onap-influxdb2 -n $METRIC_NAMESPACE
kubectl delete pv  influxdb-storage-local-pv
sudo rm -rf /dockerdata-nfs/influxdb/