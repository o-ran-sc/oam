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

# This script deploys smo with tailored override file for SMO in O-RAN-SC from onap helm repo
 
set -x
SCRIPT_DIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
export $(grep -v '^#' $SCRIPT_DIR/../../.env | xargs)
ONAP_VERSION=${ONAP_VERSION:-14.0.0}

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
override_file=$SCRIPT_DIR/override/onap-override-o-ran-sc-$ONAP_VERSION.yaml

if [ -z ${1+x} ]; then
  echo "override file is unset, set to '$override_file'";
else
  echo "override file is set to '$1'"; override_file=$1
fi

kubectl apply -f maria-db-pv.yaml

helm repo add onap-release https://nexus3.onap.org/repository/onap-helm-release/
# use onap-testing as long not in release repo
helm repo add onap-testing https://nexus3.onap.org/repository/onap-helm-testing/
helm repo update
helm deploy onap onap-testing/onap --namespace onap --create-namespace --version $ONAP_VERSION -f $override_file --timeout 900s --debug

