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
A Class representing an O-RAN radio unit (ORanRu)
"""
from model.python.nr_cell_du import NrCellDu
from model.python.o_ran_object import IORanObject
from model.python.o_ran_node import ORanNode
import xml.etree.ElementTree as ET


# Define the "IORanRu" interface
class IORanRu(IORanObject):
    def __init__(self, cell_count: int, ru_angle:int, ru_azimuth:int, **kwargs):
        super().__init__(**kwargs)
        self._cell_count = cell_count
        self._ru_angle = ru_angle
        self._ru_azimuth = ru_azimuth


# Define an abstract O-RAN Node class
class ORanRu(ORanNode, IORanRu):
    def __init__(self, o_ran_ru_data: IORanRu = None, **kwargs):
        super().__init__(o_ran_ru_data, **kwargs)
        self._cell_count = o_ran_ru_data["cellCount"] if o_ran_ru_data and "cellCount" in o_ran_ru_data else 1
        self._ru_angle = o_ran_ru_data["ruAngle"] if o_ran_ru_data and "ruAngle" in o_ran_ru_data else 120
        self._ru_azimuth = o_ran_ru_data["ruAzimuth"] if o_ran_ru_data and "ruAzimuth" in o_ran_ru_data else 0
        self._cells: list[NrCellDu] = self._create_cells()


    def _create_cells(self) -> list[NrCellDu]:
        result: list[NrCellDu] = []
        cell_angle : int = self.parent.parent.parent.parent.parent.parent.configuration()[
            "pattern"
        ]["nr-cell-du"]["cell-angle"]
        for index in range(self._cell_count):
            s: str = "00" + str(index)
            name: str = "-".join(
                [self.name.replace("RU", "NRCellDu"), s[len(s) - 2 : len(s)]]
            )
            azimuth: int = index * cell_angle +self._ru_azimuth
            result.append(
                NrCellDu(
                    {
                        "name": name,
                        "geoLocation": self.geoLocation,
                        "position": self.position,
                        "layout": self.layout,
                        "spiralRadiusProfile": self.spiralRadiusProfile,
                        "parent": self,
                        "cellAngle": cell_angle,
                        "azimuth": azimuth,
                    }
                )
            )
        return result

    @property
    def cells(self) -> list[NrCellDu]:
        return self._cells

    def toKml(self) -> ET.Element:
        print("ru-tower", self.position, self.parent.position) if self.position.q is not self.parent.position.q else "ok"
        o_ran_ru: ET.Element = ET.Element("Folder")
        open: ET.Element = ET.SubElement(o_ran_ru, "open")
        open.text = "1"
        name: ET.Element = ET.SubElement(o_ran_ru, "name")
        name.text = self.name
        for cell in self.cells:
            o_ran_ru.append(cell.toKml())
        return o_ran_ru

    def toSvg(self) -> None:
        return None
