# Copyright 2024 highstreet technologies USA CORP.
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
from network_generation.model.python.tower import Tower

# Define the "IORanDu" interface
IORanCloudDu = IORanNode


# Implements a concrete O-RAN Node class
class ORanCloudDu(ORanNode):

    _interfaces = ["o2"]

    def __init__(
        self,
        data: dict[str, Any] = cast(dict[str, Any], default_value),
        **kwargs: dict[str, Any]
    ) -> None:
        o_ran_cloud_du_data: IORanCloudDu = self._to_o_ran_cloud_du_data(data)

        super().__init__(cast(dict[str, Any], o_ran_cloud_du_data), **kwargs)
        self.type = "o-ran-sc-network:o-cloud"
        self._towers: list[Tower] = self._calculate_towers()

    def _to_o_ran_cloud_du_data(self, data: dict[str, Any]) -> IORanCloudDu:
        result: IORanCloudDu = default_value
        for key, key_type in IORanCloudDu.__annotations__.items():
            if key in data:
                result[key] = data[key]  # type: ignore
        return result

    def _calculate_towers(self) -> list[Tower]:
        hex_ring_radius: int = (
            self.parent.parent.parent.parent.spiral_radius_profile
                .oRanDuSpiralRadiusOfTowers
        )
        hex_list: list[Hex] = Cube.spiral(
            self.position, hex_ring_radius)
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
                        "geoLocation": GeoLocation(newGeo),
                        "position": hex,
                        "layout": self.layout,
                        "parent": self,
                        "network": self.network,
                    }
                )
            )
        return result

    @property
    def towers(self) -> list[Tower]:
        return self._towers

    def toKml(self) -> ET.Element:
        o_ran_cloud_du = super().toKml()
        for tower in self.towers:
            o_ran_cloud_du.append(tower.toKml())
        return o_ran_cloud_du

    def toSvg(self) -> ET.Element:
        return ET.Element("to-be-implemented")

    def to_directory(self, parent_dir: str) -> None:
        for tower in self.towers:
            tower.to_directory(parent_dir)

    def _extend_with_tower_references(
        self: Any, super_method: Any, tower_method_name: str
    ) -> list[dict[str, Any]]:
        """
        Helper method to extend results with references from towers.

        :param super_method: The superclass method to call for the initial
               result.
        :param tower_method_name: The method name to call on each tower.
        :return: A list of dictionaries with the combined results.
        """
        result = super_method()
        for tower in self.towers:
            result.extend(
                self.flatten_list(getattr(tower, tower_method_name)())
            )
        return result

    def to_topology_nodes(self) -> list[dict[str, Any]]:
        return self._extend_with_tower_references(
            super().to_topology_nodes,
            "to_topology_nodes",
        )

    def to_topology_links(self) -> list[dict[str, Any]]:
        return self._extend_with_tower_references(
            super().to_topology_links,
            "to_topology_links",
        )

    def _extend_teiv_data_with_tower_references(
        self: Any, tower_method_name: str
    ) -> dict[str, list[dict[str, Any]]]:
        """ """
        result: dict[str, Any] = {}
        for tower in self.towers:
            tower_data = getattr(tower, tower_method_name)()
            for key, value_list in tower_data.items():
                if key not in result:
                    result[key] = []
                result[key].extend(self.flatten_list(value_list))
        return result

    def add_teiv_data_entities(
            self,
            entity_type: str = "",
            attributes: dict[str, Any] = {}
    ) -> dict[str, list[dict[str, Any]]]:
        return self._extend_teiv_data_with_tower_references(
            "add_teiv_data_entities"
        )

    def add_teiv_data_relationships(
            self,
            id: str = "",
            aside: str = "",
            bside: str = "",
            rel_type: str = ""
    ) -> dict[str, list[dict[str, Any]]]:
        return self._extend_teiv_data_with_tower_references(
            "add_teiv_data_relationships"
        )
