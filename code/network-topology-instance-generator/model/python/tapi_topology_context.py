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
Module for the TAPI Topology Context
"""
from typing import Dict, List, Union
from lxml import etree
from model.python.tapi_topology import TapiTopology
from model.python.top import Top


class TapiTopologyContext(Top):
    """
    Class providing a TAPI Topology Context object
    """

    __data: Dict[str, Dict[str, List]] = {
        "tapi-topology:topology-context": {
            "topology": []}}
    __tapi_topology: List[TapiTopology] = []

    # constructor
    def __init__(self, configuration: Dict[str, Union[str, Dict[str, int]]]):
        super().__init__(configuration)
        topology = TapiTopology(configuration)
        self.__tapi_topology.append(topology)

    # getter
    def configuration(self) -> dict:
        """
        Getter for a json object representing the TAPI Topology Context initail
        configuration.
        :return TAPI Topology Context configuration as json object.
        """
        return self.__configuration

    def data(self) -> dict:
        """
        Getter for a json object representing the TAPI Topology Context.
        :return TAPI Topology Context as json object.
        """
        return self.__data

    def name(self) -> str:
        """
        Getter returning the container name.
        :return Static string
        """
        return "tapi-topology:topology-context"

    def identifier(self) -> str:
        """
        Getter returning the container name which acts as identifier
        :return Static string
        """
        return self.name()

    def json(self) -> dict:
        """
        Getter for a json object representing the TAPI Topology Context.
        :return TAPI Topology Context as json object.
        """
        result = self.__data.copy()
        for topology in self.__tapi_topology:
            result["tapi-topology:topology-context"]["topology"].append(
                topology.json())
        return result

    def svg(self, x, y) -> etree.Element:
        """
        Getter for a xml Element object representing the TAPI Topology Context.
        :return TAPI Topology Context as svg object.
        """
        group = etree.Element("g")
        title = etree.Element("title")
        title.text = "\n context: " + self.identifier() + "\n name: " + self.name()
        group.append(title)

        for topology in self.__tapi_topology:
            group.append(topology.svg(x, y))
        return group
