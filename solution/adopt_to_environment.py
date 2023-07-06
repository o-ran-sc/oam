#!/usr/bin/env python
################################################################################
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

import os
import argparse

default_ip_address = 'aaa.bbb.ccc.ddd'
default_http_domain = 'smo.o-ran-sc.org'

script_name = os.path.basename(__file__)
directory_path = os.path.dirname(__file__)
file_extensions = ['.env', '.yaml', '.json']

parser = argparse.ArgumentParser(script_name)
required = parser.add_argument_group('required named arguments')
required.add_argument("-i", "--ip_address", help="The remote accessable IP address of this system.", type=str, required=True)
parser.add_argument("-d", "--http_domain", help="The http domain. Default is " + default_http_domain + ".", type=str, default=default_http_domain)
parser.add_argument("-r", "--revert", help="Reverts the previous made changes.", action='store_true')
args = parser.parse_args()

def find_replace(directory, find_text, replace_text, extensions):
    for root, dirs, files in os.walk(directory):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            file_ext = os.path.splitext(file_name)[1]
            if file_ext in extensions or file_name in extensions:
                with open(file_path, 'r') as file:
                    content = file.read()
                    if find_text in content:
                        updated_content = content.replace(find_text, replace_text)
                        with open(file_path, 'w') as file:
                            file.write(updated_content)
                        print(f"Replaced '{find_text}' with '{replace_text}' in '{file_path}'")

if args.revert == False:
    # replace ip
    find_replace(directory_path, default_ip_address, args.ip_address, file_extensions)

    # replace domain
    if not args.http_domain == default_http_domain:
      find_replace(directory_path, default_http_domain, args.http_domain, file_extensions)
else:
    # revert back ip
    find_replace(directory_path, args.ip_address, default_ip_address, file_extensions)

    # revert back domain
    if not args.http_domain == default_http_domain:
      find_replace(directory_path, args.http_domain, default_http_domain, file_extensions)
