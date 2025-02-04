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

# docker-tester/Dockerfile
FROM python:3.9-slim

# 1. Install libpcap for Scapy sniffing, and tcpdump for debugging
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpcap-dev tcpdump iproute2 \
 && rm -rf /var/lib/apt/lists/*

# 2. Install Scapy
RUN pip install scapy

WORKDIR /app

# 3. Copy your test script
COPY test_dhcp.py .

# 4. Copy a small entrypoint script
COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Make the entrypoint script run by default
ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]

# We won't specify CMD here, so it can remain empty or be overridden
