#!/bin/sh
#
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
# This script runs test_dhcp.py once, prints the result, then keeps
# the container alive (by tailing /dev/null). That way you can
# debug inside the container if needed.

echo "[+] Starting DHCP test..."
python3 /app/test_dhcp.py

echo "[+] Test script finished. Container will remain running for debugging..."
echo "    You can run 'docker exec -it dhcp-tester bash' (or sh) to explore."

# Keep the container alive indefinitely
tail -f /dev/null
