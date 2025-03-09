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
An abstract Class for O-RAN Node
"""
import uuid
import xml.etree.ElementTree as ET
from abc import abstractmethod
from datetime import datetime, timezone
from typing import Any, cast

import network_generation.model.python.hexagon as Hexagon
from network_generation.model.python.countries import Country
from network_generation.model.python.geo_location import (
    GeoLocation,
)
from network_generation.model.python.hexagon import Hex, Layout
from network_generation.model.python.o_ran_object import (
    IORanObject,
    ORanObject,
)
from network_generation.model.python.o_ran_spiral_radius_profile import (
    SpiralRadiusProfile,
)
from network_generation.model.python.o_ran_termination_point import (
    ORanTerminationPoint,
)
from network_generation.model.python.point import Point
from network_generation.model.python.type_definitions import AddressType


# Define the "IORanObject" interface
class IORanNode(IORanObject):
    address: AddressType
    geoLocation: GeoLocation
    url: str
    position: Hex
    layout: Layout
    spiralRadiusProfile: SpiralRadiusProfile
    parent: Any
    network: Any


default_address: AddressType = {
    "street": "highstreet",
    "building": "none",
    "city": "heaven",
    "room": "frist",
    "zip": "12345",
    "state": "none",
    "country": Country.Germany,
}
default_value: IORanNode = cast(
    IORanNode,
    {
        **ORanObject.default(),
        **{
            "address": default_address,
            "geoLocation": GeoLocation(),
            "url": "non-url",
            "position": Hex(0, 0, 0),
            "layout": Layout(Hexagon.layout_flat, Point(1, 1), Point(0, 0)),
            "spiralRadiusProfile": SpiralRadiusProfile(),
            "parent": None,
            "network": None,
        },
    },
)


# Define an abstract O-RAN Node class
class ORanNode(ORanObject):

    # Get the current date and time in UTC
    __current_time = datetime.now(timezone.utc)
    # Format the time string as required
    __time_string = __current_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    # List of logical TerminationPoint labels
    _interfaces: list[str] = []

    @staticmethod
    def default() -> dict[str, Any]:
        return cast(dict[str, Any], default_value)

    def __init__(
        self,
        data: dict[str, Any] = cast(dict[str, Any], default_value),
        **kwargs: dict[str, Any],
    ) -> None:
        o_ran_node_data: IORanNode = self._to_o_ran_node_data(data)
        super().__init__(cast(dict[str, Any], data), **kwargs)
        self._address: AddressType = cast(
            AddressType, o_ran_node_data["address"]
        )
        self._geo_location: GeoLocation = o_ran_node_data["geoLocation"]
        self._url: str = str(o_ran_node_data["url"])
        self._position: Hex = cast(Hex, o_ran_node_data["position"])
        self._layout: Layout = cast(Layout, o_ran_node_data["layout"])
        self._spiral_radius_profile: SpiralRadiusProfile = cast(
            SpiralRadiusProfile, o_ran_node_data["spiralRadiusProfile"]
        )
        self._parent: Any = o_ran_node_data["parent"]
        self._network: Any = o_ran_node_data["network"]
        self._termination_points = (
            self._add_termination_points(self._interfaces))

    def _to_o_ran_node_data(self, data: dict[str, Any]) -> IORanNode:
        result: IORanNode = default_value
        for key, key_type in IORanNode.__annotations__.items():
            if key in data:
                result[key] = data[key]  # type: ignore
        return result

    @property
    def host(self) -> str:
        return self.parent.host

    @property
    def address(self) -> AddressType:
        return self._address

    @address.setter
    def address(self, value: AddressType) -> None:
        self._address = value

    @property
    def geo_location(self) -> GeoLocation:
        return self._geo_location

    @geo_location.setter
    def geo_location(self, value: GeoLocation) -> None:
        self._geo_location = value

    @property
    def url(self) -> str:
        return self._url

    @url.setter
    def url(self, value: str) -> None:
        self._url = value

    @property
    def position(self) -> Hex:
        return self._position

    @position.setter
    def position(self, value: Hex) -> None:
        self._position = value

    @property
    def layout(self) -> Layout:
        return self._layout

    @layout.setter
    def layout(self, value: Layout) -> None:
        self._layout = value

    @property
    def spiral_radius_profile(self) -> SpiralRadiusProfile:
        return self._spiral_radius_profile

    @spiral_radius_profile.setter
    def spiral_radius_profile(self, value: SpiralRadiusProfile) -> None:
        self._spiral_radius_profile = value

    @property
    def parent(
        self,
    ) -> Any:  # expected are ORanNodes and all inherits for ORanNode
        return self._parent

    @parent.setter
    def parent(self, value: Any) -> None:
        self._parent = value

    @property
    def network(
        self,
    ) -> Any:  # expected is ORanNetwork
        return self._network

    @network.setter
    def network(self, value: Any) -> None:
        self._network = value

    # @property
    # @abstractmethod
    def termination_points(self) -> list[ORanTerminationPoint]:
        return self._termination_points

    def _add_termination_points(
        self,
        logical_interfaces: list[str]
    ) -> list[ORanTerminationPoint]:
        result: list[ORanTerminationPoint] = []
        phy_tp: str = "-".join([self.name, "phy".upper()])
        result.append(ORanTerminationPoint({
            "name": phy_tp,
            "type": "o-ran-sc-network:phy",
            "operationalState": self.operationalState,
            "network": self.network,
        }))
        for interface in logical_interfaces:
            id: str = "-".join([self.name, interface.upper()])
            result.append(ORanTerminationPoint({
                     "name": id,
                     "type": ":".join(["o-ran-sc-network", interface]),
                     "operationalState": self.operationalState,
                     "supporter": {
                        "network-ref": self.network.id,
                        "node-ref": self.name,
                        "tp-ref": phy_tp,
                     },
                     "network": self.network
                }))
        return result

    @abstractmethod
    def to_topology_nodes(self) -> list[dict[str, Any]]:
        tps: list[dict[str, Any]] = []
        for tp in self.termination_points():
            new_tp = tp.to_topology()
            if any(
                existing_tp["tp-id"] == new_tp["tp-id"] for existing_tp in tps
            ):
                pass
            else:
                tps.append(new_tp)

        result: list[dict[str, Any]] = []
        result.append(
            {
                "node-id": self.name,
                "o-ran-sc-network:uuid": str(uuid.uuid5(uuid.NAMESPACE_DNS, "-".join([self.network.name, self.name]))),
                "o-ran-sc-network:type": self.type,
                "o-ran-sc-network:operational-state": self.operationalState,
                "ietf-network-topology:termination-point": tps,
            }
        )
        return result

    @abstractmethod
    def to_topology_links(self) -> list[dict[str, Any]]:
        result: list[dict[str, Any]] = []
        source_tp: str = "-".join([self.name, "phy".upper()])
        dest_tp: str = "-".join([self.parent.name, "phy".upper()])
        if self.parent and "Tower" not in source_tp and "Tower" not in dest_tp:
            link_id: str = "".join(
                ["phy", ":", self.name, "<->", self.parent.name]
            )
            link = {
                "link-id": link_id,
                "source": {"source-node": self.name, "source-tp": source_tp},
                "destination": {
                    "dest-node": self.parent.name,
                    "dest-tp": dest_tp,
                },
            }
            result.append(link)
        return result

    @abstractmethod
    def toKml(self) -> ET.Element:
        folder: ET.Element = ET.Element("Folder")
        open: ET.Element = ET.SubElement(folder, "open")
        open.text = "1"
        name: ET.Element = ET.SubElement(folder, "name")
        name.text = self.name

        placemark: ET.Element = ET.SubElement(folder, "Placemark")
        name: ET.Element = ET.SubElement(placemark, "name")
        name.text = self.name
        style: ET.Element = ET.SubElement(placemark, "styleUrl")
        style.text = f'#{self.__class__.__name__}'
        multi_geometry: ET.Element = ET.SubElement(placemark, "MultiGeometry")

        # my position as point
        point: ET.Element = ET.SubElement(multi_geometry, "Point")
        point_coordinates: ET.Element = ET.SubElement(point, "coordinates")

        point_gl = self.geo_location
        point_coordinates.text = ",".join([
                str("%.6f" % float(point_gl.longitude)),
                str("%.6f" % float(point_gl.latitude)),
                str("%.6f" % float(point_gl.aboveMeanSeaLevel)),
            ])

        # link to parent
        if (getattr(self.parent, 'geo_location', None) is not None):
            line: ET.Element = ET.SubElement(multi_geometry, "LineString")
            extrude: ET.Element = ET.SubElement(line, "extrude")
            extrude.text = "1"
            tessellate: ET.Element = ET.SubElement(line, "tessellate")
            tessellate.text = "1"
            coordinates: ET.Element = ET.SubElement(line, "coordinates")

            my_gl = self.geo_location
            parent_gl = self.parent.geo_location
            coordinates.text = " ".join([
                ",".join([
                    str("%.6f" % float(my_gl.longitude)),
                    str("%.6f" % float(my_gl.latitude)),
                    str("%.6f" % float(my_gl.aboveMeanSeaLevel)),
                ]),
                ",".join([
                    str("%.6f" % float(parent_gl.longitude)),
                    str("%.6f" % float(parent_gl.latitude)),
                    str("%.6f" % float(parent_gl.aboveMeanSeaLevel)),
                ]),
            ])
        return folder

    @abstractmethod
    def toSvg(self) -> ET.Element:
        pass

    @abstractmethod
    def to_directory(self, parent_dir: str) -> None:
        pass

    def get_coordinates(self) -> list[float]:
        lng: float = 0.0
        lat: float = 0.0

        gl = self._geo_location
        # TODO: Why a is gl sometimes a dict and not a GeoLoaction???
        if isinstance(gl, GeoLocation):
            lng = gl.longitude
            lat = gl.latitude
        elif isinstance(gl, dict):
            lng = gl["longitude"]
            lat = gl["latitude"]

        return [lng, lat]

    @abstractmethod
    def to_geojson_feature(self) -> list[dict[str, Any]]:
        result: list[dict[str, Any]] = []
        tps: list[dict[str, Any]] = []
        for tp in self.termination_points():
            new_tp = tp.to_topology()
            if any(existing_tp['tp-id'] == new_tp['tp-id'] for existing_tp in tps):
                pass
            else:
                tps.append(new_tp)

        result.append(
            {
                "type": "Feature",
                "properties": {
                    "type": "PropertiesNode",
                    "node-uuid": str(uuid.uuid5(uuid.NAMESPACE_DNS, "-".join([self.network.name, self.name]))),
                    "node-id": self.name,
                    "function": self.type
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": self.get_coordinates(),
                },
            }
        )
        return result

    @abstractmethod
    def to_tmf686_vertex(self) -> list[dict[str, Any]]:
        result: list[dict[str, Any]] = []
        result.append(
            {
                "id": self.id,
                "name": self.name,
                "description": f"Description of a vertex object of type {type(self)}",
                "href": f"https://{self.host}/tmf-api/topologyDiscovery/v4/graph/{self.network.id}/vertex/{self.id}",
                # optional "edge": [],
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
                    # "@schemaLocation": F'https://{self.host}/schema/tmf686-schema.json',
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
                    #     "@schemaLocation": F'https://{self.host}/schema/tmf686-schema.json',
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
                "@schemaLocation": f"https://{self.host}/schema/tmf686-schema.json",
                "@type": "Vertex",
            }
        )
        for tp in self.termination_points():
            result.append(tp.to_tmf686_vertex())
        return result

    @abstractmethod
    def to_tmf686_edge(self) -> list[dict[str, Any]]:
        result: list[dict[str, Any]] = []
        source_tp: str = "-".join([self.name, "phy".upper()])
        dest_tp: str = "-".join([self.parent.name, "phy".upper()])
        if self.parent and "Tower" not in source_tp and "Tower" not in dest_tp:
            link_id: str = "".join(["phy", ":", self.name, "<->", self.parent.name])
            link: dict[str, Any] = {
                "link-id": link_id,
                "source": {"source-node": self.name, "source-tp": source_tp},
                "destination": {
                    "dest-node": self.parent.name,
                    "dest-tp": dest_tp,
                },
            }
            link = {
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
                            f'https://{self.host}/tmf-api/topologyDiscovery/v4'
                            f'/graph/{self.network.id}/vertex/{source_tp}'
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
                            f'https://{self.host}/tmf-api/topologyDiscovery/v4'
                            f'/graph/{self.network.id}/vertex/{dest_tp}'
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
            result.append(link)
        return result

    @abstractmethod
    def to_tmf633_service_candidate_references(self) -> list[dict[str, Any]]:
        return [
            {
                "id": self.id,
                "href": f"https://{self.host}/tmf-api/serviceCatalogManagement/v4/serviceCandidate/{self.id}",
                "name": self.name,
                "version": self.network.version,
            }
        ]

    @abstractmethod
    def to_tmf633_service_candidates(self) -> list[dict[str, Any]]:
        return [
            {
                "id": self.id,
                "href": f"https://{self.host}/tmf-api/serviceCatalogManagement/v4/serviceCandidate/{self.id}",
                "name": self.name,
                "description": (
                    "The service candidate of 5G services including RAN, core "
                    "network and IoT services for the year "
                    f'{self.__current_time.strftime("%Y")}.'),
                "lastUpdate": self.__time_string,
                "lifecycleStatus": "Active",
                "version": self.network.version,
                "category": [
                    {
                        "id": self.network.id,
                        "href": (
                            f"https://{self.host}/tmf-api/serviceCatalogManagement/v4/serviceCategory/{self.network.id}"
                        ),
                        "name": self.network.name,
                        "version": self.network.version,
                    }
                ],
                "serviceSpecification": {
                    "id": self.id,
                    "href": f"https://{self.host}/tmf-api/serviceCatalogManagement/v4/serviceSpecification/{self.id}",
                    "name": self.name,
                    "version": self.network.version,
                },
                "validFor": self.network.valid_for,
            }
        ]

    def get_oran_network_id_property(self) -> str:
        if self.__class__.__name__ == "NrCellDu":
            return "properties.name"
        else:
            return "properties.node-id"

    @abstractmethod
    def to_tmf633_service_specifications(self) -> list[dict[str, Any]]:
        result: list[dict[str, Any]] = []
        result.append(
            {
                "id": self.id,
                "href": f"https://{self.host}/tmf-api/serviceCatalogManagement/v4/serviceSpecification/{self.id}",
                "name": self.name,
                "description": "INDIGO Service Specification PublicSafety",
                "isBundle": False,
                "version": self.network.version,
                "lastUpdate": self.__time_string,
                "lifecycleStatus": "Active",
                "relatedParty": self.network.related_party,
                "validFor": self.network.valid_for,
                "attachment": [],
                "entitySpecRelationship": [],
                "featureSpecification": [],
                "resourceSpecification": self.to_tmf634_resource_specification_references(),
                "serviceLevelSpecification": [],
                "serviceSpecRelationship": [],
                "specCharacteristic": [
                    {
                        "id": "resilienceLevel",
                        "name": "Resilience Level",
                        "description": "The resilience level of this service.",
                        "valueType": "integer",
                        "configurable": False,
                        "characteristicValueSpecification": [
                            {"value": 0, "isDefault": True}
                        ],
                    },
                    {
                        "id": "securityLevel",
                        "description": "The security level of this service.",
                        "valueType": "integer",
                        "configurable": False,
                        "characteristicValueSpecification": [
                            {"value": 1, "isDefault": True}
                        ],
                    },
                    {
                        "id": "sNssai",
                        "name": "Single Network Slice Selection Assistance Information",
                        "description": "The Single Network Slice Selection Assistance Information of this service.",
                        "configurable": True,
                        "valueType": "Integer32",
                        "isUnique": True,
                    },
                    {
                        "id": "maxBandwidthUE",
                        "name": "Maximum Bandwidth UE",
                        "description": "Maximum bandwidth in [MBps] per User Equipment (UE)",
                        "configurable": True,
                        "valueType": "Mbps",
                        "minCardinality": 5,
                        "maxCardinality": 1000,
                    },
                    {
                        "id": "coverageArea",
                        "name": "Coverage Area",
                        "description": "The geographical area covered by this entity.",
                        "configurable": False,
                        "extensible": False,
                        "isUnique": True,
                        "characteristicValueSpecification": [
                            {
                                "valueType": "href",
                                "value": (
                                    f'https://{self.host}/area/o-ran-network.'
                                    "geo.json/features?"
                                    f'{self.get_oran_network_id_property()}='
                                    f'{self.name}'),
                            }
                        ],
                    },
                    {
                        "id": "maxLatency",
                        "name": "Maximal Latency",
                        "description": (
                            "Maximum tolerable delay in milliseconds [ms]"),
                        "configurable": False,
                        "valueType": "time",
                        "characteristicValueSpecification": [
                            {"valueType": "integer", "value": 10}
                        ],
                    },
                    {
                        "name": "availability",
                        "description": "Guaranteed service uptime",
                        "configurable": False,
                        "valueType": "Propability",
                        "characteristicValueSpecification": [
                            {"valueType": "Propability", "value": "99.9%"}
                        ],
                    },
                    {
                        "id": "mttr",
                        "name": "Mean Time to Repair",
                        "description": "Maximal Mean Time To Repair a failure",
                        "configurable": False,
                        "valueType": "time",
                        "characteristicValueSpecification": [
                            {"valueType": "maximum time", "value": "4 hours"}
                        ],
                    },
                    {
                        "id": "mtbf",
                        "name": "Mean Time Between Failures",
                        "description": "Target for Mean Time Between Failures",
                        "configurable": False,
                        "valueType": "time",
                        "characteristicValueSpecification": [
                            {"valueType": "minimum time", "value": "1 year"}
                        ],
                    },
                ],
            }
        )
        return result

    @abstractmethod
    def to_tmf634_resource_candidate_references(self) -> list[dict[str, Any]]:
        return [
            {
                "id": self.id,
                "href": f"https://{self.host}/tmf-api/resourceCatalog/v5/resourceCandidate/{self.id}",
                "name": self.name,
                "version": self.network.version,
                "@type": "ResourceCandidateRef",
                "@referredType": "ResourceCandidate",
            }
        ]

    @abstractmethod
    def to_tmf634_resource_specification_references(self) -> list[dict[str, Any]]:
        return [
            {
                "id": self.id,
                "href": f"https://{self.host}/tmf-api/resourceCatalog/v5/resourceSpecification/{self.id}",
                "name": self.name,
                "version": self.network.version,
                "@type": "ResourceSpecificationRef",
                "@referredType": "ResourceSpecification",
            }
        ]

    @abstractmethod
    def to_tmf634_resource_candidates(self) -> list[dict[str, Any]]:
        return [
            {
                "id": self.id,
                "href": f"https://{self.host}/tmf-api/resourceCatalog/v5/resourceCandidate/{self.id}",
                "name": self.name,
                "description": f'The resource candidate of 5G RAN related resources for year {self.__current_time.strftime("%Y")}.',
                "lastUpdate": self.__time_string,
                "lifecycleStatus": "Active",
                "version": self.network.version,
                "category": [
                    {
                        "id": self.network.id,
                        "href": f"https://{self.host}/tmf-api/resourceCatalog/v5/resourceCategory/{self.network.id}",
                        "name": self.network.name,
                        "version": self.network.version,
                    }
                ],
                "resourceSpecification": {
                    "id": self.id,
                    "href": f"https://{self.host}/tmf-api/resourceCatalog/v5/resourceSpecification/{self.id}",
                    "name": self.name,
                    "version": self.network.version,
                    "@type": "ResourceSpecificationRef",
                    "@referredType": "ResourceSpecification",
                },
                "validFor": self.network.valid_for,
                "@type": "ResourceCandidate",
            }
        ]

    @abstractmethod
    def to_tmf634_resource_specifications(self) -> list[dict[str, Any]]:
        result: list[dict[str, Any]] = []
        result.append(
            {
                "id": self.id,
                "href": f"https://{self.host}/tmf-api/resourceCatalog/v5/resourceSpecification/{self.id}",
                "name": self.name,
                "description": f"INDIGO Resource Specification for type {type(self)}",
                "isBundle": False,
                "version": self.network.version,
                "lastUpdate": self.__time_string,
                "lifecycleStatus": "Active",
                "relatedParty": self.network.related_party,
                "validFor": self.network.valid_for,
                "category": "RAN resource",
                "attachment": [],
                "featureSpecification": [],
                "resourceSpecCharacteristic": [
                    {
                        "name": "nRCellName",
                        "description": "Cell identifier or name of the cell.",
                        "configurable": True,
                        "isUnique": True,
                        "valueType": "string",
                    },
                    {
                        "name": "nRCellId",
                        "description": "Uniquely identifies a cell within a PLMN. It is often constructed from gNodeB ID + Physical Cell ID.",
                        "valueType": "string",
                        "configurable": True,
                        "isUnique": True,
                    },
                    {
                        "name": "nRCellState",
                        "description": (
                            "Represents the active state of the cell. Takes "
                            "one of the following values: "
                            "IDLE ACTIVE INACTIVE UNKNOWN"),
                        "valueType": "string",
                        "configurable": False,
                        "isUnique": True,
                    },
                    {
                        "name": "TAI",
                        "description": (
                            "Tracking Area Identifier (TAI). This is a "
                            "globally unique tracking area identifier, "
                            "made up of the PLMN ID and the TAC."),
                        "valueType": "string",
                        "configurable": True,
                        "isUnique": True,
                    },
                    {
                        "name": "channelBandwidthUl",
                        "description": "Uplink channel bandwidth.",
                        "valueType": "float",
                        "configurable": True,
                        "isUnique": True,
                    },
                    {
                        "name": "channelBandwidthDl",
                        "description": "Downlink channel bandwidth.",
                        "valueType": "float",
                        "configurable": True,
                        "isUnique": True,
                    },
                    {
                        "name": "maximumOutputPower",
                        "description": (
                            "Maximum power in Watts for the sum of all downlink"
                            " channels that are allowed to be used "
                            "simultaneously in a cell."),
                        "valueType": "float",
                        "configurable": True,
                        "isUnique": True,
                    },
                    {
                        "name": "userCapacity",
                        "description": (
                            "Maximum number of pieces of user equipment (UEs) "
                            "that can connect to this nrCellDU simultaneously."
                        ),
                        "valueType": "Integer",
                        "configurable": True,
                        "isUnique": True,
                    },
                    {
                        "name": "physicalCellID",
                        "description": (
                            "Physical cell identifier. Takes a value in the "
                            "range 0 to 503. The physical cell id is used by "
                            "the cell to encode and decode the data that it "
                            "transmits. It is used in a similar way to the "
                            "UMTS scrambling code. To avoid interference, "
                            "neighboring cells should have different physical "
                            "cell identifiers. The physical cell id is derived "
                            "from the primary and secondary synchronization "
                            "signals (PSS and SSS). The PSS takes a value from "
                            "0 to 2, the SSS takes a value from 0 to 167, and "
                            "the physical cell id is determined based on the "
                            "following formula: PSS + 3*SSS. The result of "
                            "this calculation equates to a value of between "
                            "0 and 503."),
                        "valueType": "Integer",
                        "configurable": True,
                        "isUnique": True,
                    },
                    {
                        "name": "localCellId",
                        "description": "Local cell id unique within the nrCellDU.",
                        "valueType": "Integer",
                        "configurable": True,
                        "isUnique": True,
                    },
                    {
                        "name": "arfcnDl",
                        "description": (
                            "Absolute Radio Frequency Channel Number "
                            "(downlink). An integer value which identifies the "
                            "downlink carrier frequency of the cell."),
                        "valueType": "Integer",
                        "configurable": True,
                        "isUnique": True,
                    },
                    {
                        "name": "arfcnUl",
                        "description": (
                            "Absolute Radio Frequency Channel Number (uplink). "
                            "An integer value which identifies the uplink "
                            "carrier frequency of the cell."),
                        "valueType": "Integer",
                        "configurable": True,
                        "isUnique": True,
                    },
                    {
                        "name": "nRPCI",
                        "description": (
                            "Holds the Physical Cell Identity (PCI) of the "
                            "NR cell."),
                        "valueType": "String",
                        "configurable": True,
                        "isUnique": True,
                    },
                    {
                        "name": "ssbFreq",
                        "description": (
                            "Indicates cell defining SSB frequency domain "
                            "position. Frequency of the cell defining SSB "
                            "transmission. The frequency provided in this "
                            "attribute identifies the position of resource "
                            "element. The frequency shall be positioned on the "
                            "NR global frequency raster, and within "
                            "bSChannelBwDL. Allowed values: 0..3279165"),
                        "valueType": "Float",
                        "configurable": True,
                        "isUnique": True,
                    },
                    {
                        "name": "ssbPeriodicity",
                        "description": (
                            "Indicates cell defined SSB periodicity in number "
                            "of subframes(ms). The SSB periodicity in msec is "
                            "used for the rate matching purpose. "
                            "Allowed values: 5, 10, 20, 40, 80, 160"),
                        "valueType": "Integer",
                        "configurable": True,
                        "isUnique": True,
                    },
                    {
                        "name": "ssbSubCarrierSpacing",
                        "description": "This SSB is used for synchronization. Its units are in kHz. Allowed values: {15, 30, 120, 240}",
                        "valueType": "Integer",
                        "configurable": True,
                        "isUnique": True,
                    },
                    {
                        "name": "operationalState",
                        "description": (
                            "Operational state of the nrCellDU. Takes one of "
                            "the following values: Enabled Disabled Other "
                            "Unknown"),
                        "valueType": "String",
                        "configurable": False,
                        "isUnique": True,
                    },
                    {
                        "name": "administrativeState",
                        "description": (
                            "Administrative state of the nrCellDU. Takes one of"
                            " the following values: Unlocked Locked Shutting "
                            "Down Other Unknown"),
                        "valueType": "String",
                        "configurable": False,
                        "isUnique": True,
                    },
                ],
                "resourceSpecRelationship": [],  # TODO self.parent.to_tmf634_resource_specifications(),
                "@type": "ResourceSpecification",
            }
        )
        return result

    @abstractmethod
    def add_teiv_data_entities(
        self, entity_type: str, attributes: dict[str, Any] = {}
    ) -> dict[str, list[dict[str, Any]]]:
        sources = []
        for tp in self.termination_points():
            sources.append(tp.name)
        result: dict[str, list[dict[str, Any]]] = {}
        entity_id = self.name
        entity: dict[str, Any] = {"id": entity_id}
        if attributes:
            entity["attributes"] = attributes
        if sources:
            entity["sourceIds"] = sources
        result[entity_type] = [entity]
        return result

    @abstractmethod
    def add_teiv_data_relationships(
        self, id: str, aside: str, bside: str, rel_type: str
    ) -> dict[str, list[dict[str, Any]]]:
        result: dict[str, list[dict[str, Any]]] = {}
        relationship = {"id": id, "aSide": aside, "bSide": bside}
        result[rel_type] = [relationship]
        return result
