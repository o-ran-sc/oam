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
Module for the class representing a TAPI Link
"""
from typing import Dict, Union
import uuid
from lxml import etree
from model.python.link_config import LinkConfig
from model.python.top import Top


class TapiLink(Top):
    """
    Class representing a TAPI Link object.
    """

    __data: dict = {}
    __configuration: dict = {}

    # constructor
    def __init__(self, configuration: dict):
        super().__init__(configuration)
        self.__configuration = configuration
        self.__link_configuration = LinkConfig(
            topology_reference=configuration["topology_reference"],
            name_prefix=configuration["name_prefix"],
            provider=configuration["provider"],
            consumer=configuration["consumer"]
        )
        link_data = self.__link_configuration.json()
        self.__data = {
            "uuid": str(uuid.uuid4()),
            "name": [{
                "value-name": "topology-link-name",
                "value": link_data['link']['name']
            }],
            "transitioned-layer-protocol-name": ["inETH", "outETH"],
            "administrative-state": "LOCKED",
            "operational-state": "ENABLED",
            "direction": "BIDIRECTIONAL",
            "lifecycle-state": "INSTALLED",
            "node-edge-point": [
                link_data['link']['a'],
                link_data['link']['z']
            ],
            "latency-characteristic": [{
                "traffic-property-name": "property-1",
                "queing-latency-characteristic": "queue-1",
                "fixed-latency-characteristic": "latency-1",
                "jitter-characteristic": "jitter-1",
                "wander-characteristic": "wander-1"
            }],
            "layer-protocol-name": ["ETH"],
            "risk-characteristic": [{
                "risk-characteristic-name": "risk-name",
                "risk-identifier-list": [
                    "risk-1"]}],
            "validation-mechanism": [{
                "validation-mechanism": "mechanism-1",
                "validation-robustness": "very-robust",
                "layer-protocol-adjacency-validated": "validated"}],
            "cost-characteristic": [{
                "cost-name": "cost",
                "cost-algorithm": "alg1",
                "cost-value": "value-1"}]}

    # getter
    def configuration(self) -> Dict[str, Dict]:
        """
        Getter for a json object representing the initial configuration of a TAPI Link.
        :return TAPI Link configuration as json object.
        """
        return self.__configuration

    def data(self) -> dict:
        """
        Getter for a json object representing the TAPI Link.
        :return TAPI Link as json object.
        """
        return self.__data

    def json(self) -> dict:
        """
        Getter for a json object representing the TAPI Link.
        :return TAPI Link as json object.
        """
        return self.data()

    def identifier(self) -> str:
        """
        Getter returning the TAPI Link identifier.
        :return Object identifier as UUID.
        """
        return self.__data["uuid"]

    def name(self) -> str:
        """
        Getter for TAPI Link name.
        :return TAPI Link as json object.
        """
        return self.__link_configuration.json()['link']['name']

    def svg(self, svg_x: int, svg_y: int) -> etree.Element:
        """
        Getter for a xml Element object representing the TAPI Link.
        :return TAPI Link as svg object.
        """

        group = etree.Element("g")
        class_name = self.name().split("-")[0].lower()
        group.attrib["class"] = " ".join(["link", class_name])
        title = etree.Element("title")
        title.text = "\n TAPI Link\n id: " + \
            self.identifier() + "\n name: " + self.name()
        group.append(title)

        # cubic bezier curves
        source_x = self.__link_configuration.consumer_node_edge_point().svg_x()
        source_y = self.__link_configuration.consumer_node_edge_point().svg_y()
        target_x = self.__link_configuration.provider_node_edge_point().svg_x()
        target_y = self.__link_configuration.provider_node_edge_point().svg_y()

        path = etree.Element("path")
        path.attrib["d"] = " ".join(["M", str(source_x), str(source_y),
                                     "C", str(source_x), str(target_y),
                                     str(target_x), str(source_y),
                                     str(target_x), str(target_y)])
        path.attrib["class"] = "link"
        group.append(path)

        return group
