################################################################################
# Copyright 2025 highstreet technologies USA Corp.
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

#!/usr/bin/env python3

import os
import socket
import netifaces
import argparse
from jinja2 import Template

default_interface = "eth0"
default_ip_address = 'aaa.bbb.ccc.ddd'
default_http_domain = 'smo.o-ran-sc.org'

script_name = os.path.basename(__file__)
directory_path = os.path.dirname(__file__)
file_extensions = ['.env', '.yaml', '.json']

parser = argparse.ArgumentParser(script_name)
required = parser.add_argument_group('required named arguments')
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
                try:
                    with open(file_path, 'r') as file:
                        content = file.read()
                        if find_text in content:
                            updated_content = content.replace(find_text, replace_text)
                            with open(file_path, 'w') as file:
                                file.write(updated_content)
                            print(f"Replaced '{find_text}' with '{replace_text}' in '{file_path}'")
                except PermissionError:
                    # Ignore or handle as you wish:
                    # e.g., just print a warning or do nothing
                    # print(f"Warning: Could not open {file_path} for writing (permission denied).")
                    pass

def create_etc_hosts(ip_address_v4: str, http_domain: str ) -> None:
    """
    creates skelton for /etc/hosts and writes to local file
    @param ip_address: ipv4 address of the system
    @param http_domain: base domain name for the deployment
    """
    template_str = """
# SMO OAM development system
{{ deployment_system_ipv4 }}                   {{ http_domain }}
{{ deployment_system_ipv4 }}           gateway.{{ http_domain }}
{{ deployment_system_ipv4 }}          identity.{{ http_domain }}
{{ deployment_system_ipv4 }}          messages.{{ http_domain }}
{{ deployment_system_ipv4 }}      kafka-bridge.{{ http_domain }}
{{ deployment_system_ipv4 }}          kafka-ui.{{ http_domain }}
{{ deployment_system_ipv4 }}         odlux.oam.{{ http_domain }}
{{ deployment_system_ipv4 }}         flows.oam.{{ http_domain }}
{{ deployment_system_ipv4 }}         tests.oam.{{ http_domain }}
{{ deployment_system_ipv4 }}    controller.dcn.{{ http_domain }}
{{ deployment_system_ipv4 }} ves-collector.dcn.{{ http_domain }}

"""
    template = Template(template_str)
    hosts_entries: str = template.render(deployment_system_ipv4=ip_address_v4,
                                         http_domain=http_domain)
    output_txt_path = f"{directory_path}/append_to_etc_hosts.txt"
    with open(output_txt_path, 'w', encoding="utf-8") as f:
        f.write(hosts_entries)
    print(f"Entries for /etc/hosts: {output_txt_path}")

def get_default_interface():
    """Return the name of the default interface for IPv4 traffic."""
    gws = netifaces.gateways()
    # gws['default'] might look like {AF_INET: ('192.168.1.1', 'eth0')}
    if 'default' in gws and netifaces.AF_INET in gws['default']:
        # The tuple is (gateway_ip, interface_name)
        _, interface = gws['default'][netifaces.AF_INET]
        return interface
    return None

def get_interface_ipv4_addr(interface):
    """Return the IPv4 address for a specified interface using netifaces."""
    addrs = netifaces.ifaddresses(interface)
    if netifaces.AF_INET in addrs:
        return addrs[netifaces.AF_INET][0].get('addr')
    return None

if __name__ == "__main__":
    interface = get_default_interface()
    print("Default interface:", interface)

    if interface:
        ip_address = get_interface_ipv4_addr(interface)
        print("IPv4 on default interface:", ip_address)

        if args.revert == False:
            # replace interface
            find_replace(directory_path, default_interface, interface, file_extensions)

            # replace ip
            find_replace(directory_path, default_ip_address, ip_address, file_extensions)

            # replace domain
            if not args.http_domain == default_http_domain:
                find_replace(directory_path, default_http_domain, args.http_domain, file_extensions)

            # write append file for etc/hosts
            create_etc_hosts(ip_address_v4=ip_address, http_domain=args.http_domain)

        else:
            # revert back interface
            find_replace(directory_path, interface, default_interface, file_extensions)

            # revert back ip
            find_replace(directory_path, ip_address, default_ip_address, file_extensions)

            # revert back domain
            if not args.http_domain == default_http_domain:
                find_replace(directory_path, args.http_domain, default_http_domain, file_extensions)
