#!/usr/bin/env python
################################################################################
# Copyright 2021 highstreet technologies GmbH
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
#

################################################################################
# Send a VES event for domain 'notification'

# importing the datetime, json, requests, os socket and yaml library
import datetime
import json
import requests
import os
import socket
import yaml
from pathlib import Path

# Globals
dir = os.path.dirname(os.path.realpath(__file__))
domain = "heartbeat"
fqdn = socket.getfqdn()

# time formats
currentTime = datetime.datetime.utcnow()
timestamp = int(currentTime.timestamp()*1000000)
eventTime = currentTime.isoformat() + "Z"

# Create output path
Path(dir + "/json/examples").mkdir(parents=True, exist_ok=True)

# Read settings
with open("config.yml", 'r') as stream:
    try:
        cfg = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

print("################################################################################")
print("# send SDN-Controller " + domain)

# Read template body
templateFileName = dir + "/json/templates/" + domain + ".json"
with open(templateFileName) as f:
    data = json.load(f)

data["event"]["commonEventHeader"]["domain"] = domain
data["event"]["commonEventHeader"]["eventId"] = fqdn + "_" + eventTime
data["event"]["commonEventHeader"]["eventName"] = domain + \
    "_" + cfg["settings"]["eventType"]
data["event"]["commonEventHeader"]["eventType"] = cfg["settings"]["eventType"]
data["event"]["commonEventHeader"]["sequence"] = cfg["settings"]["sequence"]
data["event"]["commonEventHeader"]["reportingEntityName"] = fqdn
data["event"]["commonEventHeader"]["sourceName"] = fqdn
data["event"]["commonEventHeader"]["startEpochMicrosec"] = timestamp
data["event"]["commonEventHeader"]["lastEpochMicrosec"] = timestamp
data["event"]["commonEventHeader"]["nfNamingCode"] = "SDN-Controller"
data["event"]["commonEventHeader"]["nfVendorName"] = "O-RAN-SC OAM"

data["event"]["heartbeatFields"]["additionalFields"]["eventTime"] = eventTime

# save example body
outputFileName = dir + "/json/examples/" + domain + ".json"
with open(outputFileName, 'w') as f:
    json.dump(data, f, indent=2, sort_keys=True)

# Send VES Event
url = cfg["vesEndpoint"]["url"]
username = cfg["vesEndpoint"]["username"]
password = cfg["vesEndpoint"]["password"]
verify = cfg["vesEndpoint"]["verify"]
response = requests.post(url, json=data, auth=(username, password), verify=verify)
print(response)
