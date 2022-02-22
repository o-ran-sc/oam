# Copyright 2022 highstreet technologies GmbH
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

#!/usr/bin/python
"""
Module containing a class representing an O-RAN Radio Unit as TAPI Node.
"""
from model.python.tapi_node import TapiNode
from model.python.tapi_node_edge_point import TapiNodeEdgePoint


class TapiNodeFronthaulGateway(TapiNode):
    """
    Class representing a O-RAN Fronthaul Gateway as TAPI Node.
    """

    # constructor
    def __init__(self, parent, configuration):
        super().__init__(parent, configuration)

        count = max(2, configuration["node"]["southbound-nep-count"])
        super().width((count + 1) * (2*self.FONTSIZE))

        # add Ethernet Northbound provider
        nep_configuration = {
            "parent": self.identifier(),
            "nodeEdgePoint": {
                "interface": "eth", "cep": [{"protocol": "ofh", "role": "provider"}]
            }
        }
        self.add(TapiNodeEdgePoint(nep_configuration))

        # add OAM provider
        nep_configuration = {
            "parent": self.identifier(),
            "nodeEdgePoint": {
                "interface": "oam", "cep": [{"protocol": "netconf", "role": "provider"}]
            }
        }
        self.add(TapiNodeEdgePoint(nep_configuration))

        # add Ethernet Southbound consumer
        for nep_index in range(configuration["node"]["southbound-nep-count"]):
            nep_configuration = {
                "parent": self.identifier(),
                "nodeEdgePoint": {
                    "local-id": nep_index,
                    "interface": "eth",
                    "cep": [{"protocol": "ofh", "role": "consumer"}]
                }
            }
            self.add(TapiNodeEdgePoint(nep_configuration))
