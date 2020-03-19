#!/bin/bash
################################################################################
#
# Copyright 2020 highstreet technologies GmbH and others
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

################################################################################
# Script to request interfaces from ONAP SDN-R

# import settings
. x-ran-ru-swm-config;

# send HTTP-GET Software Inventory
curl $auth -H "Content-Type: application/json" -H "Accept: application/json" $urlInventory --compressed | python -m json.tool

# send HTTP-POST Software Download
curl $auth -H "Content-Type: application/json" -H "Accept: application/json" $urlDownload -d @x-ran-ru-swm-software-download.json --compressed | python -m json.tool

# send HTTP-POST Software Install
curl $auth -H "Content-Type: application/json" -H "Accept: application/json" $urlInstall  -d @x-ran-ru-swm-software-install.json  --compressed | python -m json.tool

# send HTTP-POST Software Activate
curl $auth -H "Content-Type: application/json" -H "Accept: application/json" $urlActivate -d @x-ran-ru-swm-software-activate.json --compressed | python -m json.tool
