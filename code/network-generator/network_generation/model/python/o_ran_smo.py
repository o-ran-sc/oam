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
A Class representing an O-RAN Service Management and
Orchestration Framework (SMO)
"""
import xml.etree.ElementTree as ET
from typing import Any, cast

import network_generation.model.python.hexagon as Hexagon
from network_generation.model.python.geo_location import GeoLocation
from network_generation.model.python.hexagon import Hex
from network_generation.model.python.o_ran_near_rt_ric import ORanNearRtRic
from network_generation.model.python.o_ran_node import (
    IORanNode,
    ORanNode,
    default_value,
)
from network_generation.model.python.o_ran_termination_point import (
    ORanTerminationPoint,
)
from network_generation.model.python.tower import Tower

# Define the "IORanSmo" interface
IORanSmo = IORanNode


# Define an abstract O-RAN Node class
class ORanSmo(ORanNode):
    """
    Class representing an O-RAN Service Management and Operation object.
    """

    def __init__(
        self,
        data: dict[str, Any] = cast(dict[str, Any], default_value),
        **kwargs: dict[str, Any]
    ) -> None:
        o_ran_smo_data: IORanSmo = self._to_o_ran_smo_data(data)
        super().__init__(cast(dict[str, Any], o_ran_smo_data), **kwargs)
        if self.parent is not None:
            self._o_ran_near_rt_rics: list[
                ORanNearRtRic
            ] = self._calculate_near_rt_rics()

    def _calculate_near_rt_rics(self) -> list[ORanNearRtRic]:
        hex_ring_radius: int = (
            self.parent.spiral_radius_profile.oRanSmoSpiralRadiusOfNearRtRics
            if self.parent is not None
            else 1
        )
        hex_list: list[
            Hex
        ] = self.parent.spiral_radius_profile.oRanNearRtRicSpiral(
            self.position, hex_ring_radius
        )
        result: list[ORanNearRtRic] = []
        for index, hex in enumerate(hex_list):
            s: str = "00" + str(index)
            name: str = "-".join(
                [self.name.replace("SMO", "NearRtRic"), s[len(s) - 2: len(s)]]
            )
            network_center: GeoLocation = self.parent.center
            newGeo = Hexagon.hex_to_geo_location(
                self.layout, hex, network_center
            ).json()
            result.append(
                ORanNearRtRic(
                    {
                        "name": name,
                        "geoLocation": newGeo,
                        "position": hex,
                        "layout": self.layout,
                        "parent": self,
                    },
                )
            )
        return result

    def _to_o_ran_smo_data(self, data: dict[str, Any]) -> IORanSmo:
        result: IORanSmo = default_value
        for key, key_type in IORanSmo.__annotations__.items():
            if key in data:
                result[key] = data[key]  # type: ignore
        return result

    @property
    def o_ran_near_rt_rics(self) -> list[ORanNearRtRic]:
        return self._o_ran_near_rt_rics

    @property
    def towers(self) -> list[Tower]:
        result: list[Tower] = []
        for ric in self.o_ran_near_rt_rics:
            for tower in ric.towers:
                result.append(tower)
        return result

    # @property
    def termination_points(self) -> list[ORanTerminationPoint]:
        result: list[ORanTerminationPoint] = super().termination_points()
        phy_tp: str = "-".join([self.name, "phy".upper()])
        result.append(ORanTerminationPoint({"id": phy_tp, "name": phy_tp}))
        for interface in ["a1", "o1", "o2"]:
            id: str = "-".join([self.name, interface.upper()])
            result.append(
                ORanTerminationPoint(
                    {
                        "id": id,
                        "name": id,
                        "supporter": phy_tp,
                        "parent": self,
                    },
                )
            )
        return result

    def to_topology_nodes(self) -> list[dict[str, Any]]:
        result: list[dict[str, Any]] = super().to_topology_nodes()
        for ric in self.o_ran_near_rt_rics:
            result.extend(ric.to_topology_nodes())
        return result

    def to_topology_links(self) -> list[dict[str, Any]]:
        result: list[dict[str, Any]] = []  # super().to_topology_links()
        for ric in self.o_ran_near_rt_rics:
            result.extend(ric.to_topology_links())
        return result

    def toKml(self) -> ET.Element:
        smo: ET.Element = ET.Element("Folder")
        open: ET.Element = ET.SubElement(smo, "open")
        open.text = "1"
        name: ET.Element = ET.SubElement(smo, "name")
        name.text = self.name
        for ric in self.o_ran_near_rt_rics:
            smo.append(ric.toKml())
        return smo

    def toSvg(self) -> ET.Element:
        return ET.Element("not-implemented-yet-TODO")
