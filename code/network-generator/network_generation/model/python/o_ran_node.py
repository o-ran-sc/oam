# Copyright 2023 highstreet technologies GmbH
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

#!/usr/bin/python

"""
An abstract Class for O-RAN Node
"""
import json
import xml.etree.ElementTree as ET
from abc import abstractmethod, abstractproperty
from typing import Any

import network_generation.model.python.hexagon as Hexagon
from network_generation.model.python.geo_location import GeoLocation
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
    def __init__(
        self,
        address: AddressType = None,
        geoLocation: GeoLocation = None,
        url: str = None,
        position: Hex = None,
        layout: Layout = None,
        spiralRadiusProfile: SpiralRadiusProfile = None,
        parent=None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.address = address
        self.geoLocation = geoLocation
        self.url = url
        self.position = position
        self.layout = layout
        self.spiralRadiusProfile = (spiralRadiusProfile,)
        self.parent = parent


# Define an abstract O-RAN Node class
class ORanNode(ORanObject, IORanNode):
    def __init__(self, of: IORanNode = None, **kwargs):
        super().__init__(of, **kwargs)
        self.address = of["address"] if of and "address" in of else None
        self.geoLocation = (
            of["geoLocation"] if of and "geoLocation" in of else GeoLocation()
        )
        self.url = of["url"] if of and "url" in of else self.id
        self.position = (
            of["position"] if of and "position" in of else Hex(0, 0, 0)
        )
        self.layout = (
            of["layout"]
            if of and "layout" in of
            else Layout(Hexagon.layout_flat, Point(1, 1), Point(0, 0))
        )
        self.spiralRadiusProfile = (
            of["spiralRadiusProfile"]
            if of and "spiralRadiusProfile" in of
            else SpiralRadiusProfile()
        )
        self.parent = of["parent"] if of and "parent" in of else None
        self._termination_points: list[ORanTerminationPoint] = []

    @property
    def address(self) -> str:
        return self._address

    @address.setter
    def address(self, value: str):
        self._address = value

    @property
    def geoLocation(self) -> GeoLocation:
        return self._geographicalLocation

    @geoLocation.setter
    def geoLocation(self, value: GeoLocation):
        self._geographicalLocation = value

    @property
    def url(self) -> str:
        return self._url

    @url.setter
    def url(self, value: str):
        self._url = value

    @property
    def position(self) -> Hex:
        return self._position

    @position.setter
    def position(self, value: Hex):
        self._position = value

    @property
    def layout(self) -> Layout:
        return self._layout

    @layout.setter
    def layout(self, value: Layout):
        self._layout = value

    @property
    def spiralRadiusProfile(self) -> SpiralRadiusProfile:
        return self._spiralRadiusProfile

    @spiralRadiusProfile.setter
    def spiralRadiusProfile(self, value: SpiralRadiusProfile):
        self._spiralRadiusProfile = value

    @property
    def parent(
        self,
    ) -> Any:  # expected are ORanNodes and all inherits for ORanNode
        return self._parent

    @parent.setter
    def parent(self, value: Any):
        self._parent = value

    @abstractproperty
    def termination_points(self) -> list[ORanTerminationPoint]:
        return self._termination_points

    def json(self) -> dict[str, dict]:
        result: dict = super().json()
        result["address"] = self.address
        result["geoLocation"] = self.geoLocation
        result["url"] = self.url
        result["layout"] = self.layout
        result["spiralRadiusProfile"] = self.spiralRadiusProfile
        result["parent"] = self.parent
        return result

    @abstractmethod
    def to_topology_nodes(self) -> list[dict[str, dict]]:
        tps: list[dict[str, dict]] = []
        for tp in self.termination_points:
            if (
                str(type(tp))
                == "<class 'model.python.o_ran_termination_point.ORanTerminationPoint'>"
            ):
                tps.append(tp.to_topology())

        result: list[dict[str, dict]] = []
        result.append(
            {
                "node-id": self.name,
                "ietf-network-topology:termination-point": tps,
            }
        )
        return result

    @abstractmethod
    def to_topology_links(self) -> list[dict[str, dict]]:
        result: list[dict[str, dict]] = []
        source_tp: str = "-".join([self.name, "phy".upper()])
        dest_tp: str = "-".join([self.parent.name, "phy".upper()])
        if self.parent and not "Tower" in source_tp and not "Tower" in dest_tp:
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
    def toKml(self) -> ET.Element | None:
        pass

    @abstractmethod
    def toSvg(self) -> ET.Element | None:
        pass
