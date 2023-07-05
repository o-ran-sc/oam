#!/usr/bin/env python
################################################################################
# Copyright 2021 highstreet technologies GmbH
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

################################################################################
# A selection of common methods

import datetime
import json
import requests
import os
import socket
import sys
import yaml
from pathlib import Path
from _datetime import timezone

def sendVesEvent(data):
    url = data['config']['vesEndpoint']['url']
    username = data['config']['vesEndpoint']['username']
    password = data['config']['vesEndpoint']['password']
    headers = {'content-type': 'application/json'}
    verify = data['config']['vesEndpoint']['verify']
    try:
      response = requests.post(url, json=data['body'], auth=(
          username, password), headers=headers, verify=verify)
    except requests.exceptions.Timeout:
      sys.exit('HTTP request failed, please check you internet connection.')
    except requests.exceptions.TooManyRedirects:
      sys.exit('HTTP request failed, please check your proxy settings.')
    except requests.exceptions.RequestException as e:
      # catastrophic error. bail.
      raise SystemExit(e)

    if response.status_code >= 200 and response.status_code <= 300:
      print(response)
    else:
      print(response.status_code)
      sys.exit('Sending VES "stndDefined" message template failed with code %d.' % response.status_code)

def sendHttpGet(url):
    try:
      response = requests.get(url)
    except requests.exceptions.Timeout:
      sys.exit('HTTP request failed, please check you internet connection.')
    except requests.exceptions.TooManyRedirects:
      sys.exit('HTTP request failed, please check your proxy settings.')
    except requests.exceptions.RequestException as e:
      # catastrophic error. bail.
      raise SystemExit(e)

    if response.status_code >= 200 and response.status_code < 300:
      return response.json()
    else:
      sys.exit('Reading VES "stndDefined" message template failed.')

def getInitData(domain, stndBody=''):
  currentTime = datetime.datetime.now(tz=timezone.utc)
  dir = os.path.dirname(os.path.realpath(__file__))

  result = {}
  result['domain']= domain
  result['directory']= dir
  result['outdir']= dir + '/json/examples'
  result['fqdn']= socket.getfqdn()
  result['timestamp']= int(currentTime.timestamp()*1000000)
  result['eventTime']= currentTime.isoformat() + 'Z'
  result['interface']= "urn:ietf:params:xml:ns:yang:ietf-interfaces:interfaces/interface/name='O-RAN-SC-OAM'"

  # Read config
  with open('config.yaml', 'r') as stream:
    try:
        result['config']= yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

  # Read template body
  if domain == 'stndDefined':
    url = 'https://raw.githubusercontent.com/onap/testsuite/master/robot/assets/dcae/ves_stdnDefined_' + stndBody + '.json'
    result['body']= sendHttpGet(url)
  else:
    templateFileName = dir + '/json/templates/' + domain + '.json'
    with open(templateFileName) as f:
      result['body']= json.load(f)
  
  Path(result["outdir"]).mkdir(parents=True, exist_ok=True)
  return result

def saveExample(data):
  if 'directory' in data and 'domain' in data and 'body' in data:
    name = data['domain']
    if 'pnfId' in data: name = '-'.join( (data['pnfId'], data['domain']) )
    outputFileName = data['directory'] + '/json/examples/' + name + '.json'
    with open(outputFileName, 'w') as f:
      json.dump(data['body'], f, indent=2, sort_keys=True)
  else:
    print("Example could not been saved:\n" + json.dump(data, f, indent=2, sort_keys=True))
