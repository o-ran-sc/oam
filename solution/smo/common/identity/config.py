#!/usr/bin/env python
#############################################################################
# Copyright 2023 highstreet technologies GmbH
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
import argparse
import os
import pathlib
import sys
import json
import time
import getpass
import requests
import warnings
from dotenv import load_dotenv
from requests import Response

warnings.filterwarnings('ignore', message='Unverified HTTPS request')


class IdentityConfig:
    ENV_FILE_NAME: str = '.env'

    def __init__(self, auth_file: str, realm_file: str, ready_timeout: int = 180):
        self.ready_timeout: int = ready_timeout
        self.auth_config: dict = self.__load_json_file(auth_file)
        self.realm_config: dict = self.__load_json_file(realm_file)
        self.env_file_path: str = self.__get_env_file_path()
        load_dotenv(self.env_file_path)
        self.identity_provider_url: str = os.getenv('IDENTITY_PROVIDER_URL')
        self.admin_username: str = os.getenv('ADMIN_USERNAME')
        self.admin_password: str = os.getenv('ADMIN_PASSWORD')
        self.users_url: str = f'{self.identity_provider_url}/admin/realms/{self.realm_config["id"]}/users'
        self.session: requests.Session = self.__create_session()

    @staticmethod
    def __load_json_file(file_path: str) -> dict:
        with open(file_path) as file:
            return json.load(file)

    @staticmethod
    def __get_env_file_path():
        path = pathlib.Path(os.path.dirname(os.path.abspath(__file__)))
        return f'{path.parent.absolute()}/.env'

    def __check_for_ready(self, timeout_in_seconds) -> bool:
        while timeout_in_seconds > 0:
            try:
                response = requests.get(self.identity_provider_url, verify=False)
            except:
                response = None
            if response is not None and response.status_code == 200:
                return True
            time.sleep(1)
            timeout_in_seconds -= 1
        return False

    def __create_session(self) -> requests.Session:
        print('Checking if identity provider is ready...')
        if self.__check_for_ready(self.ready_timeout):
            print('Identity provider is ready!')
            session = requests.Session()
            session.verify = False
            session.headers = {
                'content-type': 'application/json',
                'accept': 'application/json',
                'authorization': f'bearer {self.__get_token()}'
            }
            return session
        else:
            sys.exit('Identity provider is not ready. Exiting...')

    def __get_token(self) -> str:
        url = f'{self.identity_provider_url}/realms/master/protocol/openid-connect/token'
        headers: dict = {
            'content-type': 'application/x-www-form-urlencoded',
            'accept': 'application/json'
        }
        body: dict = {
            'client_id': 'admin-cli',
            'grant_type': 'password',
            'username': os.getenv('ADMIN_USERNAME'),
            'password': os.getenv('ADMIN_PASSWORD')
        }
        try:
            response = requests.post(url, verify=False, auth=(self.admin_username, self.admin_password), data=body,
                                     headers=headers)
        except requests.exceptions.Timeout:
            sys.exit('HTTP request failed, please check you internet connection.')
        except requests.exceptions.TooManyRedirects:
            sys.exit('HTTP request failed, please check your proxy settings.')
        except requests.exceptions.RequestException as e:
            # catastrophic error. bail.
            raise SystemExit(e)
        if 200 <= response.status_code < 300:
            print('Got token!')
            return response.json()['access_token']
        else:
            sys.exit('Getting token failed.')

    def __check_realm_exists(self) -> bool:
        realm_id: int = self.realm_config['id']
        url: str = f'{self.identity_provider_url}/admin/realms/{realm_id}'
        try:
            response: Response = self.session.get(url)
        except requests.exceptions.Timeout:
            sys.exit('HTTP request failed, please check you internet connection.')
        except requests.exceptions.TooManyRedirects:
            sys.exit('HTTP request failed, please check your proxy settings.')
        except requests.exceptions.RequestException as e:
            # catastrophic error. bail.
            raise SystemExit(e)
        if 200 <= response.status_code < 300:
            return realm_id == response.json()['id']
        else:
            return False

    def create_realm(self):
        if self.__check_realm_exists():
            print('Realm already exists! Skipping creation...')
        else:
            try:
                response: Response = self.session.post(f'{self.identity_provider_url}/admin/realms', verify=False,
                                                       json=self.realm_config)
            except requests.exceptions.Timeout:
                sys.exit('HTTP request failed, please check you internet connection.')
            except requests.exceptions.TooManyRedirects:
                sys.exit('HTTP request failed, please check your proxy settings.')
            except requests.exceptions.RequestException as e:
                # catastrophic error. bail.
                raise SystemExit(e)
            response.raise_for_status()

    def create_users(self):
        for user in self.auth_config['users']:
            self.__create_user(user)
            # create a user based on system user
        system_user: dict = {
            "firstName": getpass.getuser(),
            "lastName": "",
            "email": getpass.getuser() + "@sdnr.onap.org",
            "enabled": "true",
            "username": getpass.getuser(),
            "credentials": [
                {
                    "type": "password",
                    "value": self.admin_password,
                    "temporary": True
                }
            ],
            "requiredActions": [
                "UPDATE_PASSWORD"
            ]
        }
        self.__create_user(system_user)

    def __create_user(self, user: dict):
        if self.__check_user_exists(user):
            print('User', user['username'], 'already exists. Updating...')
            self.__update_user(user)
        else:
            try:
                response: Response = self.session.post(self.users_url, json=user)
            except requests.exceptions.Timeout:
                sys.exit('HTTP request failed, please check you internet connection.')
            except requests.exceptions.TooManyRedirects:
                sys.exit('HTTP request failed, please check your proxy settings.')
            except requests.exceptions.RequestException as e:
                # catastrophic error. bail.
                raise SystemExit(e)
            try:
                response.raise_for_status()
                print('User', user['username'], 'created!')
            except requests.exceptions.HTTPError:
                print('User creation', user['username'], 'failed!\n', response.text)

    def __check_user_exists(self, user: dict) -> bool:
        return len(self.__get_user_details(user)) > 0

    def __get_user_details(self, user: dict) -> dict:
        return self.session.get(self.users_url, params={'username': user['username']}).json()

    def __update_user(self, user: dict):
        url: str = f'{self.users_url}/{self.__get_user_details(user)[0]["id"]}'
        self.session.put(url, json=user).raise_for_status()

    def add_user_roles(self):
        try:
            response: Response = self.session.get(self.users_url)
        except requests.exceptions.Timeout:
            sys.exit('HTTP request failed, please check you internet connection.')
        except requests.exceptions.TooManyRedirects:
            sys.exit('HTTP request failed, please check your proxy settings.')
        except requests.exceptions.RequestException as e:
            # catastrophic error. bail.
            raise SystemExit(e)
        try:
            response.raise_for_status()
            users = response.json()
            for user in users:
                role = self.__find_role(user['username'])
                self.__add_user_role(user, role)
        except requests.exceptions.HTTPError:
            sys.exit('Getting users failed.')

    def __find_role(self, username: str) -> dict | None:
        role_name: str = 'administration'
        for grant in self.auth_config['grants']:
            if grant['username'] == username:
                role_name = grant['role']
        for role in self.realm_config['roles']['realm']:
            if role['name'] == role_name:
                return role
        return None

    def __add_user_role(self, user: dict, role: dict):
        url: str = f'{self.users_url}/{user["id"]}/role-mappings/realm'
        try:
            response: Response = self.session.post(url, json=[{'id': role['id'], 'name': role['name']}])
        except requests.exceptions.Timeout:
            sys.exit('HTTP request failed, please check you internet connection.')
        except requests.exceptions.TooManyRedirects:
            sys.exit('HTTP request failed, please check your proxy settings.')
        except requests.exceptions.RequestException as e:
            # catastrophic error. bail.
            raise SystemExit(e)
        try:
            response.raise_for_status()
            print('User role', user['username'], role['name'], 'created!')
        except requests.exceptions.HTTPError:
            print('Creation of user role', user['username'], role['name'], 'failed!\n', response.text)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--auth', type=str, required=False,
                        default=f'{os.path.dirname(os.path.abspath(__file__))}/authentication.json',
                        help='Authentication file path')
    parser.add_argument('--realm', type=str, required=False,
                        default=f'{os.path.dirname(os.path.abspath(__file__))}/o-ran-sc-realm.json',
                        help='Realm file path')
    parser.add_argument('--timeout', type=int, required=False, default=180, help='Timeout in seconds')
    args = parser.parse_args()
    identity_config: IdentityConfig = IdentityConfig(args.auth, args.realm, args.timeout)

    identity_config.create_realm()
    identity_config.create_users()
    identity_config.add_user_roles()