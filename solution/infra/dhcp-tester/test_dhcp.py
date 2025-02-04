#!/usr/bin/env python3

################################################################################
# Copyright 2025 highstreet technologies
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
"""
Scapy-based DHCP test script with Option 43 parsing.

Sends DHCPDISCOVER, waits for DHCPOFFER, extracts vendor-specific Option 43 data,
and prints all relevant information.
"""

from scapy.all import Ether, IP, UDP, BOOTP, DHCP, sendp, sniff, AsyncSniffer
import time
import sys

# Mapping of Option 43 sub-option types
OPTION_43_TYPES = {
    0x81: "Controller IP Address",
    0x82: "Controller FQDN",
    0x83: "Event Collector IP Address",
    0x84: "Event Collector FQDN",
    0x85: "PNF Registration Format",
    0x86: "NETCONF Call Home"
}

def parse_option_43(raw_bytes):
    """Parses vendor-encapsulated Option 43 data."""
    index = 0
    parsed_data = {}

    while index < len(raw_bytes):
        if index + 2 > len(raw_bytes):
            print("[!] Malformed Option 43 data (truncated)")
            break

        opt_type = raw_bytes[index]  # First byte is the sub-option type
        opt_len = raw_bytes[index + 1]  # Second byte is the length

        if index + 2 + opt_len > len(raw_bytes):
            print(f"[!] Skipping invalid Option 43 sub-option {opt_type:#04x} (bad length)")
            break

        opt_value = raw_bytes[index + 2: index + 2 + opt_len]  # Value field

        if opt_type in [0x81, 0x83]:  # IP Address (4 bytes)
            if opt_len == 4:
                parsed_value = ".".join(str(b) for b in opt_value)
            else:
                parsed_value = f"Invalid IP length ({opt_len})"
        
        elif opt_type in [0x82, 0x84]:  # FQDN (ASCII string)
            try:
                parsed_value = opt_value.decode("ascii")
            except UnicodeDecodeError:
                parsed_value = opt_value.hex()  # Fallback to hex if not ASCII

        elif opt_type in [0x85, 0x86]:  # Single-byte flags
            parsed_value = int(opt_value[0]) if opt_len == 1 else f"Invalid flag length ({opt_len})"
        
        else:
            parsed_value = opt_value.hex()  # Unknown types are printed in hex

        parsed_data[OPTION_43_TYPES.get(opt_type, f"Unknown Type {opt_type:#04x}")] = parsed_value

        index += 2 + opt_len  # Move to the next sub-option

    return parsed_data

def print_dhcp_options(dhcp_options):
    """Print all DHCP options from a list of (option, value) tuples."""
    for opt in dhcp_options:
        if isinstance(opt, tuple):
            if opt[0] == "vendor_specific":  # Fix: Use the correct Scapy name for Option 43
                print("    Option 43 (Vendor-Specific Information):")
                parsed_43 = parse_option_43(opt[1])  # Convert raw bytes
                for k, v in parsed_43.items():
                    print(f"        {k}: {v}")
            else:
                print(f"    Option {opt[0]}: {opt[1]}")

def handle_packet(pkt):
    """Callback to process incoming DHCP packets and detect DHCPOFFER."""
    if DHCP in pkt:
        dhcp_opts = pkt[DHCP].options
        for opt in dhcp_opts:
            if isinstance(opt, tuple) and opt[0] == "message-type":
                if opt[1] in [2, "offer"]:  # DHCPOFFER detected
                    server_ip = pkt[IP].src
                    offered_ip = pkt[BOOTP].yiaddr
                    print(f"[+] Received DHCPOFFER from {server_ip}")
                    print(f"    Offered IP: {offered_ip}")
                    print("    Full DHCP options:")
                    print_dhcp_options(dhcp_opts)
                    return True
    return False

def test_dhcp():
    # Start sniffing in *async* mode so we don't block.
    sniff_thread = AsyncSniffer(
        iface="eth0",
        filter="udp and (port 67 or port 68)",
        prn=handle_packet
    )
    sniff_thread.start()

    time.sleep(1)  # Give it a moment to get ready

    # Now send DHCPDISCOVER
    discover = (
        Ether(src="02:50:02:99:00:01", dst="ff:ff:ff:ff:ff:ff")
        / IP(src="0.0.0.0", dst="255.255.255.255")
        / UDP(sport=68, dport=67)
        / BOOTP(chaddr=b'\x02\x50\x02\x99\x00\x01', xid=0x99999999, flags=0x8000)
        / DHCP(options=[
            ("message-type", "discover"),
            ("parameter-request-list", [43]),  # Explicitly request Option 43
            ("vendor_class_id", "o-ran-ru2/pynts"),  # Option 60
            "end"
        ])
    )
    print("[*] Sending DHCPDISCOVER...")
    sendp(discover, iface="eth0", verbose=False)

    print("[*] Sniffing for 5 seconds...")
    time.sleep(5)

    sniff_thread.stop()
    results = sniff_thread.results
    print(f"[+] Captured {len(results)} packets in total")

    for pkt in results:
        if handle_packet(pkt):
            print("[+] Test SUCCESS - Received a valid DHCPOFFER.")
            sys.exit(0)  # Exit with success code 0

    print("[-] Test FAILED - No DHCPOFFER received.")
    sys.exit(1)  # Exit with failure code 1

if __name__ == "__main__":
    test_dhcp()
