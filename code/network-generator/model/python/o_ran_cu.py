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
        index: int = 0
        s: str = "00" + str(index)
        name: str = "O-RAN-DU-" + s[len(s) - 2 : len(s)]
        result: list[ORanDu] = []
        result.append(
            ORanDu(
                {
                    "name": name,
                    "geoLocation": self.geoLocation,
                    "position": self.position,
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

    def toKml(self) -> None:
        return None

    def toSvg(self) -> None:
        return None
