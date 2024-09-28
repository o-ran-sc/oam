# Copyright 2024 highstreet technologies
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

# !/usr/bin/python3

"""
A Class representing an O-RAN Near real-time intelligent controller
(ORanNearRtRic)
"""
import xml.etree.ElementTree as ET
from typing import Any, cast

import network_generation.model.python.hexagon as Hexagon
from network_generation.model.python.geo_location import GeoLocation
from network_generation.model.python.hexagon import Hex
from network_generation.model.python.o_ran_cu import ORanCu
from network_generation.model.python.o_ran_node import (
    IORanNode,
    ORanNode,
    default_value,
)
from network_generation.model.python.tower import Tower

# Define the "IORanNearRtRic" interface
IORanNearRtRic = IORanNode


# Define an abstract O-RAN Node class
class ORanNearRtRic(ORanNode):

    _interfaces = ["e2", "o1", "ofhm", "ofhc", "ofhu", "ofhs"]

    def __init__(
        self,
        data: dict[str, Any] = cast(dict[str, Any], default_value),
        **kwargs: dict[str, Any]
    ) -> None:
        o_ran_near_rt_ric_data: IORanNearRtRic = (
            self._to_o_ran_near_rt_ric_data(data)
        )
        super().__init__(
            cast(dict[str, Any], o_ran_near_rt_ric_data), **kwargs
        )
        self.type = "o-ran-sc-network:near-rt-ric"
        self._o_ran_cus: list[ORanCu] = self._calculate_o_ran_cus()

    def _to_o_ran_near_rt_ric_data(
        self, data: dict[str, Any]
    ) -> IORanNearRtRic:
        result: IORanNearRtRic = default_value
        for key, key_type in IORanNearRtRic.__annotations__.items():
            if key in data:
                result[key] = data[key]  # type: ignore
        return result

    def _calculate_o_ran_cus(self) -> list[ORanCu]:
        hex_ring_radius: int = (
            self.parent.parent.spiral_radius_profile
                .oRanNearRtRicSpiralRadiusOfOCus
        )
        hex_list: list[Hex] = (
            self.parent.parent.spiral_radius_profile.oRanCuSpiral(
                self.position, hex_ring_radius
            )
        )
        result: list[ORanCu] = []
        for index, hex in enumerate(hex_list):
            s: str = "00" + str(index)
            name: str = "-".join(
                [self.name.replace("NearRtRic", "CU"), s[len(s) - 2: len(s)]]
            )
            network_center: GeoLocation = self.parent.parent.center
            newGeo = Hexagon.hex_to_geo_location(
                self.layout, hex, network_center
            ).json()
            result.append(
                ORanCu(
                    {
                        "name": name,
                        "geoLocation": newGeo,
                        "position": hex,
                        "layout": self.layout,
                        "parent": self,
                        "network": self.network,
                    }
                )
            )
        return result

    @property
    def o_ran_cus(self) -> list[ORanCu]:
        return self._o_ran_cus

    @property
    def towers(self) -> list[Tower]:
        result: list[Tower] = []
        for cu in self.o_ran_cus:
            for tower in cu.towers:
                result.append(tower)
        return result

    def toKml(self) -> ET.Element:
        ric: ET.Element = ET.Element("Folder")
        open: ET.Element = ET.SubElement(ric, "open")
        open.text = "1"
        name: ET.Element = ET.SubElement(ric, "name")
        name.text = self.name
        for o_ran_cu in self.o_ran_cus:
            ric.append(o_ran_cu.toKml())
        return ric

    def toSvg(self) -> ET.Element:
        return ET.Element("to-be-implemented")

    def to_directory(self, parent_dir: str) -> None:
        for o_ran_cu in self.o_ran_cus:
            o_ran_cu.to_directory(parent_dir)

    def _extend_with_o_ran_cu_references(
        self: Any, super_method: Any, o_ran_cu_method_name: str
    ) -> list[dict[str, Any]]:
        """
        Helper method to extend results with references from o_ran_cus.

        :param super_method: The superclass method to call for the initial
                             result.
        :param o_ran_cu_method_name: The method name to call on each o_ran_cu.
        :return: A list of dictionaries with the combined results.
        """
        result = super_method()
        for o_ran_cu in self.o_ran_cus:
            result.extend(
                self.flatten_list(getattr(o_ran_cu, o_ran_cu_method_name)())
            )
        return result

    def to_topology_nodes(self) -> list[dict[str, Any]]:
        return self._extend_with_o_ran_cu_references(
            super().to_topology_nodes, "to_topology_nodes"
        )

    def to_topology_links(self) -> list[dict[str, Any]]:
        return self._extend_with_o_ran_cu_references(
            super().to_topology_links, "to_topology_links"
        )
