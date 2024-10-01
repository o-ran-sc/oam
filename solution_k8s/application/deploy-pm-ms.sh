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

# This script installs pm metric microservice. This service 
# - converts stddefined file ready messages to legacy ves file readymessage and publishs to kafka
# - get 3GPP pm data from kafka topics and publishs to influxdb
set -x
export METRIC_NAMESPACE=onap
influxdbpass=$(kubectl get secret -n metric onap-influxdb2-auth -o jsonpath='{.data.admin-password}' | base64 -d)
influxdbtoken=$(kubectl get secret -n metric onap-influxdb2-auth -o jsonpath='{.data.admin-token}' | base64 -d)
cd helm
helm install -n $METRIC_NAMESPACE pm-metric-service pm-metric-service --set .Values.config.influxDB.password=$influxdbpass,.Values.config.influxDB.toke=$influxdbtoken
