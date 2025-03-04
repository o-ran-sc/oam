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
            "network": self.network
        }))
        for interface in logical_interfaces:
            id: str = "-".join([self.name, interface.upper()])
            result.append(ORanTerminationPoint({
                     "name": id,
                     "type": ":".join(["o-ran-sc-network", interface]),
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
                "o-ran-sc-network:uuid": str(
                    uuid.uuid5(
                        uuid.NAMESPACE_DNS,
                        "-".join([self.network.name, self.name]),
                    )
                ),
                "o-ran-sc-network:type": self.type,
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
