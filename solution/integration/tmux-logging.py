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

from libtmux import Pane, Server, Window, exc
from libtmux.common import has_gte_version

def createLoggingWindow():
  logging = session.new_window(attach=False, window_name="logging")
  sdnr = logging.list_panes()[0]
  sdnr.send_keys('echo "sdnr"', enter=True)
  sdnr.send_keys('docker exec -it sdnr tail -f /opt/opendaylight/data/log/karaf.log', enter=True)

  ntsim = logging.split_window(attach=False, vertical=True)
  ntsim.send_keys('echo "ntsim"', enter=True)
  ntsim.send_keys('docker exec -it ntsim-ng-o-du-1122 tail -f /opt/dev/ntsim-ng/log/log.txt', enter=True)

  ves = logging.split_window(attach=False, vertical=False)
  ves.send_keys('echo "ves"', enter=True)
  ves.send_keys('docker logs -f ves-collector', enter=True)

  env = ntsim.split_window(attach=False, vertical=False)
  env.send_keys('htop', enter=True)

# main
server = Server()
session = server.find_where({ "session_name": "integration" })

workspace = session.select_window("workspace")
pane = workspace.list_panes()[0]
# pane.send_keys('clear', enter=True)
pane.send_keys('cat README.md', enter=True)
pane.send_keys('docker ps -a', enter=True)

# create logging window, if needed
logging = session.find_where({'window_name':'logging'})
if logging is None:
  createLoggingWindow()
