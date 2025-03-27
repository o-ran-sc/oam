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
A Class representing an O-RAN radio unit (ORanRu)
"""
import os
import re
import xml.etree.ElementTree as ET
from typing import Any, cast

from network_generation.model.python.nr_cell_du import NrCellDu
from network_generation.model.python.o_ran_du import ORanDu
from network_generation.model.python.o_ran_node import IORanNode, ORanNode


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

    _interfaces = ["ofhc", "ofhu", "ofhs", "ofhm"]

    def __init__(
        self,
        data: dict[str, Any] = cast(dict[str, Any], default_value),
        **kwargs: dict[str, Any],
    ) -> None:
        o_ran_ru_data: IORanRu = self._to_o_ran_ru_data(data)
        super().__init__(cast(dict[str, Any], o_ran_ru_data), **kwargs)
        self.type = "o-ran-common-identity-refs:o-ru-function"
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
            "network": self.network,
            "operationalState": self.operationalState,
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
            self.parent.parent.parent.parent.parent.parent.configuration[
                "pattern"]["nrCellDu"]
        )
        cell_angle: int = cell_config["cellAngle"]
        cell_scale_factor: int = cell_config["cellScaleFactorForHandoverArea"]
        maxReach: int = cell_config["maxReach"]
        for index in range(self._cell_count):
            s: str = "00" + str(index)
            name: str = "-".join(
                [self.name, s[len(s) - 2: len(s)], "CELL"]
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
                        "network": self.network,
                        "operationalState": self.operationalState,
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

    def to_topology_nodes(self) -> list[dict[str, Any]]:
        # cells should be interpreted as termination points
        for cell in self.cells:
            cell_tp = cell.to_termination_point()
            self.termination_points().append(cell_tp)
        result: list[dict[str, Any]] = super().to_topology_nodes()
        result.extend(self.oRanDu.to_topology_nodes())
        return result

    def to_tmf686_vertex(self) -> list[dict[str, Any]]:
        result: list[dict[str, Any]] = super().to_tmf686_vertex()
        result.extend(self.oRanDu.to_tmf686_vertex())
        return result

    def to_topology_links(self) -> list[dict[str, Any]]:
        result: list[dict[str, Any]] = super().to_topology_links()
        result.extend(self.oRanDu.to_topology_links())
        for interface in ["phy", "ofhm", "ofhc", "ofhu", "ofhs"]:
            link_id: str = "".join([interface, ":", self.name, "<->", self.oRanDu.name])
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
        # The O-RU 'creates' the O-DUs
        # therefore the O-RU returns is "wrapper" too
        o_ran_du = self.oRanDu.toKml()
        o_ran_ru = super().toKml()
        for cell in self.cells:
            o_ran_ru.append(cell.toKml())
        o_ran_du.append(o_ran_ru)
        return o_ran_du

    def toSvg(self) -> ET.Element:
        return ET.Element("to-be-implemented")

    def to_directory(self, parent_dir: str) -> None:
        self.oRanDu.to_directory(parent_dir)
        parent_path = os.path.join(parent_dir, self.type)
        path = os.path.join(parent_path, self.name)
        if not os.path.exists(parent_path):
            os.makedirs(parent_path, exist_ok=True)
        if not os.path.exists(path):
            os.mkdir(path)

    def _extend_with_cell_references(
        self: Any, super_method: Any, cell_method_name: str
    ) -> list[dict[str, Any]]:
        """
        Helper method to extend results with references from cells.

        :param super_method: The superclass method to call for the initial result.
        :param cell_method_name: The method name to call on each cell.
        :return: A list of dictionaries with the combined results.
        """
        result = super_method()
        result.extend(getattr(self.oRanDu, cell_method_name)())
        for cell in self.cells:
            result.extend(self.flatten_list(getattr(cell, cell_method_name)()))
        return result

    def to_geojson_feature(self) -> list[dict[str, Any]]:
        return self._extend_with_cell_references(
            super().to_geojson_feature,
            "to_geojson_feature",
        )

    def to_tmf686_vertex(self) -> list[dict[str, Any]]:
        result: list[dict[str, Any]] = super().to_tmf686_vertex()
        result.extend(self.oRanDu.to_tmf686_vertex())
        return result

    def to_tmf686_edge(self) -> list[dict[str, Any]]:
        result: list[dict[str, Any]] = super().to_topology_links()
        result.extend(self.oRanDu.to_topology_links())
        for interface in ["phy", "ofhm", "ofhc", "ofhu", "ofhs"]:
            link_id: str = "".join([interface, ":", self.name, "<->", self.oRanDu.name])
            source_tp: str = "-".join([self.name, interface.upper()])
            dest_tp: str = "-".join([self.oRanDu.name, interface.upper()])
            result.append(
                {
                    "id": link_id,
                    "href": f"https://{self.host}/tmf-api/topologyDiscovery/v4/graph/{self.network.id}/edge/{link_id}",
                    "bidirectional": True,
                    "description": "Description of an edge object",
                    "name": self.name,
                    "edgeCharacteristic": [
                        # {
                        #     "id": "string",
                        #     "name": "string",
                        #     "valueType": "string",
                        #     "characteristicRelationship": [
                        #         {
                        #             "id": "string",
                        #             "href": "string",
                        #             "relationshipType": "string",
                        #             "@baseType": "string",
                        #             "@schemaLocation": "string",
                        #             "@type": "string",
                        #         }
                        #     ],
                        #     "value": "string",
                        #     "@baseType": "string",
                        #     "@schemaLocation": "string",
                        #     "@type": "string",
                        # }
                    ],
                    "edgeSpecification": {
                        # "id": "string",
                        # "href": "string",
                        # "name": "string",
                        # "version": "string",
                        # "@baseType": "string",
                        # "@schemaLocation": "string",
                        # "@type": "string",
                        # "@referredType": "string",
                    },
                    "entity": {
                        "id": "indigo",
                        "href": "https://indigo.cosmos-lab.org",
                        "name": "INDIGO",
                        "@baseType": "object",
                        "@schemaLocation": f"https://{self.host}/schema/tmf686-schema.json",
                        "@type": "EntityRef",
                        "@referredType": "Individual",
                    },
                    "graph": {
                        "id": self.network.id,
                        "href": f"https://{self.host}/tmf-api/topologyDiscovery/v4/graph/{self.network.id}",
                        "name": self.network.name,
                        "@baseType": "object",
                        "@schemaLocation": f"https://{self.host}/schema/tmf686-schema.json",
                        "@type": "GraphRef",
                        "@referredType": "Graph",
                    },
                    "subGraph": {
                        # "id": "string",
                        # "href": "string",
                        # "name": "string",
                        # "@baseType": "string",
                        # "@schemaLocation": "string",
                        # "@type": "string",
                        # "@referredType": "string",
                    },
                    "vertex": [
                        {
                            "id": source_tp,
                            "href": f"https://{self.host}/tmf-api/topologyDiscovery/v4/graph/{self.network.id}/vertex/{source_tp}",
                            "name": source_tp,
                            "@baseType": "object",
                            "@schemaLocation": f"https://{self.host}/schema/tmf686-schema.json",
                            "@type": "VertexRef",
                            "@referredType": "Vertex",
                        },
                        {
                            "id": dest_tp,
                            "href": f"https://{self.host}/tmf-api/topologyDiscovery/v4/graph/{self.network.id}/vertex/{dest_tp}",
                            "name": dest_tp,
                            "@baseType": "object",
                            "@schemaLocation": f"https://{self.host}/schema/tmf686-schema.json",
                            "@type": "VertexRef",
                            "@referredType": "Vertex",
                        },
                    ],
                    "@baseType": "object",
                    "@schemaLocation": f"https://{self.host}/schema/tmf686-schema.json",
                    "@type": "Edge",
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

    def to_directory(self, parent_dir: str) -> None:
        self.oRanDu.to_directory(parent_dir)
        parent_path = os.path.join(parent_dir, self.type)
        path = os.path.join(parent_path, self.name)
        if not os.path.exists(parent_path):
            os.makedirs(parent_path, exist_ok=True)
        if not os.path.exists(path):
            os.mkdir(path)

    def _extend_with_cell_references(
        self: Any, super_method: Any, cell_method_name: str
    ) -> list[dict[str, Any]]:
        """
        Helper method to extend results with references from cells.

        :param super_method: The superclass method to call for the initial result.
        :param cell_method_name: The method name to call on each cell.
        :return: A list of dictionaries with the combined results.
        """
        result = super_method()
        result.extend(getattr(self.oRanDu, cell_method_name)())
        for cell in self.cells:
            result.extend(self.flatten_list(getattr(cell, cell_method_name)()))
        return result

    def to_geojson_feature(self) -> list[dict[str, Any]]:
        return self._extend_with_cell_references(
            super().to_geojson_feature,
            "to_geojson_feature",
        )

    def to_tmf633_service_candidate_references(self) -> list[dict[str, Any]]:
        return self._extend_with_cell_references(
            super().to_tmf633_service_candidate_references,
            "to_tmf633_service_candidate_references",
        )

    def to_tmf633_service_candidates(self) -> list[dict[str, Any]]:
        return self._extend_with_cell_references(
            super().to_tmf633_service_candidates,
            "to_tmf633_service_candidates",
        )

    def to_tmf633_service_specifications(self) -> list[dict[str, Any]]:
        return self._extend_with_cell_references(
            super().to_tmf633_service_specifications,
            "to_tmf633_service_specifications",
        )

    def to_tmf634_resource_candidate_references(self) -> list[dict[str, Any]]:
        return self._extend_with_cell_references(
            super().to_tmf634_resource_candidate_references,
            "to_tmf634_resource_candidate_references",
        )

    def to_tmf634_resource_specification_references(self) -> list[dict[str, Any]]:
        return self._extend_with_cell_references(
            super().to_tmf634_resource_specification_references,
            "to_tmf634_resource_specification_references",
        )

    def to_tmf634_resource_candidates(self) -> list[dict[str, Any]]:
        return self._extend_with_cell_references(
            super().to_tmf634_resource_candidates, "to_tmf634_resource_candidates"
        )

    def to_tmf634_resource_specifications(self) -> list[dict[str, Any]]:
        return self._extend_with_cell_references(
            super().to_tmf634_resource_specifications,
            "to_tmf634_resource_specifications",
        )

    def add_teiv_data_entities(
            self,
            entity_type: str = "o-ran-smo-teiv-ran:ORUFunction",
            attributes: dict[str, Any] = {}
    ) -> dict[str, list[dict[str, Any]]]:
        id = int(re.sub(r"\D", "", self.name))
        attributes = {"oruId": id}
        result = super().add_teiv_data_entities(
            entity_type, attributes
        )
        o_ran_du_data = self.oRanDu.add_teiv_data_entities()
        for key, value_list in o_ran_du_data.items():
            if key not in result:
                result[key] = []
            result[key].extend(self.flatten_list(value_list))
        for cell in self._cells:
            cell_data = cell.add_teiv_data_entities()
            for key, value_list in cell_data.items():
                if key not in result:
                    result[key] = []
                result[key].extend(self.flatten_list(value_list))
        return result

    def add_teiv_data_relationships(
            self,
            id: str = "",
            aside: str = "",
            bside: str = "",
            rel_type: str = "",
    ) -> dict[str, list[dict[str, Any]]]:
        result = {}
        result = self.oRanDu.add_teiv_data_relationships()
        for interface in ["OFHM", "OFHC", "OFHU", "OFHS"]:
            aside = self.name
            bside = self.oRanDu.name
            id = "".join([interface, ":", aside, ":", bside])
            rel_type = (
                f"o-ran-smo-teiv-ran:ORUFUNCTION_{interface}LINK_ODUFUNCTION"
            )
            rel_data = super().add_teiv_data_relationships(
                id, aside, bside, rel_type
            )
            for key, value_list in rel_data.items():
                if key not in result:
                    result[key] = []
                result[key].extend(self.flatten_list(value_list))
        return result
