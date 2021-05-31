#!/bin/bash

#  ============LICENSE_START===============================================
#  Copyright (C) 2021 Nordix Foundation. All rights reserved.
#  ========================================================================
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#  ============LICENSE_END=================================================

unset http_proxy https_proxy
SHELL_FOLDER=$(cd "$(dirname "$0")";pwd)

cd ${SHELL_FOLDER}
git clone https://gerrit.o-ran-sc.org/r/nonrtric
cd nonrtric
git reset --hard origin/master
git pull origin master

# build o-ru application image
cd ${SHELL_FOLDER}/nonrtric/test/usecases/oruclosedlooprecovery/scriptversion/app/
docker build -t oru-app .

# build simulator image of sdnr
cd ${SHELL_FOLDER}/nonrtric/test/usecases/oruclosedlooprecovery/scriptversion/simulators/
docker build -f Dockerfile-sdnr-sim -t sdnr-simulator .

# build message generator image
docker build -f Dockerfile-message-generator -t message-generator .
