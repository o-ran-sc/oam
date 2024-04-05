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
A Class representing an O-RAN centralized unit (ORanCu)
and at the same time a location for an O-Cloud resource pool
"""
import xml.etree.ElementTree as ET
from typing import Any, cast

import network_generation.model.python.hexagon as Hexagon
from network_generation.model.python.geo_location import GeoLocation
from network_generation.model.python.hexagon import Hex
from network_generation.model.python.o_ran_cloud_du import ORanCloudDu
from network_generation.model.python.o_ran_node import (
    IORanNode,
    ORanNode,
    default_value,
)
from network_generation.model.python.o_ran_termination_point import (
    ORanTerminationPoint,
)
from network_generation.model.python.tower import Tower

# Define the "IORanCu" interface
IORanCu = IORanNode


# Define an abstract O-RAN Node class
class ORanCu(ORanNode):
    def __init__(
        self,
        data: dict[str, Any] = cast(dict[str, Any], default_value),
        **kwargs: dict[str, Any]
    ) -> None:
        o_ran_cu_data: IORanCu = self._to_o_ran_cu_data(data)
        super().__init__(cast(dict[str, Any], o_ran_cu_data), **kwargs)
        self._o_ran_cloud_dus: list[ORanCloudDu] = self._calculate_o_ran_dus()

    def _to_o_ran_cu_data(self, data: dict[str, Any]) -> IORanCu:
        result: IORanCu = default_value
        for key, key_type in IORanCu.__annotations__.items():
            if key in data:
                result[key] = data[key]  # type: ignore
        return result

    def _calculate_o_ran_dus(self) -> list[ORanCloudDu]:
        hex_ring_radius: int = (
            self.parent.parent.parent
            .spiral_radius_profile.oRanCuSpiralRadiusOfODus
        )
        hex_list: list[
            Hex
        ] = self.parent.parent.parent.spiral_radius_profile.oRanDuSpiral(
            self.position, hex_ring_radius
        )
        result: list[ORanCloudDu] = []
        for index, hex in enumerate(hex_list):
            s: str = "00" + str(index)
            name: str = "-".join(
                [self.name.replace("CU", "O-Cloud-DU"), s[len(s) - 2: len(s)]]
            )
            network_center: GeoLocation = self.parent.parent.parent.center
            newGeo = Hexagon.hex_to_geo_location(
                self.layout, hex, network_center
            ).json()
            result.append(
                ORanCloudDu(
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
    def o_ran_cloud_dus(self) -> list[ORanCloudDu]:
        return self._o_ran_cloud_dus

    @property
    def towers(self) -> list[Tower]:
        result: list[Tower] = []
        for du in self.o_ran_cloud_dus:
            for tower in du.towers:
                result.append(tower)
        return result

    def termination_points(self) -> list[ORanTerminationPoint]:
        result: list[ORanTerminationPoint] = super().termination_points()
        phy_tp: str = "-".join([self.name, "phy".upper()])
        result.append(ORanTerminationPoint({"tp-id": phy_tp, "name": phy_tp}))
        for interface in ["e2", "o1"]:
            id: str = "-".join([self.name, interface.upper()])
            result.append(
                ORanTerminationPoint(
                    {"id": id, "name": id, "supporter": phy_tp, "parent": self}
                )
            )
        return result

    def to_topology_nodes(self) -> list[dict[str, Any]]:
        result: list[dict[str, Any]] = super().to_topology_nodes()
        # for o_ran_du in self.o_ran_dus: # TODO
        #     result.extend(o_ran_du.to_topology_nodes())
        for o_ran_cloud_du in self.o_ran_cloud_dus:
            result.extend(o_ran_cloud_du.to_topology_nodes())
        return result

    def to_topology_links(self) -> list[dict[str, Any]]:
        result: list[dict[str, Any]] = super().to_topology_links()
        # for o_ran_du in self.o_ran_dus:
        # result.extend(o_ran_du.to_topology_links())
        for o_ran_cloud_du in self.o_ran_cloud_dus:
            result.extend(o_ran_cloud_du.to_topology_links())
        return result

    def toKml(self) -> ET.Element:
        o_ran_cu: ET.Element = ET.Element("Folder")
        open: ET.Element = ET.SubElement(o_ran_cu, "open")
        open.text = "1"
        name: ET.Element = ET.SubElement(o_ran_cu, "name")
        name.text = self.name
        for o_ran_cloud_du in self.o_ran_cloud_dus:
            o_ran_cu.append(o_ran_cloud_du.toKml())
        return o_ran_cu

    def toSvg(self) -> ET.Element:
        return ET.Element("to-be-implemented")

    def to_directory(self, parent_dir: str) -> None:
        for o_ran_cloud_du in self.o_ran_cloud_dus:
            o_ran_cloud_du.to_directory(parent_dir)
