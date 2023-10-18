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
from model.python.tower import Tower
from model.python.o_ran_object import IORanObject
from model.python.o_ran_node import ORanNode
import xml.etree.ElementTree as ET

# Define the "IORanDu" interface
class IORanDu(IORanObject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


# Define an abstract O-RAN Node class
class ORanDu(ORanNode, IORanDu):
    def __init__(self, o_ran_du_data: IORanDu = None, **kwargs):
        super().__init__(o_ran_du_data, **kwargs)
        self._towers: list(ORanDu) = self._calculate_towers()

    def _calculate_towers(self):
        hex_ring_radius: int = self.spiralRadiusProfile.oRanDuSpiralRadiusOfTowers
        index: int = 0
        s: str = "00" + str(index)
        name: str = "Tower-" + s[len(s) - 2 : len(s)]
        result : list(Tower) = []
        result.append(
            Tower(
                {
                    "name": name,
                    "geoLocation": self.geoLocation,
                    "position": self.position,
                    "layout": self.layout,
                    "spiralRadiusProfile": self.spiralRadiusProfile,
                    "parent": self
                }
            )
        )
        return result

    @property
    def towers(self):
        return self._towers
    
    def toKml(self):
        return None

    def toSvg(self):
        return None
