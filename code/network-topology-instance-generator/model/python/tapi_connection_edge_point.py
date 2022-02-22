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
Module containing a class representing a TAPI Connection Node Edge Point
"""
import uuid
from typing import Dict, Union
from lxml import etree
from model.python.svg.connection_edge_point import ConnectionEdgePoint
from model.python.svg.svg import Svg
from model.python.top import Top


class TapiConnectionEdgePoint(Top):
    """
    Class representing a TAPI Connection Node Edge Point object
    """

    __data: Dict = {}
    __configuration = {
        "protocol": "unknown",
        "role": "consumer",
        "parent": {
            "node": "unknown",
            "node-edge-point": "unknown",
            "interface": "unknown"
        }
    }

    # constructor
    def __init__(self, configuration: Dict[str, str]):
        super().__init__(configuration)
        self.__configuration = configuration
        self.__data = {
            "uuid": str(uuid.uuid4()),
            "name": [{
                "value-name": "connection-edge-point-name",
                "value": self.name()
            }],
            "operational-state": "ENABLED",
            "lifecycle-state": "INSTALLED",
            "termination-state": self.termination_state(),
            "termination-direction": self.termination_direction(),
            "layer-protocol-name": "ETH",
            "layer-protocol-qualifier": self.protocol(),

            "connection-port-role": "SYMMETRIC",
            "connection-port-direction": "BIDIRECTIONAL",

            "parent-node-edge-point": {
                #  TODO              "topology-uuid": "?",
                "node-uuid": self.parent()["node"],
                "node-edge-point-uuid": self.parent()["node-edge-point"]
            }
        }

    # getter
    def configuration(self) -> dict:
        """
        Getter for a json object representing the TAPI Node Edge Point intiail
        configuration.
        :return TAPI Node Edge Point configuration as json object.
        """
        return self.__configuration

    def data(self) -> dict:
        """
        Getter for a json object representing the TAPI Node Edge Point.
        :return TAPI Node Edge Point as json object.
        """
        return self.__data

    def identifier(self) -> str:
        """
        Getter returning the TAPI Node Edge Point identifier.
        :return Object identifier as UUID.
        """
        return self.__data["uuid"]

    def json(self) -> dict:
        """
        Getter for a json object representing the TAPI Node Edge Point.
        :return TAPI Node Edge Point as json object.
        """
        return self.data()

    def name(self) -> str:
        """
        Getter a human readable identifier of the TAPI Node Edge Point.
        :return TAPI Node Edge Point name as String.
        """
        items = (self.parent()["interface"],
                 self.protocol().split(":")[1],
                 self.role())
        return "-".join(items).lower()

    def protocol(self) -> str:
        """
        Getter a human readable identifier of the TAPI Connection Edge Point protocol.
        :return protocol label.
        """
        protocol = self.__configuration['protocol'].lower()
        if protocol == "otf":
            protocol = "fronthaul-gateway"
        return ":".join(["o-ran-sc-topology-common", self.__configuration['protocol'].lower()])

    def role(self) -> str:
        """
        Getter a human readable identifier of the TAPI Node Edge Point role.
        :return role label.
        """
        return self.__configuration['role'].lower()

    def parent(self) -> Dict:
        """
        Getter returning the identifier the the TAPI Node hosting the Node
        Edge Point.
        :return Identifier of the TAPI Node containing this NEP.
        """
        return self.__configuration["parent"]

    def svg(self, x: int, y: int) -> etree.Element:
        """
        Getter for a xml Element object representing the TAPI Node Edge Point.
        :return TAPI Node Edge Point as SVG object.
        """
        return ConnectionEdgePoint(self, x, y).svg_element()

    def termination_direction(self) -> str:
        """
        Getter returning the TAPI Node Edge Point direction.
        :return TAPI Node Edge Point direction as String.
        """
        mapping = {
            "consumer": "SINK",
            "provider": "SOURCE"
        }
        if self.__configuration['role'].lower() in mapping:
            return mapping[self.__configuration['role'].lower()]
        return "BIDIRECTIONAL"

    def termination_state(self) -> str:
        """
        Getter returning the TAPI Node Edge Point state.
        :return TAPI Node Edge Point state as String.
        """
        return "LT_PERMENANTLY_TERMINATED"
