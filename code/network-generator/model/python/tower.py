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
A Class representing a Tower to mount O-RAN RUs
It can be interpreted as 'resource pool' for physical network
functions.
"""
from typing import overload
from model.python.o_ran_object import IORanObject
from model.python.o_ran_ru import ORanRu
from model.python.o_ran_node import ORanNode
from model.python.o_ran_termination_point import ORanTerminationPoint
import xml.etree.ElementTree as ET


# Define the "IORanDu" interface
class ITower(IORanObject):
    def __init__(self, o_ran_ru_count: int, **kwargs):
        super().__init__(**kwargs)
        self._o_ran_ru_count = o_ran_ru_count


# Implement a concrete O-RAN Node class
class Tower(ORanNode):
    def __init__(self, tower_data: ITower = None, **kwargs):
        super().__init__(tower_data, **kwargs)
        self._o_ran_ru_count = (
            tower_data["oRanRuCount"]
            if tower_data and "oRanRuCount" in tower_data
            else 3
        )
        self._o_ran_rus: list[ORanRu] = self._create_o_ran_rus()

    def _create_o_ran_rus(self) -> list[ORanRu]:
        result: list[ORanRu] = []
        for index in range(self._o_ran_ru_count):
            s: str = "00" + str(index)
            name: str = "-".join(
                [self.name.replace("Tower", "RU"), s[len(s) - 2 : len(s)]]
            )
            cell_count: int = self.parent.parent.parent.parent.parent.configuration()[
                "pattern"
            ]["o-ran-ru"]["nr-cell-du-count"]
            cell_angle : int = self.parent.parent.parent.parent.parent.configuration()[
                "pattern"
            ]["nr-cell-du"]["cell-angle"]
            ru_angle: int = cell_count * cell_angle
            ru_azimuth: int = index * ru_angle
            result.append(
                ORanRu(
                    {
                        "name": name,
                        "geoLocation": self.geoLocation,
                        "position": self.position,
                        "layout": self.layout,
                        "spiralRadiusProfile": self.spiralRadiusProfile,
                        "parent": self,
                        "cellCount": cell_count,
                        "ruAngle": ru_angle,
                        "ruAzimuth": ru_azimuth,
                    }
                )
            )
        return result

    @property
    def o_ran_rus(self) -> list[ORanRu]:
        return self._o_ran_rus

    @property
    def termination_points(self) -> list[ORanTerminationPoint]:
        result: list[ORanTerminationPoint] = super().termination_points
        phy_tp: str = "-".join([self.name, "phy".upper()])
        result.append({"tp-id": phy_tp})
        for interface in ["e2", "o1", "ofhm", "ofhc", "ofhu","ofhs"]:
            result.append(              {
                "tp-id": "-".join([self.name, interface.upper()]),
                "supporting-termination-point": [
                  {
                    "network-ref": type(self.parent.parent.parent.parent),
                    "node-ref":self.name,
                    "tp-ref": phy_tp
                  }
                ]
              })
        return result

    def to_topology_nodes(self) -> list[dict[str, dict]]:
        result: list[dict[str, dict]] = super().to_topology_nodes()
        for o_ran_ru in self.o_ran_rus:
            result.extend(o_ran_ru.to_topology_nodes())    
        return result

    def to_topology_links(self) -> list[dict[str, dict]]:
        result: list[dict[str, dict]] = super().to_topology_links()
        for o_ran_ru in self.o_ran_rus:
            result.extend(o_ran_ru.to_topology_links())    
        return result
    
    def toKml(self) -> ET.Element:
        tower: ET.Element = ET.Element("Folder")
        open: ET.Element = ET.SubElement(tower, "open")
        open.text = "1"
        name: ET.Element = ET.SubElement(tower, "name")
        name.text = self.name
        for o_ran_ru in self.o_ran_rus:
            tower.append(o_ran_ru.toKml())
        return tower


    def toSvg(self) -> None:
        return None
