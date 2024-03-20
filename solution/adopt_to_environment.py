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
from jinja2 import Template

default_ip_address = 'aaa.bbb.ccc.ddd'
default_http_domain = 'smo.o-ran-sc.org'

script_name = os.path.basename(__file__)
directory_path = os.path.dirname(__file__)
file_extensions = ['.env', '.yaml', '.json']

parser = argparse.ArgumentParser(script_name)
required = parser.add_argument_group('required named arguments')
required.add_argument("-i", "--ip_address", help="The remote accessable IP address of this system.",
                      type=str, required=True)
parser.add_argument("-d", "--http_domain", help="The http domain. Default is " +
                    default_http_domain + ".",
                    type=str, default=default_http_domain)
parser.add_argument("-r", "--revert", help="Reverts the previous made changes.",
                    action='store_true')
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
def create_etc_hosts(ip_adress_v4: str, http_domain: str ) -> None:
    """
    creates scelaton for /etc/hosts and writes to local file
    @param ip_adress: ipv4 address of the system
    @param http_domain: base domain name for the deployment
    """
    template_str = """
# SMO OAM development system
{{ deployment_system_ipv4 }}                   {{ http_domain }}
{{ deployment_system_ipv4 }}           gateway.{{ http_domain }}
{{ deployment_system_ipv4 }}          identity.{{ http_domain }}
{{ deployment_system_ipv4 }}          messages.{{ http_domain }}
{{ deployment_system_ipv4 }}      kafka-bridge.{{ http_domain }}
{{ deployment_system_ipv4 }}         odlux.oam.{{ http_domain }}
{{ deployment_system_ipv4 }}         flows.oam.{{ http_domain }}
{{ deployment_system_ipv4 }}         tests.oam.{{ http_domain }}
{{ deployment_system_ipv4 }}    controller.dcn.{{ http_domain }}
{{ deployment_system_ipv4 }} ves-collector.dcn.{{ http_domain }}

"""
    template = Template(template_str)
    hosts_entries: str = template.render(deployment_system_ipv4=ip_adress_v4,
                                         http_domain=http_domain)
    output_txt_path = f"{directory_path}/append_to_etc_hosts.txt"
    with open(output_txt_path, 'w', encoding="utf-8") as f:
        f.write(hosts_entries)
    print(f"/etc/hosts entries created: {output_txt_path}")

if args.revert == False:
    # replace ip
    find_replace(directory_path, default_ip_address, args.ip_address, file_extensions)

    # replace domain
    if not args.http_domain == default_http_domain:
        find_replace(directory_path, default_http_domain, args.http_domain, file_extensions)
    # write append file for etc/hosts
    create_etc_hosts(ip_adress_v4=args.ip_address, http_domain=args.http_domain)
else:
    # revert back ip
    find_replace(directory_path, args.ip_address, default_ip_address, file_extensions)

    # revert back domain
    if not args.http_domain == default_http_domain:
        find_replace(directory_path, args.http_domain, default_http_domain, file_extensions)

