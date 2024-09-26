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


set -o xtrace
SCRIPT_DIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
export $(grep -v '^#' $SCRIPT_DIR/../../.env | xargs)
helm_version=${HELM_VERSION:-3.13.1}
echo $SCRIPT_DIR

if [ -z ${1+x} ]; 
then 
  echo "helm version is unset, set to $helm_version"
else 
  echo "helm version is set to '$1'"
  helm_version=$1 
fi

# chartmuseum installation
curl https://raw.githubusercontent.com/helm/chartmuseum/main/scripts/get-chartmuseum | bash
mkdir -p ~/helm3-storage
nohup chartmuseum --storage local --storage-local-rootdir ~/helm3-storage -port 8879 > chartmuseum.log &



wget https://get.helm.sh/helm-v$helm_version-linux-amd64.tar.gz
tar -zxvf helm-v$helm_version-linux-amd64.tar.gz
sudo mv linux-amd64/helm /usr/local/bin/helm
rm https://get.helm.sh/helm-v$helm_version-linux-amd64.tar.gz*
rm -rf linux-amd64

helm plugin install https://github.com/chartmuseum/helm-push.git
helm plugin install $SCRIPT_DIR/plugins/deploy
helm plugin install $SCRIPT_DIR/plugins/undeploy
helm plugin list

helm repo add local http://127.0.0.1:8879
helm repo list