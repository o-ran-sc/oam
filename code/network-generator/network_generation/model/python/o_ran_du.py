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
A Class representing an O-RAN distributed unit (ORanDu)
"""
import os
import re
import xml.etree.ElementTree as ET
from typing import Any, cast

from network_generation.model.python.o_ran_node import IORanNode, ORanNode


# Define the "IORanDu" interface
class IORanDu(IORanNode):
    o_ran_ru_count: int


default_value: IORanDu = cast(
    IORanDu,
    {
        **ORanNode.default(),
        **{"oRanRuCount": 1},
    },
)


# Define an abstract O-RAN Node class
class ORanDu(ORanNode):

    _interfaces = ["e2", "o1", "ofhm", "ofhc", "ofhu", "ofhs"]

    def __init__(
        self,
        data: dict[str, Any] = cast(dict[str, Any], default_value),
        **kwargs: dict[str, Any]
    ) -> None:
        o_ran_du_data: IORanDu = self._to_o_ran_du_data(data)
        super().__init__(cast(dict[str, Any], o_ran_du_data), **kwargs)
        self.type = "o-ran-common-identity-refs:o-du-function"
        self._o_ran_ru_count = (
            o_ran_du_data["oRanRuCount"]
            if o_ran_du_data and "oRanRuCount" in o_ran_du_data
            else 1
        )

    def _to_o_ran_du_data(self, data: dict[str, Any]) -> IORanDu:
        result: IORanDu = default_value
        for key, key_type in IORanDu.__annotations__.items():
            if key in data:
                result[key] = data[key]  # type: ignore
        return result

    def to_topology_nodes(self) -> list[dict[str, Any]]:
        result: list[dict[str, Any]] = super().to_topology_nodes()
        return result

    def to_topology_links(self) -> list[dict[str, Any]]:
        result: list[dict[str, Any]] = super().to_topology_links()
        for interface in ["e2", "o1"]:
            destination_node = self.parent.parent
            if interface == "o1":
                destination_node = self.parent.parent.parent
            link_id: str = "".join(
                [interface, ":", self.name, "<->", destination_node.name]
            )
            source_tp: str = "-".join([self.name, interface.upper()])
            dest_tp: str = "-".join([destination_node.name, interface.upper()])
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

    def toKml(self) -> ET.Element:
        o_ran_du = super().toKml()
        # for tower in self.towers:
        #     o_ran_du.append(tower.toKml())
        return o_ran_du

    def toSvg(self) -> ET.Element:
        return ET.Element("to-be-implemented")

    def to_directory(self, parent_dir: str) -> None:
        parent_path = os.path.join(parent_dir, self.type)
        path = os.path.join(parent_path, self.name)
        if not os.path.exists(parent_path):
            os.makedirs(parent_path, exist_ok=True)
        if not os.path.exists(path):
            os.mkdir(path)

    def to_geojson_feature(self) -> list[dict[str, Any]]:
        return super().to_geojson_feature()

    def to_tmf686_vertex(self) -> list[dict[str, Any]]:
        result: list[dict[str, Any]] = super().to_tmf686_vertex()
        return result

    def to_tmf686_edge(self) -> list[dict[str, Any]]:
        result: list[dict[str, Any]] = super().to_tmf686_edge()
        for interface in ["e2", "o1"]:
            link_id: str = "".join(
                [interface, ":", self.name, "<->", self.parent.name]
            )
            source_tp: str = "-".join([self.name, interface.upper()])
            dest_tp: str = "-".join([self.parent.name, interface.upper()])
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
                            "href": (
                                f'https://{self.host}/tmf-api/topologyDiscovery'
                                f'/v4/graph/{self.network.id}/vertex/{source_tp}'
                            ),
                            "name": source_tp,
                            "@baseType": "object",
                            "@schemaLocation": f"https://{self.host}/schema/tmf686-schema.json",
                            "@type": "VertexRef",
                            "@referredType": "Vertex",
                        },
                        {
                            "id": dest_tp,
                            "href": (
                                f'https://{self.host}/tmf-api/topologyDiscovery'
                                f'/v4/graph/{self.network.id}/vertex/{dest_tp}'
                            ),
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

    def to_tmf633_service_candidate_references(self) -> list[dict[str, Any]]:
        return super().to_tmf633_service_candidate_references()

    def to_tmf633_service_candidates(self) -> list[dict[str, Any]]:
        return super().to_tmf633_service_candidates()

    def to_tmf633_service_specifications(self) -> list[dict[str, Any]]:
        return super().to_tmf633_service_specifications()

    def to_tmf634_resource_candidate_references(self) -> list[dict[str, Any]]:
        return super().to_tmf634_resource_candidate_references()

    def to_tmf634_resource_specification_references(self) -> list[dict[str, Any]]:
        return super().to_tmf634_resource_specification_references()

    def to_tmf634_resource_candidates(self) -> list[dict[str, Any]]:
        return super().to_tmf634_resource_candidates()

    def to_tmf634_resource_specifications(self) -> list[dict[str, Any]]:
        return super().to_tmf634_resource_specifications()

    def add_teiv_data_entities(
            self,
            entity_type: str = "o-ran-smo-teiv-ran:ODUFunction",
            attributes: dict[str, Any] = {}
    ) -> dict[str, list[dict[str, Any]]]:
        id = int(re.sub(r"\D", "", self.name))
        id_len = len(str(abs(id)))
        attributes = {"gNBDUId": id, "gNBId": id, "gNBIdLength": id_len}
        return super().add_teiv_data_entities(
            entity_type, attributes
        )

    def add_teiv_data_relationships(
            self,
            id: str = "",
            aside: str = "",
            bside: str = "",
            rel_type: str = "o-ran-smo-teiv-ran:ODUFUNCTION_O1LINK_SMO"
    ) -> dict[str, list[dict[str, Any]]]:
        result = {}
        aside = self.name
        bside = self.parent.parent.parent.name
        id = "".join(["o1", ":", aside, ":", bside])
        result = super().add_teiv_data_relationships(
            id, aside, bside, rel_type
        )
        aside = self.name
        bside = self.parent.parent.name
        id = "".join(["e2", ":", aside, ":", bside])
        rel_type = "o-ran-smo-teiv-ran:ODUFUNCTION_E2LINK_NEARRTRICFUNCTION"
        rel_data = super().add_teiv_data_relationships(
            id, aside, bside, rel_type
        )
        for key, value_list in rel_data.items():
            if key not in result:
                result[key] = []
            result[key].extend(self.flatten_list(value_list))
        return result
