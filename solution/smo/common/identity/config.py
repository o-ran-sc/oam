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
from sqlite3 import TimeFromTicks
from jproperties import Properties
import os
import sys
import json
import time
import re
import requests
import getpass
import warnings
from typing import List

warnings.filterwarnings('ignore', message='Unverified HTTPS request')


# global configurations
def get_env(name):
    configs = Properties()
    envFile = os.path.dirname(os.path.abspath(__file__)) + '/' + '../' + '.env'

    with open(envFile, "rb") as read_prop:
        configs.load(read_prop)
    value = configs.get(name).data

    regex = r"\$\{([^\}]+)\}"
    matches = re.finditer(regex, value)
    while True:
        match = next(matches, None)
        if match is None:
            break
        inner = get_env(match.group(1))
        value = value.replace("${" + match.group(1) + "}", inner)
    return value


def loadArgs(args: List[str]) -> tuple:
    realmFile = os.path.dirname(os.path.abspath(__file__)) + '/o-ran-sc-realm.json'
    authFile = os.path.dirname(os.path.abspath(__file__)) + '/authentication.json'
    readyTimeout = 180
    args.pop(0)
    while len(args) > 0:
        arg = args.pop(0)
        if arg == '--auth' and len(args) > 0:
            authFile = args.pop(0)
            print('overwriting auth file: {}'.format(authFile))
        elif arg == '--realm' and len(args) > 0:
            realmFile = args.pop(0)
            print('overwriting realm file: {}'.format(realmFile))
        elif arg == '--timeout' and len(args) > 0:
            readyTimeout = int(args.pop(0))
            print('waiting for ready {} seconds'.format(readyTimeout))

    return (realmFile, authFile, readyTimeout)


def isReady(timeoutSeconds=180):
    url = getBaseUrl()
    print(url)
    response = None
    print("waiting for ready state", end='')
    while timeoutSeconds > 0:
        try:
            response = requests.get(url, verify=False, headers={})
            print(response)
        except:
            pass
        if response is not None and response.status_code == 200:
            print('succeeded')
            return True
        time.sleep(1)
        timeoutSeconds -= 1
        print('.', end='', flush=True)
    return False


def getBaseUrl():
    try:
        if get_env("USE_LOCAL_HOST_FOR_IDENTITY_CONFIG").strip("'\"") == "true":
            return get_env("IDENTITY_PROVIDER_URL_LOCAL_HOST")
    except AttributeError:
        print("Using IDENTITY_PROVIDER_URL")
    return get_env("IDENTITY_PROVIDER_URL")


# Request a token for futher communication
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
    url = base + '/admin/realms'
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
                "temporary": False
            }
        ]
    }
    createUser(token, realmConfig, systemUser)


# Grants a role to a user
def addUserRole(user: dict, role: list, options: dict):
    url = options['url'] + '/' + user['id'] + '/role-mappings/realm'
    try:
        for irole in role:
            response = requests.post(url, verify=False, json=[{'id': irole['id'], 'name': irole['name']}],
                                     headers=options['headers'])
            if response.status_code >= 200 and response.status_code < 300:
                print('User role', user['username'], irole['name'], 'created!')
            else:
                print('Creation of user role', user['username'], irole['name'], 'failed!\n', response.text)
    except requests.exceptions.Timeout:
        sys.exit('HTTP request failed, please check you internet connection.')
    except requests.exceptions.TooManyRedirects:
        sys.exit('HTTP request failed, please check your proxy settings.')
    except requests.exceptions.RequestException as e:
        # catastrophic error. bail.
        raise SystemExit(e)


# searches for the role of a given user
def findRole(username: str, authConfig: dict, realmConfig: dict) -> dict:
    roleList = []
    roleNames = []
    roleName = 'administration'
    for grant in authConfig['grants']:
        if grant['username'] == username:
            roleName = grant['role']
            roleNames = roleName.split(",")  # A user can have multiple roles, comma separated
    for iroleName in roleNames:
        for role in realmConfig['roles']['realm']:
            if role['name'] == iroleName:
                roleList.append(role)
    return roleList


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

(realmFile, authFile, readyTimeout) = loadArgs(sys.argv)
username = get_env('ADMIN_USERNAME')
password = get_env('ADMIN_PASSWORD')
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
