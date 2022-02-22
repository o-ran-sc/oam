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
Module containing a class representing a SMO as TAPI Node.
"""
from typing import List
from lxml import etree
from model.python.tapi_node import TapiNode
from model.python.tapi_node_edge_point import TapiNodeEdgePoint


class TapiNodeSmo(TapiNode):
    """
    Class representing a SMO as TAPI Node
    """
    __width: 0

    # constructor
    def __init__(self, parent: TapiNode, config):
        super().__init__(parent, config)

        # add O2 consumer interface
        nep_configuration = {
            "parent": self.identifier(),
            "nodeEdgePoint": {
                "interface": "o2", "cep": [{"protocol": "REST", "role": "consumer"}]
            }
        }
        self.add(TapiNodeEdgePoint(nep_configuration))

        # add A1 consumer interface
        nep_configuration = {
            "parent": self.identifier(),
            "nodeEdgePoint": {
                "interface": "a1", "cep": [{"protocol": "REST", "role": "consumer"}]
            }
        }
        self.add(TapiNodeEdgePoint(nep_configuration))

        # add O1/OAM NetConf Consumer interface
        nep_configuration = {
            "parent": self.identifier(),
            "nodeEdgePoint": {
                "interface": "oam", "cep": [{"protocol": "NETCONF", "role": "consumer"}]
            }
        }
        self.add(TapiNodeEdgePoint(nep_configuration))

        # add O1 VES Provider interface
        nep_configuration = {
            "parent": self.identifier(),
            "nodeEdgePoint": {
                "interface": "o1", "cep": [{"protocol": "VES", "role": "provider"}]
            }
        }
        self.add(TapiNodeEdgePoint(nep_configuration))

        # add O1 File Transfer Consumer interface
        nep_configuration = {
            "parent": self.identifier(),
            "nodeEdgePoint": {
                "interface": "o1", "cep": [{"protocol": "FILE", "role": "consumer"}]
            }
        }
        self.add(TapiNodeEdgePoint(nep_configuration))

    def __smo_component(self, x: int, y: int, label: str) -> etree.Element:
        group = etree.Element("g")
        group.attrib["class"] = " ".join(["node", label])

        width = (2 + 2) * (2.2*self.FONTSIZE)
        height = 2 * (2*self.FONTSIZE)

        rect = etree.Element("rect")
        rect.attrib["x"] = str(int(x - width/2))
        rect.attrib["y"] = str(int(y - height/2))
        rect.attrib["width"] = str(int(width))
        rect.attrib["height"] = str(int(height))
        rect.attrib["rx"] = str(self.FONTSIZE)
        rect.attrib["class"] = " ".join(["node", label])
        group.append(rect)

        labelElement = etree.Element('text')
        labelElement.attrib['x'] = str(x)
        # +4px for font-size 14px (think of chars like 'gjy')
        labelElement.attrib['y'] = str(y + 4)
        labelElement.attrib['class'] = " ".join(["node", label])
        labelElement.text = label.upper()
        group.append(labelElement)
        return group

    def svg(self, x: int, y: int) -> etree.Element:
        """
        Getter for a xml Element object representing the TAPI Node.
        :return TAPI Node as svg object.
        """
        super().svg(x, y)

        components = ["o2-controller", "non-rt-ric", "oam-controller",
                      "ves-collector", "file-server"]

        group = etree.Element("g")
        group.attrib["class"] = "node"
        title = etree.Element("title")
        title.text = "\n TAPI Node\n id: " + \
            self.identifier() + "\n name: " + self.name()
        group.append(title)

        width = (len(components)*5 +1) * (2.2*self.FONTSIZE)
        height = 2 * (2.2*self.FONTSIZE)

        rect = etree.Element("rect")
        rect.attrib["x"] = str(int(x - width/2))
        rect.attrib["y"] = str(int(y - height/2))
        rect.attrib["width"] = str(int(width))
        rect.attrib["height"] = str(int(height))
        rect.attrib["rx"] = str(self.FONTSIZE)
        rect.attrib["class"] = " ".join(
            ["node", self.function_label().lower()])
        group.append(rect)

        label = etree.Element('text')
        label.attrib['x'] = str(x)
        # +4px for font-size 14px (think of chars like 'gjy')
        label.attrib['y'] = str(y + 4)
        label.attrib['class'] = " ".join(
            ["node", self.function_label().lower()])
        label.text = self.function_label()
        group.append(label)

        for component in components:
            x_mapping = {
                "o2-controller": -4*6*self.FONTSIZE,
                "non-rt-ric": -2*6*self.FONTSIZE,
                "oam-controller": -0*6*self.FONTSIZE,
                "ves-collector": +2*6*self.FONTSIZE,
                "file-server": +4*6*self.FONTSIZE
            }
            comp_x = x + x_mapping[component]
            comp_y = y-0*self.FONTSIZE
            group.append(self.__smo_component(comp_x, comp_y, component))

        for nep in self.data()['owned-node-edge-point']:
            nep_x = x + \
                super().x_offset_by_cep_name(
                    nep.connection_edge_points()[0].name(), 0)
            nep_y = y + \
                super().y_offset_by_cep_name(
                    nep.connection_edge_points()[0].name())
            group.append(nep.svg(nep_x, nep_y))

        return group
