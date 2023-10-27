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
A Class representing an O-RAN distributed unit (ORanDu)
"""
import model.python.hexagon as Hexagon
from model.python.hexagon import Hex
from model.python.cube import Cube
from model.python.o_ran_ru import ORanRu
from model.python.o_ran_object import IORanObject
from model.python.o_ran_node import ORanNode
import xml.etree.ElementTree as ET


# Define the "IORanDu" interface
class IORanDu(IORanObject):
    def __init__(self, o_ran_ru_count: int, **kwargs):
        super().__init__(**kwargs)
        self._o_ran_ru_count = o_ran_ru_count


# Define an abstract O-RAN Node class
class ORanDu(ORanNode, IORanDu):
    def __init__(self, o_ran_du_data: IORanDu = None, **kwargs):
        super().__init__(o_ran_du_data, **kwargs)
        self._o_ran_rus: list[ORanRu] = self._calculate_o_ran_rus()

    def _calculate_o_ran_rus(self) -> list[ORanRu]:
        result: list[ORanRu] = []
        for index in range(self._o_ran_ru_count):
            s: str = "00" + str(index)
            name: str = "-".join(
                [self.name.replace("DU", "RU"), s[len(s) - 2 : len(s)]]
            )
            network_center: dict = self.parent.parent.parent.parent.center
            newGeo = Hexagon.hex_to_geo_location(
                self.layout, hex, network_center
            ).json()
            result.append(
                ORanRu(
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
    def o_ran_rus(self) -> list[ORanRu]:
        return self._o_ran_rus

    def toKml(self) -> ET.Element:
        o_ran_du: ET.Element = ET.Element("Folder")
        open: ET.Element = ET.SubElement(o_ran_du, "open")
        open.text = "1"
        name: ET.Element = ET.SubElement(o_ran_du, "name")
        name.text = self.name
        for tower in self.towers:
            o_ran_du.append(tower.toKml())
        return o_ran_du

    def toSvg(self) -> None:
        return None
