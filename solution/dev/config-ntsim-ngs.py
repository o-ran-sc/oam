#!/usr/bin/env python
################################################################################
# Copyright 2021 highstreet technologies GmbH
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# importing the sys, json, requests library
import os
import sys
import json
import requests
import subprocess

dockerFilter = subprocess.check_output("docker ps --format '{{.Names}}'", shell=True)
containers = dockerFilter.splitlines()

mapping = dict({"ntsim-ng-o-ru": "highstreet-O-RU", "ntsim-ng-o-du": "highstreet-O-DU"}) 
base = 'http://localhost:8181'
username = 'admin'
password = 'Kp8bJ4SXszM0WXlhak3eHlcse2gAw84vaoGGmJvUy2U'

# REST to set event settings
def configEventSettings(nfName, nfType):
  file = os.path.dirname(os.path.abspath(__file__)) + '/' + nfType + '/event-settings.json'
  with open(file) as json_file:
    body = json.load(json_file)
    url = base + '/rests/data/network-topology:network-topology/topology=topology-netconf/node=' + nfName + '/yang-ext:mount/nts-network-function:simulation/network-function'
    headers = {
        'content-type': 'application/yang-data+json',
        'accept': 'application/yang-data+json'
    }
    try:
      response = requests.put(url, verify=False, auth=(username, password), json=body, headers=headers)
    except requests.exceptions.Timeout:
      sys.exit('HTTP request failed, please check you internet connection.')
    except requests.exceptions.TooManyRedirects:
      sys.exit('HTTP request failed, please check your proxy settings.')
    except requests.exceptions.RequestException as e:
      # catastrophic error. bail.
      raise SystemExit(e)

    return response.status_code >= 200 and response.status_code < 300

# main
for container in containers:
  name = container.decode("utf-8")
  if "ntsim-ng" in name:
    if "ntsim-ng-o-ru" in name:
      nfName = mapping["ntsim-ng-o-ru"] + name[name.rindex("-"):]
      print("Set", nfName, configEventSettings(nfName, "ntsim-ng-o-ru"))
    if "ntsim-ng-o-du" in name:
      nfName = mapping["ntsim-ng-o-du"] + name[name.rindex("-"):]
      print("Set", nfName, configEventSettings(nfName, "ntsim-ng-o-du"))
