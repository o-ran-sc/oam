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
import getpass

# global configurations
# TODO: read from ../.env
base = 'http://localhost:8081'
username = 'admin'
password = 'Kp8bJ4SXszM0WXlhak3eHlcse2gAw84vaoGGmJvUy2U'
realmFile = os.path.dirname(os.path.abspath(__file__)) + '/o-ran-sc-realm.json'
authFile = os.path.dirname(os.path.abspath(__file__)) + '/authentication.json'

# Request a token for futher communication
def getToken():
    url = base + '/auth/realms/master/protocol/openid-connect/token'
    headers = {
        'content-type': 'application/x-www-form-urlencoded',
        'accept': 'application/json'
    }
    body = {
      'client_id':'admin-cli',
      'grant_type': 'password',
      'username': username,
      'password': password
    }
    try:
      response = requests.post(url, verify=False, auth=(username, password), data=body, headers=headers)
    except requests.exceptions.Timeout:
      sys.exit('HTTP request failed, please check you internet connection.')
    except requests.exceptions.TooManyRedirects:
      sys.exit('HTTP request failed, please check your proxy settings.')
    except requests.exceptions.RequestException as e:
      # catastrophic error. bail.
      raise SystemExit(e)

    if response.status_code >= 200 and response.status_code < 300:
      print('Got token!')
      return response.json()['access_token']
    else:
      sys.exit('Getting token failed.')

# create the default realm from file
def createRealm(token, realm):
  url = base + '/auth/admin/realms'
  auth = 'bearer ' + token
  headers = {
      'content-type': 'application/json',
      'accept': 'application/json',
      'authorization': auth
  }
  try:
    response = requests.post(url, verify=False, json=realm, headers=headers)
  except requests.exceptions.Timeout:
    sys.exit('HTTP request failed, please check you internet connection.')
  except requests.exceptions.TooManyRedirects:
    sys.exit('HTTP request failed, please check your proxy settings.')
  except requests.exceptions.RequestException as e:
    # catastrophic error. bail.
    raise SystemExit(e)

  return response.status_code >= 200 and response.status_code < 300

# Check if default realm exists
def checkRealmExists(token, realmId):
  url = base + '/auth/admin/realms/' + realmId
  auth = 'bearer ' + token
  headers = {
      'accept': 'application/json',
      'authorization': auth
  }
  try:
      response = requests.get(url, verify=False, headers=headers)
  except requests.exceptions.Timeout:
      sys.exit('HTTP request failed, please check you internet connection.')
  except requests.exceptions.TooManyRedirects:
      sys.exit('HTTP request failed, please check your proxy settings.')
  except requests.exceptions.RequestException as e:
      # catastrophic error. bail.
      raise SystemExit(e)

  if response.status_code >= 200 and response.status_code < 300:
    return realmId == response.json()['id']
  else:
    # sys.exit('Getting realm failed.')
    return False

# create a user in default realm
def createUser(token, realmId, user):
  url = base + '/auth/admin/realms/' + realmId + '/users'
  auth = 'bearer ' + token
  headers = {
      'accept': 'application/json',
      'authorization': auth
  }
  try:
    response = requests.post(url, verify=False, json=user, headers=headers)
  except requests.exceptions.Timeout:
    sys.exit('HTTP request failed, please check you internet connection.')
  except requests.exceptions.TooManyRedirects:
    sys.exit('HTTP request failed, please check your proxy settings.')
  except requests.exceptions.RequestException as e:
    # catastrophic error. bail.
    raise SystemExit(e)

  if response.status_code >= 200 and response.status_code < 300:
    print('User', user['username'], 'created!')
  else:
    print('User creation', user['username'], 'failed!\n', response.text)

# creates User accounts in realm based a file
def createUsers(token, realm, authConfig):
  for user in authConfig['users']:
    createUser(token, realm, user)
  
  # create a user based on system user
  systemUser = {
    "firstName": getpass.getuser(),
    "lastName": "",
    "email": getpass.getuser() + "@sdnr.onap.org",
    "enabled": "true",
    "username": getpass.getuser(),
    "credentials": [
      {
        "type": "password",
        "value": password,
        "temporary": False
      }
    ]
  }
  createUser(token, realm, systemUser)

# Grants a role to a user
def addUserRole(user, role, options):
  url = options['url'] + '/' + user['id'] + '/role-mappings/realm'
  try:
    response = requests.post(url, verify=False, json=role, headers=options['headers'])
  except requests.exceptions.Timeout:
    sys.exit('HTTP request failed, please check you internet connection.')
  except requests.exceptions.TooManyRedirects:
    sys.exit('HTTP request failed, please check your proxy settings.')
  except requests.exceptions.RequestException as e:
    # catastrophic error. bail.
    raise SystemExit(e)

  if response.status_code >= 200 and response.status_code < 300:
    print('User role', user['username'], role[0]['name'], 'created!')
  else:
    print('Creation of user role', user['username'], role[0]['name'], 'failed!\n', response.text)

# searches for the role of a given user
def findRole(user, authConfig):
  roleName='administration'
  for grant in authConfig['grants']:
    if grant['username'] == user:
      roleName= grant['role']
  role=authConfig['roles'][roleName]
  return role

# adds roles to users
def addUserRoles(token, realmId, authConfig):
  url = base + '/auth/admin/realms/' + realmId + '/users'
  auth = 'bearer ' + token
  headers = {
      'content-type': 'application/json',
      'accept': 'application/json',
      'authorization': auth
  }
  try:
      response = requests.get(url, verify=False, headers=headers)
  except requests.exceptions.Timeout:
      sys.exit('HTTP request failed, please check you internet connection.')
  except requests.exceptions.TooManyRedirects:
      sys.exit('HTTP request failed, please check your proxy settings.')
  except requests.exceptions.RequestException as e:
      # catastrophic error. bail.
      raise SystemExit(e)

  if response.status_code >= 200 and response.status_code < 300:
    users = response.json()
    options = {
      "url": url,
      "auth": auth,
      "headers": headers
    }
    for user in users:
      role=findRole(user['username'], authConfig)
      addUserRole(user, role, options)
  else:
    sys.exit('Getting users failed.')

# main
token = getToken()
if token:
  with open(realmFile) as file:
    realm = json.load(file)
    if not checkRealmExists(token, realm['id']):
      createRealm(token, realm)

    with open(authFile) as authConfig:
      auth = json.load(authConfig)
      createUsers(token, realm['id'], auth);
    addUserRoles(token, realm['id'], auth)
