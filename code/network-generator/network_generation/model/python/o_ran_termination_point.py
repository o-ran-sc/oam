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
An abstract Class for O-RAN TerminationPoint
"""
from typing import Any, cast

from network_generation.model.python.o_ran_object import (
    IORanObject,
    ORanObject
)


# Define the "IORanObject" interface
class IORanTerminationPoint(IORanObject):
    supporter: dict[str, str]
    network: Any


default_value: IORanTerminationPoint = cast(
    IORanTerminationPoint,
    {
        **ORanObject.default(),
        **{
            "supporter": {},
            "network": None,
        },
    },
)


# Define an O-RAN Termination Point
# (ietf-interface, onf:logical-termination-point) class
class ORanTerminationPoint(ORanObject):
    @staticmethod
    def default() -> dict[str, Any]:
        return cast(dict[str, Any], default_value)

    def __init__(
        self, data: dict[str, Any] = default(), **kwargs: dict[str, Any]
    ) -> None:
        itp: IORanTerminationPoint = self._to_itp_data(data)
        super().__init__(cast(dict[str, Any], itp), **kwargs)
        self._supporter = cast(dict[str, str], itp["supporter"])
        self._network: Any = itp["network"]
        self._operationalState = cast(dict[str, str], itp["operationalState"])

    def _to_itp_data(self, data: dict[str, Any]) -> IORanTerminationPoint:
        result: IORanTerminationPoint = default_value
        for key, key_type in IORanTerminationPoint.__annotations__.items():
            if key in data:
                result[key] = data[key]  # type: ignore
        return result

    @property
    def host(self) -> str:
        return self.network.host

    @property
    def supporter(self) -> dict[str, str]:
        return self._supporter

    @supporter.setter
    def supporter(self, value: dict[str, str]) -> None:
        self._supporter = value

    @property
    def network(
        self,
    ) -> Any:  # expected is ORanNetwork
        return self._network

    @network.setter
    def network(self, value: Any) -> None:
        self._network = value

    def to_topology(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "tp-id": self.name,
            "o-ran-sc-network:uuid": self.id,
            "o-ran-sc-network:type": self.type,
            "o-ran-sc-network:operational-state": self.operationalState
        }

        if not (self.type == "o-ran-sc-network:phy"):
            result["supporting-termination-point"] = [self.supporter]
        return result

    def to_tmf686_vertex(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "id": self.id,
            "name": self.name,
            "description": f"Description of a vertex object of type {type(self)}",
            "@type": "Vertex",
        }
        if (self.supporter and self.network):
            # TODO self.network!!! network.host
            result = {
                "id": self.id,
                "name": self.name,
                "description": (
                    f'Description of a vertex object of type {type(self)}'),
                "href": (
                    f'https://{self.network.host}/tmf-api/topologyDiscovery/v4/'
                    f'graph/{self.network.id}/vertex/{self.id}'),
                # optional "edge": [],
                "entity": {
                    "id": "indigo",
                    "href": "https://indigo.cosmos-lab.org",
                    "name": "INDIGO",
                    "@baseType": "object",
                    "@schemaLocation": (
                        f'https://{self.network.host}/schema/tmf686-schema.json'
                    ),
                    "@type": "EntityRef",
                    "@referredType": "Individual",
                },
                "graph": {
                    "id": self.network.id,
                    "href": f"https://{self.host}/tmf-api/topologyDiscovery/v4/graph/{self.network.id}",
                    "name": self.network.name,
                    "@baseType": "object",
                    "@schemaLocation": f"https://{self.network.host}/schema/tmf686-schema.json",
                    "@type": "GraphRef",
                    "@referredType": "Graph",
                },
                "subGraph": {
                    # "id": "string",
                    # "href": "string",
                    # "name": "string",
                    # "@baseType": "string",
                    # "@schemaLocation": f'https://{self.network.host}/schema/tmf686-schema.json',
                    # "@type": "string",
                    # "@referredType": "string",
                },
                "vertexCharacteristic": [
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
                    #     "@schemaLocation": f'https://{self.network.host}/schema/tmf686-schema.json',
                    #     "@type": "string",
                    # }
                ],
                "vertexSpecification": {
                    # "id": "string",
                    # "href": "string",
                    # "name": "string",
                    # "version": "string",
                    # "@baseType": "string",
                    # "@schemaLocation": "string",
                    # "@type": "string",
                    # "@referredType": "string",
                },
                "@baseType": "object",
                "@schemaLocation": f"https://{self.network.host}/schema/tmf686-schema.json",
                "@type": "Vertex",
            }
        return result
