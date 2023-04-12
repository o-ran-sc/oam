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
import pathlib
import sys
import json
import time
import getpass
import requests
import warnings
from jproperties import Properties
from typing import List
warnings.filterwarnings('ignore', message='Unverified HTTPS request')
# global configurations


def get_environment_variable(name):
    configs = Properties()
    path = pathlib.Path( os.path.dirname(os.path.abspath(__file__)) )
    env_file = str(path.parent.absolute()) + '/.env'
    with open(env_file, "rb") as read_prop:
        configs.load(read_prop)
    return configs.get(name).data


def load_arguments(args: List[str]) -> tuple:
    realm_file = os.path.dirname(os.path.abspath(
        __file__)) + '/o-ran-sc-realm.json'
    auth_file = os.path.dirname(os.path.abspath(
        __file__)) + '/authentication.json'
    ready_timeout = 180
    args.pop(0)
    while len(args) > 0:
        arg = args.pop(0)
        if arg == '--auth' and len(args) > 0:
            auth_file = args.pop(0)
            print('overwriting auth file: {}'.format(auth_file))
        elif arg == '--realm' and len(args) > 0:
            realm_file = args.pop(0)
            print('overwriting realm file: {}'.format(realm_file))
        elif arg == '--timeout' and len(args) > 0:
            ready_timeout = int(args.pop(0))
            print('waiting for ready {} seconds'.format(ready_timeout))

    return (realm_file, auth_file, ready_timeout)


def isReady(timeoutSeconds=180):
    url = getBaseUrl();
    while timeoutSeconds > 0:
        try:
            response = requests.get(url, verify=False, headers={})
        except:
            pass
        if response is not None and response.status_code == 200:
            return True
        time.sleep(1)
        timeoutSeconds -= 1
    return False


def getBaseUrl():
    return get_environment_variable("IDENTITY_PROVIDER_URL")

# Request a token for further communication
def getToken():
    url = base + '/realms/master/protocol/openid-connect/token'
    headers = {
        'content-type': 'application/x-www-form-urlencoded',
        'accept': 'application/json'
    }
    body = {
        'client_id': 'admin-cli',
        'grant_type': 'password',
        'username': username,
        'password': password
    }
    try:
        response = requests.post(url, verify=False, auth=(
            username, password), data=body, headers=headers)
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
    url = base + '/admin/realms'
    auth = 'bearer ' + token
    headers = {
        'content-type': 'application/json',
        'accept': 'application/json',
        'authorization': auth
    }
    try:
        response = requests.post(
            url, verify=False, json=realm, headers=headers)
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
    url = base + '/admin/realms/' + realmId
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


def createUser(token, realmConfig, user):
    realmId = realmConfig['id']
    url = base + '/admin/realms/' + realmId + '/users'
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


def createUsers(token, realmConfig, authConfig):
    for user in authConfig['users']:
        createUser(token, realmConfig, user)

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
                "temporary": True
            }
      ],
      "requiredActions": [
        "UPDATE_PASSWORD"
      ]
    }
    createUser(token, realmConfig, systemUser)

# Grants a role to a user


def addUserRole(user: dict, role: dict, options: dict):
    url = options['url'] + '/' + user['id'] + '/role-mappings/realm'
    try:
        response = requests.post(url, verify=False, json=[
                                 {'id': role['id'], 'name':role['name']}], headers=options['headers'])
    except requests.exceptions.Timeout:
        sys.exit('HTTP request failed, please check you internet connection.')
    except requests.exceptions.TooManyRedirects:
        sys.exit('HTTP request failed, please check your proxy settings.')
    except requests.exceptions.RequestException as e:
        # catastrophic error. bail.
        raise SystemExit(e)

    if response.status_code >= 200 and response.status_code < 300:
        print('User role', user['username'], role['name'], 'created!')
    else:
        print('Creation of user role',
              user['username'], role['name'], 'failed!\n', response.text)

# searches for the role of a given user

def findRole(username: str, authConfig: dict, realmConfig: dict) -> dict:
    roleName = 'administration'
    for grant in authConfig['grants']:
        if grant['username'] == username:
            roleName = grant['role']
    for role in realmConfig['roles']['realm']:
        if role['name'] == roleName:
            return role
    return None

# adds roles to users


def addUserRoles(token, realmConfig, authConfig):
    realmId = realmConfig['id']
    url = base + '/admin/realms/' + realmId + '/users'
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
            role = findRole(user['username'], authConfig, realmConfig)
            addUserRole(user, role, options)
    else:
        sys.exit('Getting users failed.')

# main


(realmFile, authFile, readyTimeout) = load_arguments(sys.argv)
username = get_environment_variable('ADMIN_USERNAME')
password = get_environment_variable('ADMIN_PASSWORD')
base = getBaseUrl()
isReady(readyTimeout)
token = getToken()
if token:
    with open(realmFile) as file:
        realmConfig = json.load(file)
        if not checkRealmExists(token, realmConfig['id']):
            createRealm(token, realmConfig)

        with open(authFile) as authConfig:
            authConfig = json.load(authConfig)
            createUsers(token, realmConfig, authConfig)
        addUserRoles(token, realmConfig, authConfig)
    exit(0)
exit(1)
