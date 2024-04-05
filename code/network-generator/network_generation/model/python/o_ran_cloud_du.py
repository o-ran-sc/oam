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
A Class representing an O-RAN O-Cloud resource pool for O-RAN distributed units
(ORanDu).
By default all O-RAN-DUs associated with the towers around  are deployed here.
Maybe dedicated hardware is required to host O-DUs, but it is expected
that the O-Cloud mechanism and concepts can be applied here.
"""
import xml.etree.ElementTree as ET
from typing import Any, cast

import network_generation.model.python.hexagon as Hexagon
from network_generation.model.python.cube import Cube
from network_generation.model.python.geo_location import GeoLocation
from network_generation.model.python.hexagon import Hex
from network_generation.model.python.o_ran_node import (
    IORanNode,
    ORanNode,
    default_value,
)
from network_generation.model.python.o_ran_termination_point import (
    ORanTerminationPoint,
)
from network_generation.model.python.tower import Tower

# Define the "IORanDu" interface
IORanCloudDu = IORanNode


# Implements a concrete O-RAN Node class
class ORanCloudDu(ORanNode):
    def __init__(
        self,
        data: dict[str, Any] = cast(dict[str, Any], default_value),
        **kwargs: dict[str, Any]
    ) -> None:
        o_ran_cloud_du_data: IORanCloudDu = self._to_o_ran_cloud_du_data(data)

        super().__init__(cast(dict[str, Any], o_ran_cloud_du_data), **kwargs)
        self._towers: list[Tower] = self._calculate_towers()

    def _to_o_ran_cloud_du_data(self, data: dict[str, Any]) -> IORanCloudDu:
        result: IORanCloudDu = default_value
        for key, key_type in IORanCloudDu.__annotations__.items():
            if key in data:
                result[key] = data[key]  # type: ignore
        return result

    def _calculate_towers(self) -> list[Tower]:
        hex_ring_radius: int = (
            self.parent.parent.parent.parent
            .spiral_radius_profile.oRanDuSpiralRadiusOfTowers
        )
        hex_list: list[Hex] = Cube.spiral(self.position, hex_ring_radius)
        result: list[Tower] = []
        for index, hex in enumerate(hex_list):
            s: str = "00" + str(index)
            name: str = "-".join(
                [
                    self.name.replace("O-Cloud-DU", "Tower"),
                    s[len(s) - 2: len(s)],
                ]
            )
            network_center: GeoLocation = (
                self.parent.parent.parent.parent.center
            )
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
                        "parent": self,
                    }
                )
            )
        return result

    @property
    def towers(self) -> list[Tower]:
        return self._towers

    def termination_points(self) -> list[ORanTerminationPoint]:
        result: list[ORanTerminationPoint] = super().termination_points()
        phy_tp: str = "-".join([self.name, "phy".upper()])
        result.append(ORanTerminationPoint({"id": phy_tp, "name": phy_tp}))
        for interface in ["o2"]:
            id: str = "-".join([self.name, interface.upper()])
            result.append(
                ORanTerminationPoint(
                    {"id": id, "name": id, "supporter": phy_tp, "parent": self}
                )
            )
        return result

    def to_topology_nodes(self) -> list[dict[str, Any]]:
        result: list[dict[str, Any]] = super().to_topology_nodes()
        for tower in self.towers:
            result.extend(tower.to_topology_nodes())
        return result

    def to_topology_links(self) -> list[dict[str, Any]]:
        result: list[dict[str, Any]] = super().to_topology_links()
        for tower in self.towers:
            result.extend(tower.to_topology_links())
        return result

    def toKml(self) -> ET.Element:
        o_ran_cloud_du: ET.Element = ET.Element("Folder")
        open: ET.Element = ET.SubElement(o_ran_cloud_du, "open")
        open.text = "1"
        name: ET.Element = ET.SubElement(o_ran_cloud_du, "name")
        name.text = self.name
        for tower in self.towers:
            o_ran_cloud_du.append(tower.toKml())
        return o_ran_cloud_du

    def toSvg(self) -> ET.Element:
        return ET.Element("to-be-implemented")

    def to_directory(self, parent_dir: str) -> None:
        for tower in self.towers:
            tower.to_directory(parent_dir)
