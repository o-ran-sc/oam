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
Module containing a class representing a TAPI Node Edge Point
"""
import uuid
from typing import Dict, List, Union
from lxml import etree
from model.python.svg.node_edge_point import NodeEdgePoint
from model.python.tapi_connection_edge_point import TapiConnectionEdgePoint
from model.python.top import Top


class TapiNodeEdgePoint(Top):
    """
    Class representing a TAPI Node Edge Point object
    """

    __data: Dict = {}
    __configuration: Dict = {
        "parent": "unknown",
        "nodeEdgePoint": {
            "interface": "unknown-interface",
            "protocol": "unknown-protocol",
            "role": "consumer"
        }
    }
    __ceps: List[TapiConnectionEdgePoint] = []

    # constructor
    def __init__(self, configuration: dict):
        super().__init__(configuration)
        self.__configuration = configuration
        self.__ceps = []
        self.__data = {
            "uuid": str(uuid.uuid4()),
            "name": [{
                "value-name": "interface-name",
                "value": self.name()
            }],
            "administrative-state": "LOCKED",
            "operational-state": "ENABLED",
            "lifecycle-state": "INSTALLED",
            "link-port-role": "SYMMETRIC",
            "layer-protocol-name": "ETH",
            "supported-cep-layer-protocol-qualifier": [
                "tapi-dsr:DIGITAL_SIGNAL_TYPE_GigE"
            ],
            "link-port-direction": "BIDIRECTIONAL",
            "termination-state": self.termination_state(),
            "termination-direction": self.termination_direction()
        }
        for cep in configuration['nodeEdgePoint']['cep']:
            cep["parent"] = {
                "node": self.parent(),
                "node-local-id": self.local_id(),
                "node-edge-point": self.__data["uuid"],
                "interface": self.interface()
            }
            self.__ceps.append(TapiConnectionEdgePoint(cep))

    # getter
    def __x_offset_by_cep_name(self, name) -> int:
        mapping: Dict[str, int] = {
            "o2-rest-consumer": 0*self.FONTSIZE,
            "a1-rest-consumer": 0*self.FONTSIZE,
            "oam-netconf-consumer": 0*self.FONTSIZE,
            "o1-ves-provider": 0*self.FONTSIZE,
            "o1-file-consumer": 0*self.FONTSIZE,

            "o2-rest-provider": 0*self.FONTSIZE,
            "a1-rest-provider": 0*self.FONTSIZE,
            "e2-rest-consumer": 0*self.FONTSIZE,

            "f1-c-unknown-consumer": 0*self.FONTSIZE,
            "f1-u-unknown-consumer": 0*self.FONTSIZE,

            "e1-unknown-provider": +2.5*self.FONTSIZE,
            "e1-unknown-consumer": -2.5*self.FONTSIZE,

            "e2-rest-provider": 0*self.FONTSIZE,
            "f1-c-unknown-provider": 0*self.FONTSIZE,
            "f1-u-unknown-provider": 0*self.FONTSIZE,
            "f1-unknown-provider": 0*self.FONTSIZE,
            "o1-netconf-provider": -4*self.FONTSIZE,
            "o1-ves-consumer": 0*self.FONTSIZE,
            "o1-file-provider": +4*self.FONTSIZE,
            "ofh-netconf-consumer": 0*self.FONTSIZE,

            "eth-ofh-provider": 0*self.FONTSIZE,
            "oam-netconf-provider": 0*self.FONTSIZE,
            "eth-ofh-consumer": 0*self.FONTSIZE,

            "ofh-netconf-provider": 0*self.FONTSIZE,
            "uu-unknown-provider": 0*self.FONTSIZE,

            "uu-unknown-consumer": 0*self.FONTSIZE
        }
        if name in mapping:
            return mapping[name]

        print(" NEP: CEP name", name, "for x postion calculation not found")
        return 0

    def __y_offset_by_cep_name(self, name: str) -> int:
        mapping: Dict[str, int] = {
            "o2-rest-consumer": -1.5*self.FONTSIZE,
            "a1-rest-consumer": -1.5*self.FONTSIZE,
            "oam-netconf-consumer": -1.5*self.FONTSIZE,
            "o1-ves-provider": -1.5*self.FONTSIZE,
            "o1-file-consumer": -1.5*self.FONTSIZE,

            "o2-rest-provider": +1.5*self.FONTSIZE,
            "a1-rest-provider": +1.5*self.FONTSIZE,
            "e2-rest-consumer": -1.5*self.FONTSIZE,

            "e1-unknown-provider": 0*self.FONTSIZE,
            "e1-unknown-consumer": 0*self.FONTSIZE,

            "f1-c-unknown-consumer": -1.5*self.FONTSIZE,
            "f1-u-unknown-consumer": -1.5*self.FONTSIZE,

            "e2-rest-provider": +1.5*self.FONTSIZE,
            "f1-c-unknown-provider": +1.5*self.FONTSIZE,
            "f1-u-unknown-provider": +1.5*self.FONTSIZE,
            "f1-unknown-provider": +1.5*self.FONTSIZE,
            "o1-netconf-provider": +1.5*self.FONTSIZE,
            "o1-ves-consumer": +1.5*self.FONTSIZE,
            "o1-file-provider": +1.5*self.FONTSIZE,
            "ofh-netconf-consumer": -1.5*self.FONTSIZE,

            "eth-ofh-provider": +1.5*self.FONTSIZE,
            "oam-netconf-provider": +1.5*self.FONTSIZE,
            "eth-ofh-consumer": -1.5*self.FONTSIZE,

            "ofh-netconf-provider": +1.5*self.FONTSIZE,
            "uu-unknown-provider": -1.5*self.FONTSIZE,

            "uu-unknown-consumer": +1.5*self.FONTSIZE
        }
        if name in mapping:
            return mapping[name]

        print(" NEP: CEP name", name, "for y postion calculation not found")
        return 0

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
        result = self.__data.copy()
        result['tapi-connectivity:cep-list'] = {}
        result['tapi-connectivity:cep-list']['connection-end-point'] = []
        for cep in self.connection_edge_points():
            result['tapi-connectivity:cep-list']['connection-end-point'].append(
                cep.json())
        return result

    def local_id(self) -> int:
        if "local-id" in self.configuration()["nodeEdgePoint"]:
            return self.configuration()["nodeEdgePoint"]["local-id"]
        return 0

    def name(self) -> str:
        """
        Getter a human readable identifier of the TAPI Node Edge Point.
        :return TAPI Node Edge Point name as String.
        """
        result = self.interface().lower()
        if "local-id" in self.configuration()["nodeEdgePoint"]:
            result = "#".join(
                [result, str(self.configuration()["nodeEdgePoint"]["local-id"])])
        return result

    def interface(self) -> str:
        """
        Getter a human readable identifier of the TAPI Node Edge Point interface.
        :return Interface label.
        """
        return self.__configuration['nodeEdgePoint']['interface'].lower()

    def connection_edge_points(self) -> List[TapiConnectionEdgePoint]:
        """
        Getter a human readable identifier of the TAPI Node Edge Point interface.
        :return Interface label.
        """
        return self.__ceps

    def parent(self) -> str:
        """
        Getter returning the identifier the the TAPI Node hosting the Node
        Edge Point.
        :return Identifier of the TAPI Node containing this NEP.
        """
        return self.__configuration["parent"]

    def svg_x(self) -> int:
        return self.__svg_x

    def svg_y(self) -> int:
        return self.__svg_y

    def svg(self, x: int, y: int) -> etree.Element:
        """
        Getter for a xml Element object representing the TAPI Node Edge Point.
        :return TAPI Node Edge Point as SVG object.
        """
        self.__svg_x = x
        self.__svg_y = y

        svg_nep = NodeEdgePoint(self, x, y)
        group: etree.Element = svg_nep.svg_element()

        for cep in self.connection_edge_points():
            cep_x = x + self.__x_offset_by_cep_name(cep.name())
            cep_y = y + self.__y_offset_by_cep_name(cep.name())
            group.append(cep.svg(cep_x, cep_y))
        return group

    def termination_direction(self) -> str:
        """
        Getter returning the TAPI Node Edge Point direction.
        :return TAPI Node Edge Point direction as String.
        """
        value = "BIDIRECTIONAL"
        mapping = {
            "consumer": "SINK",
            "provider": "SOURCE"
        }
        if self.__configuration['nodeEdgePoint']['cep'][0]['role'].lower() in mapping:
            return mapping[self.__configuration['nodeEdgePoint']['cep'][0]['role'].lower()]
        return value

    def termination_state(self) -> str:
        """
        Getter returning the TAPI Node Edge Point state.
        :return TAPI Node Edge Point state as String.
        """
        return "LT_PERMENANTLY_TERMINATED"
