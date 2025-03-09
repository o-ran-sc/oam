# Copyright 2025 highstreet technologies USA Corp.
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
from network_generation.model.python.o_ran_ru import ORanRu
from network_generation.model.python.tower import Tower

# Define the "IORanSmo" interface
IORanSmo = IORanNode


# Define an abstract O-RAN Node class
class ORanSmo(ORanNode):
    """
    Class representing an O-RAN Service Management and Operation object.
    """
    _interfaces = ["a1", "o1", "ofhm", "o2"]

    def __init__(
        self,
        data: dict[str, Any] = cast(dict[str, Any], default_value),
        **kwargs: dict[str, Any]
    ) -> None:
        o_ran_smo_data: IORanSmo = self._to_o_ran_smo_data(data)
        super().__init__(cast(dict[str, Any], o_ran_smo_data), **kwargs)
        self.type = "o-ran-sc-network:smo"
        if self.parent is not None:
            self._o_ran_near_rt_rics: list[ORanNearRtRic] = (
                self._calculate_near_rt_rics()
            )

    def _calculate_near_rt_rics(self) -> list[ORanNearRtRic]:
        hex_ring_radius: int = (
            self.parent.spiral_radius_profile.oRanSmoSpiralRadiusOfNearRtRics
            if self.parent is not None
            else 1
        )
        hex_list: list[Hex] = (
            self.parent.spiral_radius_profile.oRanNearRtRicSpiral(
                self.position, hex_ring_radius
            )
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
                        "geoLocation": GeoLocation(newGeo),
                        "position": hex,
                        "layout": self.layout,
                        "parent": self,
                        "network": self.network,
                        "operationalState": self.operationalState
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

    @property
    def rus(self) -> list[ORanRu]:
        result: list[ORanRu] = []
        for ric in self.o_ran_near_rt_rics:
            for tower in ric.towers:
                result.extend(tower.o_ran_rus)
        return result

    def toKml(self) -> ET.Element:
        smo = super().toKml()
        for ric in self.o_ran_near_rt_rics:
            smo.append(ric.toKml())
        return smo

    def toSvg(self) -> ET.Element:
        return ET.Element("not-implemented-yet-TODO")

    def to_directory(self, parent_dir: str) -> None:
        for ric in self.o_ran_near_rt_rics:
            ric.to_directory(parent_dir)

    def _extend_with_ric_references(
        self: Any, super_method: Any, ric_method_name: str
    ) -> list[dict[str, Any]]:
        """
        Helper method to extend results with references from
        o_ran_near_rt_rics.

        :param super_method: The superclass method to call for the initial
                             result.
        :param ric_method_name: The method name to call on each ric.
        :return: A list of dictionaries with the combined results.
        """
        result = super_method()
        for ric in self.o_ran_near_rt_rics:
            result.extend(self.flatten_list(getattr(ric, ric_method_name)()))
        return result

    def to_topology_nodes(self) -> list[dict[str, Any]]:
        return self._extend_with_ric_references(
            super().to_topology_nodes, "to_topology_nodes"
        )

    def to_topology_links(self) -> list[dict[str, Any]]:
        return self._extend_with_ric_references(
            super().to_topology_links, "to_topology_links"
        )

    def to_tmf686_vertex(self) -> list[dict[str, Any]]:
        return self._extend_with_ric_references(
            super().to_tmf686_vertex, "to_tmf686_vertex")

    def to_tmf686_edge(self) -> list[dict[str, Any]]:
        return self._extend_with_ric_references(
            super().to_tmf686_edge, "to_tmf686_edge")

    def to_geojson_feature(self) -> list[dict[str, Any]]:
        return self._extend_with_ric_references(
            super().to_geojson_feature, "to_geojson_feature")

    def to_tmf633_service_candidate_references(self) -> list[dict[str, Any]]:
        return self._extend_with_ric_references(
            super().to_tmf633_service_candidate_references,
            "to_tmf633_service_candidate_references")

    def to_tmf633_service_candidates(self) -> list[dict[str, Any]]:
        return self._extend_with_ric_references(
            super().to_tmf633_service_candidates,
            "to_tmf633_service_candidates")

    def to_tmf633_service_specifications(self) -> list[dict[str, Any]]:
        return self._extend_with_ric_references(
            super().to_tmf633_service_specifications,
            "to_tmf633_service_specifications")

    def to_tmf634_resource_candidate_references(self) -> list[dict[str, Any]]:
        return self._extend_with_ric_references(
            super().to_tmf634_resource_candidate_references,
            "to_tmf634_resource_candidate_references")

    def to_tmf634_resource_specification_references(self) -> list[dict[str, Any]]:
        return self._extend_with_ric_references(
            super().to_tmf634_resource_specification_references,
            "to_tmf634_resource_specification_references")

    def to_tmf634_resource_candidates(self) -> list[dict[str, Any]]:
        return self._extend_with_ric_references(
            super().to_tmf634_resource_candidates,
            "to_tmf634_resource_candidates")

    def to_tmf634_resource_specifications(self) -> list[dict[str, Any]]:
        return self._extend_with_ric_references(
            super().to_tmf634_resource_specifications,
            "to_tmf634_resource_specifications")

    def _extend_teiv_data_with_ric_references(
        self: Any,
        teiv_data: dict[str, list[dict[str, Any]]],
        ric_method_name: str
    ) -> dict[str, list[dict[str, Any]]]:
        """ """
        for ric in self.o_ran_near_rt_rics:
            ric_data = getattr(ric, ric_method_name)()
            for key, value_list in ric_data.items():
                if key not in teiv_data:
                    teiv_data[key] = []
                teiv_data[key].extend(self.flatten_list(value_list))
        return teiv_data

    def add_teiv_data_entities(
            self,
            entity_type: str = "o-ran-smo-teiv-ran:SMO",
            attributes: dict[str, Any] = {}
    ) -> dict[str, list[dict[str, Any]]]:
        attributes = {
            "smoName": self.name
        }
        return self._extend_teiv_data_with_ric_references(
            super().add_teiv_data_entities(entity_type, attributes),
            "add_teiv_data_entities"
        )

    def add_teiv_data_relationships(
            self,
            id: str = "",
            aside: str = "",
            bside: str = "",
            rel_type: str = ""
    ) -> dict[str, list[dict[str, Any]]]:
        return self._extend_teiv_data_with_ric_references(
            {}, "add_teiv_data_relationships"
        )
