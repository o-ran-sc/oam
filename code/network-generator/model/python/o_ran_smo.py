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
A Class representing an O-RAN Service Management and Orchestration Framework (SMO)
"""
from model.python.tower import Tower
from model.python.o_ran_near_rt_ric import ORanNearRtRic
from model.python.o_ran_object import IORanObject
from model.python.o_ran_node import ORanNode
import xml.etree.ElementTree as ET


# Define the "IORanSmo" interface
class IORanSmo(IORanObject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


# Define an abstract O-RAN Node class
class ORanSmo(ORanNode, IORanSmo):
    def __init__(self, o_ran_smo_data: IORanSmo = None, **kwargs):
        super().__init__(o_ran_smo_data, **kwargs)
        self._o_ran_near_rt_rics: list(ORanNearRtRic) = self._calculate_near_rt_rics()

    def _calculate_near_rt_rics(self):
        hex_ring_radius: int = self.spiralRadiusProfile.oRanSmoSpiralRadiusOfNearRtRics
        index: int = 0
        s: str = "00" + str(index)
        name: str = "Ric-" + s[len(s) - 2 : len(s)]
        result: list(ORanNearRtRic) = []
        result.append(
            ORanNearRtRic(
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

    # return this.spiralProfile.oRanNearRtRicSpiral(this.position, hexRingRadius).map((hex, index) => {
    #   const name: string = 'Ric-' + ('00' + index).slice(-2);
    #   return new ORanNearRtRic({ name: name, position: hex, layout: this.layout, spiralProfile: this.spiralProfile, parent: this });
    # });

    @property
    def o_ran_near_rt_rics(self):
        return self._o_ran_near_rt_rics
    
    @property
    def towers(self):
        result: list(Tower) = []
        for ric in self.o_ran_near_rt_rics:
            for tower in ric.towers:
                result.append(tower)
        return result

    def toKml(self):
        return None

    def toSvg(self):
        return None
