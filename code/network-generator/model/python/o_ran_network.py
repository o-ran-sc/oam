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
from typing import Any

from model.python.o_ran_smo import ORanSmo
from model.python.o_ran_spiral_radius_profile import SpiralRadiusProfile
from model.python.o_ran_object import IORanObject, ORanObject
import model.python.hexagon as Hexagon
from model.python.hexagon import Layout
from model.python.point import Point
import xml.etree.ElementTree as ET


class ORanNetwork(ORanObject):
    """
    Class representing an O-RAN Network object.
    """

    # constructor
    def __init__(self, configuration: dict[str, Any], of: IORanObject = None, **kwargs):
        super().__init__(of, **kwargs)
        self.__configuration = configuration
        self.name = configuration["name"]
        self.center = configuration["center"]
        size = configuration["pattern"]["o-ran-ru"]["max-reach"]
        layout = Layout(
            Hexagon.layout_flat, Point(size, size), Point(0, 0)
        )  # 1 pixel = 1 meter
        spiral_radius_profile = SpiralRadiusProfile(
            {
                "oRanSmoSpiralRadiusOfNearRtRics": configuration["pattern"]["smo"][
                    "near-rt-ric-spiral-radius"
                ],
                "oRanNearRtRicSpiralRadiusOfOCus": configuration["pattern"][
                    "near-rt-ric"
                ]["o-ran-cu-spiral-radius"],
                "oRanCuSpiralRadiusOfODus": configuration["pattern"]["o-ran-cu"][
                    "o-ran-du-spiral-radius"
                ],
                "oRanDuSpiralRadiusOfTowers": configuration["pattern"]["o-ran-du"][
                    "tower-spiral-radius"
                ],
            }
        )
        self._o_ran_smo = ORanSmo(
            {
                "name": "SMO",
                "geoLocation": self.center,
                "layout": layout,
                "spiralRadiusProfile": spiral_radius_profile,
                "parent": self,
            }
        )

    # getter
    def configuration(self) -> dict[str, dict]:
        """
        Getter for a json object representing the O-RAN Network.
        :return O-RAN Network as json object.
        """
        return self.__configuration

    def __appendNodes(self) -> list[dict[str, Any]]:
        result: list[dict[str, Any]] = []
        for tower in self._o_ran_smo.towers:
            result.append(tower.toTopology())
        return result

    def toTopology(self) -> dict[str, Any]:
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

    def toKml(self) -> ET.Element:
        root: ET.Element = ET.Element("kml", xmlns="http://www.opengis.net/kml/2.2")
        document = ET.SubElement(root, "Document")
        open = ET.SubElement(document, "open")
        open.text = "1"
        name = ET.SubElement(document, "name")
        name.text = self.name
        folder = ET.SubElement(document, "Folder")
        open = ET.SubElement(folder, "open")
        open.text = "1"
        name = ET.SubElement(folder, "name")
        name.text = "Towers"
        for tower in self._o_ran_smo.towers:
            folder.append(tower.toKml())

        return root

    def toSvg(self) -> ET.Element:
        """
        Getter for a xml/svg Element object representing the Network.
        :return Network as SVG object.
        """
        root: ET.Element = ET.Element(
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
