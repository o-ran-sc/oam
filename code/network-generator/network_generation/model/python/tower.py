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
A Class representing a Tower to mount O-RAN RUs
It can be interpreted as 'resource pool' for physical network
functions.
"""
import xml.etree.ElementTree as ET
from typing import Any, cast

from network_generation.model.python.o_ran_node import IORanNode, ORanNode
from network_generation.model.python.o_ran_ru import ORanRu


# Define the "IoRanDu" interface
class ITower(IORanNode):
    o_ran_ru_count: int


default_value: ITower = cast(
    ITower,
    {
        **ORanNode.default(),
        **{
            "o_ran_ru_count": 1,
        },
    },
)


# Implement a concrete O-RAN Node class
class Tower(ORanNode):

    _interfaces = ["o2"]

    def __init__(
        self,
        data: dict[str, Any] = cast(dict[str, Any], default_value),
        **kwargs: dict[str, Any]
    ) -> None:
        tower_data: ITower = self._to_tower_data(data)
        super().__init__(cast(dict[str, Any], tower_data), **kwargs)
        self.type = "o-ran-sc-network:tower"
        self._o_ran_ru_count: int = (
            int(str(tower_data["oRanRuCount"]))
            if tower_data and "oRanRuCount" in tower_data
            else 3
        )
        self._o_ran_rus: list[ORanRu] = self._create_o_ran_rus()

    def _to_tower_data(self, data: dict[str, Any]) -> ITower:
        result: ITower = default_value
        for key, key_type in ITower.__annotations__.items():
            if key in data:
                result[key] = data[key]  # type: ignore
        return result

    def _create_o_ran_rus(self) -> list[ORanRu]:
        result: list[ORanRu] = []
        for index in range(self._o_ran_ru_count):
            s: str = "00" + str(index)
            name: str = "-".join(
                [self.name.replace("Tower", "RU"), s[len(s) - 2: len(s)]]
            )
            cell_count: int = (
                self.parent.parent.parent.parent.parent.configuration[
                    "pattern"
                ]["oRanRu"]["nrCellDuCount"]
            )
            cell_angle: int = (
                self.parent.parent.parent.parent.parent.configuration[
                    "pattern"
                ]["nrCellDu"]["cellAngle"]
            )
            ru_angle: int = cell_count * cell_angle
            ru_azimuth: int = index * ru_angle
            result.append(
                ORanRu(
                    {
                        "name": name,
                        "geoLocation": self.geo_location,
                        "position": self.position,
                        "layout": self.layout,
                        "parent": self,
                        "network": self.network,
                        "cellCount": cell_count,
                        "ruAngle": ru_angle,
                        "ruAzimuth": ru_azimuth,
                    }
                )
            )
        return result

    @property
    def o_ran_rus(self) -> list[ORanRu]:
        return self._o_ran_rus

    def toKml(self) -> ET.Element:
        tower = super().toKml()
        for o_ran_ru in self.o_ran_rus:
            tower.append(o_ran_ru.toKml())
        return tower

    def toSvg(self) -> ET.Element:
        return ET.Element("to-be-implemented")

    def to_directory(self, parent_dir: str) -> None:
        for o_ran_ru in self.o_ran_rus:
            o_ran_ru.to_directory(parent_dir)

    def _extend_with_o_ran_ru_references(
        self: Any, super_method: Any, o_ran_ru_method_name: str
    ) -> list[dict[str, Any]]:
        """
        Helper method to extend results with references from o_ran_rus.

        :param super_method: The superclass method to call for the initial
                             result.
        :param o_ran_ru_method_name: The method name to call on each o_ran_ru.
        :return: A list of dictionaries with the combined results.
        """
        result = super_method()
        for o_ran_ru in self.o_ran_rus:
            result.extend(
                self.flatten_list(getattr(o_ran_ru, o_ran_ru_method_name)())
            )
        return result

    def to_topology_nodes(self) -> list[dict[str, Any]]:
        return self._extend_with_o_ran_ru_references(
            super().to_topology_nodes,
            "to_topology_nodes",
        )

    def to_topology_links(self) -> list[dict[str, Any]]:
        return self._extend_with_o_ran_ru_references(
            super().to_topology_links,
            "to_topology_links",
        )

    def _extend_teiv_data_with_o_ran_ru_references(
        self: Any, o_ran_ru_method_name: str
    ) -> dict[str, list[dict[str, Any]]]:
        """ """
        result: dict[str, Any] = {}
        for o_ran_ru in self.o_ran_rus:
            o_ran_ru_data = getattr(o_ran_ru, o_ran_ru_method_name)()
            for key, value_list in o_ran_ru_data.items():
                if key not in result:
                    result[key] = []
                result[key].extend(self.flatten_list(value_list))
        return result

    def add_teiv_data_entities(
            self,
            entity_type: str = "",
            attributes: dict[str, Any] = {}
    ) -> dict[str, list[dict[str, Any]]]:
        return self._extend_teiv_data_with_o_ran_ru_references(
            "add_teiv_data_entities"
        )

    def add_teiv_data_relationships(
            self,
            id: str = "",
            aside: str = "",
            bside: str = "",
            rel_type: str = "",
    ) -> dict[str, list[dict[str, Any]]]:
        return self._extend_teiv_data_with_o_ran_ru_references(
            "add_teiv_data_relationships"
        )
