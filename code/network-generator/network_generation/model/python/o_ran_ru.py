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

# !/usr/bin/python

"""
A Class representing an O-RAN radio unit (ORanRu)
"""
import xml.etree.ElementTree as ET
from typing import Any, cast

from network_generation.model.python.nr_cell_du import NrCellDu
from network_generation.model.python.o_ran_du import ORanDu
from network_generation.model.python.o_ran_node import IORanNode, ORanNode
from network_generation.model.python.o_ran_termination_point import (
    ORanTerminationPoint,
)


# Define the "IORanRu" interface
class IORanRu(IORanNode):
    cellCount: int
    ruAngle: int
    ruAzimuth: int


default_value: IORanRu = cast(
    IORanRu,
    {
        **ORanNode.default(),
        **{"cellCount": 1, "ruAngle": 120, "ruAzimuth": 0},
    },
)


# Define an abstract O-RAN Node class
class ORanRu(ORanNode):
    def __init__(
        self,
        data: dict[str, Any] = cast(dict[str, Any], default_value),
        **kwargs: dict[str, Any]
    ) -> None:
        o_ran_ru_data: IORanRu = self._to_o_ran_ru_data(data)
        super().__init__(cast(dict[str, Any], o_ran_ru_data), **kwargs)
        self._cell_count: int = (
            int(str(o_ran_ru_data["cellCount"]))
            if o_ran_ru_data and "cellCount" in o_ran_ru_data
            else 1
        )
        self._ru_angle: int = (
            int(str(o_ran_ru_data["ruAngle"]))
            if o_ran_ru_data and "ruAngle" in o_ran_ru_data
            else 120
        )
        self._ru_azimuth: int = (
            int(str(o_ran_ru_data["ruAzimuth"]))
            if o_ran_ru_data and "ruAzimuth" in o_ran_ru_data
            else 0
        )
        self._cells: list[NrCellDu] = self._create_cells()
        name: str = self.name.replace("RU", "DU")

        o_ran_du_data: dict[str, Any] = {
            "name": name,
            "geoLocation": self.parent.geo_location,
            "position": self.parent.position,
            "layout": self.layout,
            "parent": self.parent.parent.parent,
        }
        self._oRanDu: ORanDu = ORanDu(o_ran_du_data)

    def _to_o_ran_ru_data(self, data: dict[str, Any]) -> IORanRu:
        result: IORanRu = default_value
        for key, key_type in IORanRu.__annotations__.items():
            if key in data:
                result[key] = data[key]  # type: ignore
        return result

    def _create_cells(self) -> list[NrCellDu]:
        result: list[NrCellDu] = []
        cell_config: dict = (
            self.parent.parent.parent.parent.parent.parent
            .configuration["pattern"]["nrCellDu"]
        )
        cell_angle: int = cell_config["cellAngle"]
        cell_scale_factor: int = (
            cell_config["cellScaleFactorForHandoverArea"]
        )
        maxReach: int = cell_config["maxReach"]
        for index in range(self._cell_count):
            s: str = "00" + str(index)
            name: str = "-".join(
                [self.name.replace("RU", "NRCellDu"), s[len(s) - 2: len(s)]]
            )
            azimuth: int = index * cell_angle + self._ru_azimuth
            result.append(
                NrCellDu(
                    {
                        "name": name,
                        "geoLocation": self.geo_location,
                        "position": self.position,
                        "layout": self.layout,
                        "parent": self,
                        "cellAngle": cell_angle,
                        "cellScaleFactorForHandoverArea": cell_scale_factor,
                        "maxReach": maxReach,
                        "azimuth": azimuth,
                    }
                )
            )
        return result

    @property
    def cells(self) -> list[NrCellDu]:
        return self._cells

    @property
    def oRanDu(self) -> ORanDu:
        return self._oRanDu

    def termination_points(self) -> list[ORanTerminationPoint]:
        result: list[ORanTerminationPoint] = super().termination_points()
        phy_tp: str = "-".join([self.name, "phy".upper()])
        result.append(ORanTerminationPoint({"id": phy_tp, "name": phy_tp}))
        for interface in ["ofhm", "ofhc", "ofhu", "ofhs"]:
            id: str = "-".join([self.name, interface.upper()])
            result.append(
                ORanTerminationPoint(
                    {"id": id, "name": id, "supporter": phy_tp, "parent": self}
                )
            )
        for cell in self.cells:
            result.extend(cell.termination_points())
        return result

    def to_topology_nodes(self) -> list[dict[str, Any]]:
        result: list[dict[str, Any]] = super().to_topology_nodes()
        result.extend(self.oRanDu.to_topology_nodes())
        return result

    def to_topology_links(self) -> list[dict[str, Any]]:
        result: list[dict[str, Any]] = super().to_topology_links()
        result.extend(self.oRanDu.to_topology_links())
        for interface in ["phy", "ofhm", "ofhc", "ofhu", "ofhs"]:
            link_id: str = "".join(
                [interface, ":", self.name, "<->", self.oRanDu.name]
            )
            source_tp: str = "-".join([self.name, interface.upper()])
            dest_tp: str = "-".join([self.oRanDu.name, interface.upper()])
            result.append(
                {
                    "link-id": link_id,
                    "source": {
                        "source-node": self.name,
                        "source-tp": source_tp,
                    },
                    "destination": {
                        "dest-node": self.oRanDu.name,
                        "dest-tp": dest_tp,
                    },
                }
            )
        return result

    def toKml(self) -> ET.Element:
        o_ran_ru: ET.Element = ET.Element("Folder")
        open: ET.Element = ET.SubElement(o_ran_ru, "open")
        open.text = "1"
        name: ET.Element = ET.SubElement(o_ran_ru, "name")
        name.text = self.name
        for cell in self.cells:
            o_ran_ru.append(cell.toKml())
        return o_ran_ru

    def toSvg(self) -> ET.Element:
        return ET.Element("to-be-implemented")
