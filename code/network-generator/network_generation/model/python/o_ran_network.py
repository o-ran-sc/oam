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

# !/usr/bin/python
"""
Module for a class representing a O-RAN Network
"""
import xml.etree.ElementTree as ET
from typing import Any, cast

import network_generation.model.python.hexagon as Hexagon
from network_generation.model.python.geo_location import (
    GeoLocation,
    IGeoLocation,
)
from network_generation.model.python.hexagon import Layout
from network_generation.model.python.o_ran_object import (
    IORanObject,
    ORanObject,
)
from network_generation.model.python.o_ran_smo import ORanSmo
from network_generation.model.python.o_ran_spiral_radius_profile import (
    SpiralRadiusProfile,
)
from network_generation.model.python.point import Point

# Define the "IORanNetwork" interface
IORanNetwork = IORanObject


class ORanNetwork(ORanObject):
    """
    Class representing an O-RAN Network object.
    """

    __my_default_value: IORanNetwork = cast(IORanNetwork, ORanObject.default())

    # constructor
    def __init__(
        self,
        configuration: dict[str, dict],
        data: dict[str, Any] = cast(dict[str, Any], __my_default_value),
        **kwargs: dict[str, Any]
    ) -> None:
        o_ran_network_data: IORanNetwork = self._to_o_ran_network_data(data)
        super().__init__(cast(dict[str, Any], o_ran_network_data), **kwargs)
        self.__configuration = configuration

        self.name = str(configuration["name"])
        self._center: IGeoLocation = cast(
            IGeoLocation, configuration["center"]
        )

        size: int = int(
            int(configuration["pattern"]["nrCellDu"]["maxReach"])
            / (
                1
                + int(
                    configuration["pattern"]["nrCellDu"][
                        "cellScaleFactorForHandoverArea"
                    ]
                )
                / 100
            )
        )
        layout = Layout(
            Hexagon.layout_flat, Point(size, size), Point(0, 0)
        )  # 1 pixel = 1 meter
        self._spiral_radius_profile: SpiralRadiusProfile = SpiralRadiusProfile(
            {
                "oRanSmoSpiralRadiusOfNearRtRics": configuration["pattern"][
                    "smo"
                ]["nearRtRicSpiralRadius"],
                "oRanNearRtRicSpiralRadiusOfOCus": configuration["pattern"][
                    "nearRtRic"
                ]["oRanCuSpiralRadius"],
                "oRanCuSpiralRadiusOfODus": configuration["pattern"][
                    "oRanCu"
                ]["oRanDuSpiralRadius"],
                "oRanDuSpiralRadiusOfTowers": configuration["pattern"][
                    "oRanDu"
                ]["towerSpiralRadius"],
            }
        )
        self._o_ran_smo = ORanSmo(
            {
                "name": "O-RAN-SMO",
                "geoLocation": self.center,
                "layout": layout,
                "parent": self,
            }
        )

    def _to_o_ran_network_data(self, data: dict[str, Any]) -> IORanNetwork:
        result: IORanNetwork = self.__my_default_value
        for key, key_type in IORanNetwork.__annotations__.items():
            if key in data:
                result[key] = data[key]  # type: ignore
        return result

    @property
    def center(self) -> GeoLocation:
        """
        Getter for a json object representing the O-RAN Network.
        :return O-RAN Network as json object.
        """
        return GeoLocation(self._center)

    @property
    def spiral_radius_profile(self) -> SpiralRadiusProfile:
        """
        Getter for a json object representing the SpiralRadiusProfile.
        :return SpiralRadiusProfile.
        """
        return self._spiral_radius_profile

    @property
    def configuration(self) -> dict[str, Any]:
        """
        Getter for a json object representing the O-RAN Network.
        :return O-RAN Network as json object.
        """
        return self.__configuration

    def to_topology(self) -> dict[str, Any]:
        nodes: list[dict[str, Any]] = self._o_ran_smo.to_topology_nodes()
        links: list[dict[str, Any]] = self._o_ran_smo.to_topology_links()
        return {
            "ietf-network:networks": {
                "network": [
                    {
                        "network-id": self.id,
                        "node": nodes,
                        "ietf-network-topology:link": links,
                    }
                ],
            }
        }

    def toKml(self) -> ET.Element:
        root: ET.Element = ET.Element(
            "kml", xmlns="http://www.opengis.net/kml/2.2"
        )
        document = ET.SubElement(root, "Document")
        open: ET.Element = ET.SubElement(document, "open")
        open.text = "1"
        name: ET.Element = ET.SubElement(document, "name")
        name.text = self.name

        document.append(self._o_ran_smo.toKml())

        return root

    def toSvg(self) -> ET.Element:
        """
        Getter for a xml/svg Element object representing the Network.
        :return Network as SVG object.
        """
        root: ET.Element = ET.Element(
            "svg",
            # width=str(self.__svg_width()),
            # height=str(self.__svg_height()),
            # viewBox=" ".join([
            #     str(-3*self.FONTSIZE),
            #     str(-3*self.FONTSIZE),
            #     str(self.__svg_width()),
            #     str(self.__svg_height())]
            # ),
            xmlns="http://www.w3.org/2000/svg",
        )
        desc = ET.Element("desc")
        desc.text = "\n context: " + self.id + "\n name: " + self.name
        root.append(desc)

        title = ET.Element("title")
        title.text = str(self.configuration["name"])
        root.append(title)

        # root.append(self.__context.svg(x, y))
        return root

    def json(self) -> dict[str, Any]:
        return super().json()
