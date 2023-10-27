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
A Class representing an O-RAN centralized unit (ORanCu)
"""
from model.python.cube import Cube
from model.python.hexagon import Hex
import model.python.hexagon as Hexagon
from model.python.o_ran_du import ORanDu
from model.python.tower import Tower
from model.python.o_ran_object import IORanObject
from model.python.o_ran_node import ORanNode
import xml.etree.ElementTree as ET


# Define the "IORanCu" interface
class IORanCu(IORanObject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


# Define an abstract O-RAN Node class
class ORanCu(ORanNode, IORanCu):
    def __init__(self, o_ran_cu_data: IORanCu = None, **kwargs):
        super().__init__(o_ran_cu_data, **kwargs)
        self._o_ran_dus: list[ORanCu] = self._calculate_o_ran_dus()

    def _calculate_o_ran_dus(self) -> list[ORanDu]:
        hex_ring_radius: int = self.spiralRadiusProfile.oRanCuSpiralRadiusOfODus
        hex_list: list[Hex] = self.spiralRadiusProfile.oRanDuSpiral(self.position, hex_ring_radius)
        result: list[ORanDu] = []
        for index, hex in enumerate(hex_list):
            s: str = "00" + str(index)
            name: str = "-".join(
                [self.name.replace("CU", "DU"), s[len(s) - 2 : len(s)]]
            )
            network_center: dict = self.parent.parent.parent.center
            newGeo = Hexagon.hex_to_geo_location(
                self.layout, hex, network_center
            ).json()
            result.append(
                ORanDu(
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
    def o_ran_dus(self) -> list[ORanDu]:
        return self._o_ran_dus

    @property
    def towers(self) -> list[Tower]:
        result: list[Tower] = []
        for du in self.o_ran_dus:
            for tower in du.towers:
                result.append(tower)
        return result

    def toKml(self) -> ET.Element:
        o_ran_cu: ET.Element = ET.Element("Folder")
        open: ET.Element = ET.SubElement(o_ran_cu, "open")
        open.text = "1"
        name: ET.Element = ET.SubElement(o_ran_cu, "name")
        name.text = self.name
        for o_ran_du in self.o_ran_dus:
            o_ran_cu.append(o_ran_du.toKml())
        return o_ran_cu


    def toSvg(self) -> None:
        return None
