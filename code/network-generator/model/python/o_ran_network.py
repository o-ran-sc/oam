# Copyright 2023 highstreet technologies GmbH
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
Module for a class representing a O-RAN Network
"""
from typing import Any, Dict, List
from model.python.Tower import Tower
from model.python.ORanObject import IORanObject, ORanObject
import xml.etree.ElementTree as ET


class ORanNetwork(ORanObject):
    """
    Class representing an O-RAN Network object.
    """

    # constructor
    def __init__(self, configuration: Dict[str, Any], of: IORanObject = None, **kwargs):
        super().__init__(of, **kwargs)
        self.__configuration = configuration
        self.__towers: List[Tower] = []

        center = configuration["center"]
        self.__towers.append(Tower(center))

    # getter
    def configuration(self) -> Dict[str, Dict]:
        """
        Getter for a json object representing the O-RAN Network.
        :return O-RAN Network as json object.
        """
        return self.__configuration

    def __appendNodes(self):
        result: List[Dict[str, Any]] = []
        for tower in self.__towers:
            result.append(tower.toTopology())
        return result

    def toTopology(self):
        return {
            "ietf-network:networks": {
                "network": [
                    {
                        "network-id": self.id,
                        "node": self.__appendNodes(),
                        "ietf-network-topology:link": [],
                    }
                ],
            }
        }

    def toKml(self):
        root: Element = ET.Element("kml", xmlns="http://www.opengis.net/kml/2.2")
        document = ET.SubElement(root, "Document")
        open = ET.SubElement(document, "open")
        open.text = "1"
        return root

    def toSvg(self):
        """
        Getter for a xml/svg Element object representing the Network.
        :return Network as SVG object.
        """
        root: Element = ET.Element(
            "svg",
            # width=str(self.__svg_width()),
            # height=str(self.__svg_height()),
            # viewBox=" ".join([
            #     str(-3*self.FONTSIZE),
            #     str(-3*self.FONTSIZE),
            #     str(self.__svg_width()),
            #     str(self.__svg_height())]
            # ),
            xmlns="http://www.w3.org/2000/svg",
        )
        desc = ET.Element("desc")
        # desc.text="\n context: " + str(self.id()) + "\n name: " + str(self.name())
        root.append(desc)

        title = ET.Element("title")
        title.text = self.configuration()["name"]
        root.append(title)

        # root.append(self.__context.svg(x, y))
        return root
