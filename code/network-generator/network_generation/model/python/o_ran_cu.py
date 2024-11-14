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
A Class representing an O-RAN centralized unit (ORanCu)
and at the same time a location for an O-Cloud resource pool
"""
import re
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
from network_generation.model.python.tower import Tower

# Define the "IORanCu" interface
IORanCu = IORanNode


# Define an abstract O-RAN Node class
class ORanCu(ORanNode):

    _interfaces = ["e2", "o1"]

    def __init__(
        self,
        data: dict[str, Any] = cast(dict[str, Any], default_value),
        **kwargs: dict[str, Any]
    ) -> None:
        o_ran_cu_data: IORanCu = self._to_o_ran_cu_data(data)
        super().__init__(cast(dict[str, Any], o_ran_cu_data), **kwargs)
        self.type = "o-ran-common-identity-refs:o-cu-function"
        self._o_ran_cloud_dus: list[ORanCloudDu] = self._calculate_o_ran_dus()

    def _to_o_ran_cu_data(self, data: dict[str, Any]) -> IORanCu:
        result: IORanCu = default_value
        for key, key_type in IORanCu.__annotations__.items():
            if key in data:
                result[key] = data[key]  # type: ignore
        return result

    def _calculate_o_ran_dus(self) -> list[ORanCloudDu]:
        hex_ring_radius: int = (
            self.parent.parent.parent.spiral_radius_profile
                .oRanCuSpiralRadiusOfODus
        )
        hex_list: list[Hex] = (
            self.parent.parent.parent.spiral_radius_profile.oRanDuSpiral(
                self.position, hex_ring_radius
            )
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
    def o_ran_cloud_dus(self) -> list[ORanCloudDu]:
        return self._o_ran_cloud_dus

    @property
    def towers(self) -> list[Tower]:
        result: list[Tower] = []
        for du in self.o_ran_cloud_dus:
            for tower in du.towers:
                result.append(tower)
        return result

    def toKml(self) -> ET.Element:
        o_ran_cu = super().toKml()
        for o_ran_cloud_du in self.o_ran_cloud_dus:
            o_ran_cu.append(o_ran_cloud_du.toKml())
        return o_ran_cu

    def toSvg(self) -> ET.Element:
        return ET.Element("to-be-implemented")

    def to_directory(self, parent_dir: str) -> None:
        for o_ran_cloud_du in self.o_ran_cloud_dus:
            o_ran_cloud_du.to_directory(parent_dir)

    def _extend_with_o_ran_cloud_du_references(
        self: Any, super_method: Any, o_ran_cloud_du_method_name: str
    ) -> list[dict[str, Any]]:
        """
        Helper method to extend results with references from o_ran_cloud_dus.

        :param super_method: The superclass method to call for the initial
                             result.
        :param o_ran_cloud_du_method_name: The method name to call on each
                                           o_ran_cloud_du.
        :return: A list of dictionaries with the combined results.
        """
        result = super_method()
        for o_ran_cloud_du in self.o_ran_cloud_dus:
            result.extend(
                self.flatten_list(
                    getattr(o_ran_cloud_du, o_ran_cloud_du_method_name)()
                )
            )
        return result

    def to_topology_nodes(self) -> list[dict[str, Any]]:
        return self._extend_with_o_ran_cloud_du_references(
            super().to_topology_nodes,
            "to_topology_nodes",
        )

    def to_topology_links(self) -> list[dict[str, Any]]:
        interface = "o1"
        destination_node = self.parent.parent
        link_id: str = "".join(
            [interface, ":", self.name, "<->", destination_node.name]
        )
        source_tp: str = "-".join([self.name, interface.upper()])
        dest_tp: str = "-".join([destination_node.name, interface.upper()])
        result = self._extend_with_o_ran_cloud_du_references(
            super().to_topology_links,
            "to_topology_links",
        )
        result.append(
            {
                "link-id": link_id,
                "source": {
                    "source-node": self.name,
                    "source-tp": source_tp,
                },
                "destination": {
                    "dest-node": destination_node.name,
                    "dest-tp": dest_tp,
                },
            }
        )
        return result

    def _extend_teiv_data_with_o_ran_cloud_du_references(
        self: Any,
        teiv_data: dict[str, list[dict[str, Any]]],
        o_ran_cloud_du_method_name: str,
    ) -> dict[str, list[dict[str, Any]]]:
        """ """
        for o_ran_cloud_du in self.o_ran_cloud_dus:
            o_ran_cloud_du_data = getattr(
                o_ran_cloud_du, o_ran_cloud_du_method_name
            )()
            for key, value_list in o_ran_cloud_du_data.items():
                if key not in teiv_data:
                    teiv_data[key] = []
                teiv_data[key].extend(self.flatten_list(value_list))
        return teiv_data

    def add_teiv_data_entities(
            self,
            entity_type: str = "o-ran-smo-teiv-ran:OCUCPFunction",
            attributes: dict[str, Any] = {}
    ) -> dict[str, list[dict[str, Any]]]:
        id = int(re.sub(r"\D", "", self.name))
        id_len = len(str(abs(id)))
        attributes = {
            "gNBCUName": self.name,
            "gNBId": id,
            "gNBIdLength": id_len,
        }
        result = super().add_teiv_data_entities(
            entity_type, attributes
        )
        entity_type = "o-ran-smo-teiv-ran:OCUUPFunction"
        attributes = {
            "gNBId": id,
            "gNBIdLength": id_len,
        }
        o_ran_cuip_data = super().add_teiv_data_entities(
            entity_type, attributes
        )
        for key, value_list in o_ran_cuip_data.items():
            if key not in result:
                result[key] = []
            result[key].extend(self.flatten_list(value_list))
        return self._extend_teiv_data_with_o_ran_cloud_du_references(
            result, "add_teiv_data_entities"
        )

    def add_teiv_data_relationships(
            self,
            id: str = "",
            aside: str = "",
            bside: str = "",
            rel_type: str = "o-ran-smo-teiv-ran:OCUCPFUNCTION_O1LINK_SMO"
    ) -> dict[str, list[dict[str, Any]]]:
        aside = self.name
        bside = self.parent.parent.name
        id = "".join(["o1", ":", aside, ":", bside])
        return self._extend_teiv_data_with_o_ran_cloud_du_references(
            super().add_teiv_data_relationships(id, aside, bside, rel_type),
            "add_teiv_data_relationships",
        )
