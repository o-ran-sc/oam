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
Module containing the class for a TAPI Node.
"""
import uuid
from typing import Dict
from lxml import etree
from model.python.svg.near_tr_ric import NearRtRic
from model.python.svg.amf import Amf
from model.python.svg.o_cloud import OCloud
from model.python.svg.o_cu_cp import OCuCp
from model.python.svg.o_cu_up import OCuUp
from model.python.svg.o_du import ODu
from model.python.svg.ue import Ue
from model.python.svg.fronthaul_gateway import FronthaulGateway
from model.python.svg.node import Node
from model.python.tapi_node_edge_point import TapiNodeEdgePoint
from model.python.top import Top


class TapiNode(Top):
    """
    Class representing a TAPI Node.
    """

    __data: dict = {}
    __configuration: dict = {}
    __parent: 'TapiNode' = None
    __width: int = 0  # default SVG width, should be overritten by constructor

    # constructor
    def __init__(self, parent: 'TapiNode', configuration: dict):
        super().__init__(configuration)
        self.__parent = parent
        self.__configuration = configuration
        self.width((4 + 1) * (2.2*self.FONTSIZE))  # 4x nep
        self.__data = {
            "uuid": str(uuid.uuid4()),
            "name": [
                {
                    "value-name": "topology-node-name",
                    "value": self.name()
                },
                {
                    "value-name": "topology-node-local-id",
                    "value": configuration['node']['localId']
                }
            ],
            "owned-node-edge-point": [],
            "administrative-state": "LOCKED",
            "operational-state": "ENABLED",
            "lifecycle-state": "INSTALLED",
            "layer-protocol-name": ["ETH"],
            "cost-characteristic": [
                {
                    "cost-name": "cost",
                    "cost-algorithm": "alg1",
                    "cost-value": "value-1"
                }
            ],
            "latency-characteristic": [{
                "traffic-property-name": "property-1",
                "queing-latency-characteristic": "queue-1",
                "fixed-latency-characteristic": "latency-1",
                "jitter-characteristic": "jitter-1",
                "wander-characteristic": "wander-1"
            }],
            "o-ran-sc-topology:function": configuration['node']['function'],
            "o-ran-sc-topology:geolocation": {
                "longitude": "0",
                "latitude": "0",
                "altitude": "20000"
            }
        }

    # getter
    def x_offset_by_cep_name(self, name: str, local_id: int) -> int:
        cep_of_interest = len(self.data()['owned-node-edge-point'])-2
        mapping: Dict[str, int] = {
            "o2-rest-consumer": -4*6*self.FONTSIZE,
            "a1-rest-consumer": -2*6*self.FONTSIZE,
            "oam-netconf-consumer": -0*6*self.FONTSIZE,
            "o1-ves-provider": 2*6*self.FONTSIZE,
            "o1-file-consumer": 4*6*self.FONTSIZE,

            "o2-rest-provider": 0*self.FONTSIZE,
            "a1-rest-provider": -8*self.FONTSIZE,
            "e2-rest-consumer": 0*self.FONTSIZE,

            "n1-nas-provider": -2*self.FONTSIZE,
            "n2-nas-provider": +2*self.FONTSIZE,
            "n3-nas-provider": 0*self.FONTSIZE,

            "f1-c-unknown-consumer": 0*self.FONTSIZE,
            "f1-u-unknown-consumer": 0*self.FONTSIZE,

            "e1-unknown-provider": -5*2*self.FONTSIZE,
            "e1-unknown-consumer": 5*2*self.FONTSIZE,

            "e2-rest-provider": -4*2*self.FONTSIZE,
            "n2-nas-consumer": -2*2*self.FONTSIZE,
            "n3-nas-consumer": -2*2*self.FONTSIZE,
            "f1-c-unknown-provider": -2*2*self.FONTSIZE,
            "f1-u-unknown-provider": 2*2*self.FONTSIZE,
            "f1-unknown-provider": -2*2*self.FONTSIZE,
            "o1-netconf-provider": 4*self.FONTSIZE,
            "o1-ves-consumer": 8*self.FONTSIZE,
            "o1-file-provider": 12*self.FONTSIZE,
            "ofh-netconf-consumer": -2*self.FONTSIZE,

            "eth-ofh-provider": -2*self.FONTSIZE,
            "oam-netconf-provider": 2*self.FONTSIZE,
            #            "eth-ofh-consumer": -(len(self.data()['owned-node-edg
            # e-point']) - 2)/2 * 2 * self.FONTSIZE,
            "eth-ofh-consumer": 0-(cep_of_interest/2)*4*self.FONTSIZE + 2*self.FONTSIZE,

            "ofh-netconf-provider": 0*self.FONTSIZE,
            "uu-radio-provider": 0*self.FONTSIZE,

            "uu-radio-consumer": -2*self.FONTSIZE,
            "n1-nas-consumer":2*self.FONTSIZE
        }
        if name in mapping:
            return mapping[name] + 4*self.FONTSIZE * local_id

        print("Node: CEP name", name, "for x postion calculation not found")
        return 0

    def y_offset_by_cep_name(self, name: str) -> int:
        mapping: Dict[str, int] = {
            "o2-rest-consumer": 3*self.FONTSIZE,
            "a1-rest-consumer": 3*self.FONTSIZE,
            "oam-netconf-consumer": 3*self.FONTSIZE,
            "o1-ves-provider": 3*self.FONTSIZE,
            "o1-file-consumer": 3*self.FONTSIZE,

            "o2-rest-provider": -3*self.FONTSIZE,
            "a1-rest-provider": -3*self.FONTSIZE,
            "e2-rest-consumer": 3*self.FONTSIZE,

            "n1-nas-provider": 3*self.FONTSIZE,
            "n2-nas-provider": 3*self.FONTSIZE,
            "n3-nas-provider": 3*self.FONTSIZE,

            "e1-unknown-provider": 1*self.FONTSIZE,
            "e1-unknown-consumer": 1*self.FONTSIZE,

            "f1-c-unknown-consumer": 3*self.FONTSIZE,
            "f1-u-unknown-consumer": 3*self.FONTSIZE,
            "f1-unknown-consumer": 3*self.FONTSIZE,

            "e2-rest-provider": -3*self.FONTSIZE,
            "n2-nas-consumer": -3*self.FONTSIZE,
            "n3-nas-consumer": -3*self.FONTSIZE,
            "f1-c-unknown-provider": -3*self.FONTSIZE,
            "f1-u-unknown-provider": -3*self.FONTSIZE,
            "f1-unknown-provider": -3*self.FONTSIZE,
            "o1-netconf-provider": -3*self.FONTSIZE,
            "o1-ves-consumer": -3*self.FONTSIZE,
            "o1-file-provider": -3*self.FONTSIZE,
            "ofh-netconf-consumer": 3*self.FONTSIZE,

            "eth-ofh-provider": -3*self.FONTSIZE,
            "oam-netconf-provider": -3*self.FONTSIZE,
            "eth-ofh-consumer": +3*self.FONTSIZE,

            "ofh-netconf-provider": -3*self.FONTSIZE,
            "uu-radio-provider": 3*self.FONTSIZE,

            "uu-radio-consumer": -3*self.FONTSIZE,
            "n1-nas-consumer": -3*self.FONTSIZE
        }
        if name in mapping:
            return mapping[name]

        print("Node: CEP name", name, "for y postion calculation not found")
        return 0

    def configuration(self) -> dict:
        """
        Getter for a json object representing the TAPI Node configuration.
        :return TAPI Node configuration as json object.
        """
        return self.__configuration

    def data(self) -> dict:
        """
        Getter for a json object representing the TAPI Link.
        :return TAPI Link as json object.
        """
        return self.__data

    def local_id(self) -> int:
        return self.configuration()["node"]["localId"]

    def function(self) -> str:
        """
        Getter returning the network-function type
        :return The type of the network-function as yang IDENTITY.
        """
        return self.__configuration['node']['function']

    def function_label(self) -> str:
        """
        Getter returning the network-function label
        :return The type of the network-function as human readable string.
        """
        mapping = {
            "o-ran-sc-topology-common:smo": "SMO",
            "o-ran-sc-topology-common:o-cloud": "O-Cloud",
            "o-ran-sc-topology-common:near-rt-ric": "Near-RT-RIC",
            "o-ran-sc-topology-common:access-and-mobility-management-function": "AMF",
            "o-ran-sc-topology-common:user-plane-function": "UPF",
            "o-ran-sc-topology-common:o-cu": "O-CU",
            "o-ran-sc-topology-common:o-cu-cp": "O-CU-CP",
            "o-ran-sc-topology-common:o-cu-up": "O-CU-UP",
            "o-ran-sc-topology-common:o-du": "O-DU",
            "o-ran-sc-topology-common:fronthaul-gateway": "FHGW",
            "o-ran-sc-topology-common:o-ru": "O-RU",
            "o-ran-sc-topology-common:user-equipment": "UE"
        }
        if mapping[self.function()]:
            return mapping[self.function()]
        else:
            return self.function()

    def identifier(self) -> str:
        """
        Getter returning the TAPI Node identifier.
        :return Object identifier as UUID.
        """
        return self.__data["uuid"]

    def json(self) -> dict:
        """
        Getter for a json object representing the TAPI Node.
        :return TAPI Node as json object.
        """
        result = self.__data.copy()
        result['owned-node-edge-point'] = []
        for nep in self.__data['owned-node-edge-point']:
            result['owned-node-edge-point'].append(nep.json())
        return result

    def name(self) -> str:
        """
        Getter for TAPI Node name.
        :return TAPI Node as json object.
        """
        return "".join([
            self.__configuration['node']['type'],
            "-",
            str(self.__configuration['node']['localId'])
        ])

    def node_edge_point_by_cep_name(self, cep_name, local_id) -> TapiNodeEdgePoint:
        """
        Method returning a NEP based on a given interface name
        :param interface_name: Search string
        :return The NEP uuid or "not found"
        """
        result = []
        for nep in self.__data["owned-node-edge-point"]:
            for cep in nep.connection_edge_points():
                if cep.name() == cep_name:
                    result.append(nep)
        if len(result) == 0:
            for nep in self.__data["owned-node-edge-point"]:
                print("# Check", cep_name, nep.json()["name"][0]["value"], nep.json()[
                      "tapi-connectivity:cep-list"]["connection-end-point"][0]["name"][0]["value"])
            return
        if len(result) > 1:
            for nep in result:
                if nep.name().endswith(str(local_id[-1])):
                    return nep
        return result[0]

    def parent(self) -> 'TapiNode':
        """
        Getter for a TAPI Node object representing the TAPI Node configuration.
        :return TAPI Node configuration as json object.
        """
        return self.__parent

    def svg(self, x: int, y: int) -> etree.Element:
        """
        Getter for a xml Element object representing the TAPI Node.
        :return TAPI Node as svg object.
        """
        self.__svg_x = x
        self.__svg_y = y

        svg_nep = None
        if type(self).__name__ == "TapiNodeSmo":
            svg_nep = Node(self, x, y)
        elif type(self).__name__ == "TapiNodeOCloud":
            svg_nep = OCloud(self, x, y)
        elif type(self).__name__ == "TapiNodeNearRtRic":
            svg_nep = NearRtRic(self, x, y)
        elif type(self).__name__ == "TapiNodeAmf":
            svg_nep = Amf(self, x, y)
        elif type(self).__name__ == "TapiNodeOCuCp":
            svg_nep = OCuCp(self, x, y)
        elif type(self).__name__ == "TapiNodeOCuUp":
            svg_nep = OCuUp(self, x, y)
        elif type(self).__name__ == "TapiNodeODu":
            svg_nep = ODu(self, x, y)
        elif type(self).__name__ == "TapiNodeUserEquipment":
            svg_nep = Ue(self, x, y)
        elif type(self).__name__ == "TapiNodeFronthaulGateway":
            svg_nep = FronthaulGateway(self, x, y)
        # elif type(self).__name__ == "TapiNodeORu":
        #     svg_nep = Node(self, x, y)
        # elif type(self).__name__ == "TapiNodeUserEquipment":
        #     svg_nep = Node(self, x, y)
        else:
            svg_nep = Node(self, x, y)

        group: etree.Element = svg_nep.svg_element()

        for nep in self.data()['owned-node-edge-point']:
            localId = 0
            if "local-id" in nep.configuration()["nodeEdgePoint"]:
                localId = nep.configuration()["nodeEdgePoint"]["local-id"]

            nep_x = x + \
                self.x_offset_by_cep_name(
                    nep.connection_edge_points()[0].name(), localId)
            nep_y = y + \
                self.y_offset_by_cep_name(
                    nep.connection_edge_points()[0].name())
            group.append(nep.svg(nep_x, nep_y))
        return group

    def width(self, width: int) -> None:
        """
        Setter for the SVG width in px.
        :param width as integer with unit "px" (pixel)
        """
        self.__width = width

    # methods

    def add(self, nep: TapiNodeEdgePoint) -> 'TapiNode':
        """
        Method adding a TAPI Node Edge Point object.
        :return TAPI Node as object.
        """
        self.__data['owned-node-edge-point'].append(nep)
        return self
