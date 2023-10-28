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
A Class representing an O-RAN O-Cloud resource pool for O-RAN distributed units (ORanDu)
By default all O-RAN-DUs associated with the towers around  are deployed here.
Maybe dedicated hardware is required to host O-DUs, but it is expected 
that the O-Cloud mechanism and concepts can be applied here.
"""
import model.python.hexagon as Hexagon
from model.python.hexagon import Hex
from model.python.cube import Cube
from model.python.tower import Tower
from model.python.o_ran_object import IORanObject
from model.python.o_ran_node import ORanNode
import xml.etree.ElementTree as ET


# Define the "IORanDu" interface
class IORanCloudDu(IORanObject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


# Implements a concrete O-RAN Node class
class ORanCloudDu(ORanNode, IORanCloudDu):
    def __init__(self, o_ran_du_data: IORanCloudDu = None, **kwargs):
        super().__init__(o_ran_du_data, **kwargs)
        self._towers: list[Tower] = self._calculate_towers()

    def _calculate_towers(self) -> list[Tower]:
        hex_ring_radius: int = self.spiralRadiusProfile.oRanDuSpiralRadiusOfTowers
        hex_list: list[Hex] = Cube.spiral(self.position, hex_ring_radius)
        result: list[Tower] = []
        for index, hex in enumerate(hex_list):
            s: str = "00" + str(index)
            name: str = "-".join(
                [self.name.replace("O-Cloud-DU", "Tower"), s[len(s) - 2 : len(s)]]
            )
            network_center: dict = self.parent.parent.parent.parent.center
            newGeo = Hexagon.hex_to_geo_location(
                self.layout, hex, network_center
            ).json()
            result.append(
                Tower(
                    {
                        "name": name,
                        "geoLocation": newGeo,
                        "position": hex,
                        "layout": self.layout,
                        "spiralRadiusProfile": self.spiralRadiusProfile,
                        "parent": self,
                    }
                )
            )
        return result

    @property
    def towers(self) -> list[Tower]:
        return self._towers

    def toKml(self) -> ET.Element:
        o_ran_cloud_du: ET.Element = ET.Element("Folder")
        open: ET.Element = ET.SubElement(o_ran_cloud_du, "open")
        open.text = "1"
        name: ET.Element = ET.SubElement(o_ran_cloud_du, "name")
        name.text = self.name
        for tower in self.towers:
            o_ran_cloud_du.append(tower.toKml())
        return o_ran_cloud_du

    def toSvg(self) -> None:
        return None
