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
A Class representing a 3GPP new radio cell du (NrCellDu)
"""
import xml.etree.ElementTree as ET
from typing import overload

import network_generation.model.python.hexagon as Hexagon
from network_generation.model.python.geo_location import GeoLocation
from network_generation.model.python.o_ran_node import ORanNode
from network_generation.model.python.o_ran_object import IORanObject
from network_generation.model.python.o_ran_termination_point import (
    ORanTerminationPoint,
)
from network_generation.model.python.point import Point


# Define the "INrCellDu" interface
class INrCellDu(IORanObject):
    def __init__(self, cell_angel: int, azimuth: int, **kwargs):
        super().__init__(**kwargs)
        self._cell_angle = cell_angel
        self._azimuth = azimuth


# Define an abstract O-RAN Node class
class NrCellDu(ORanNode, INrCellDu):
    def __init__(self, cell_data: INrCellDu = None, **kwargs):
        super().__init__(cell_data, **kwargs)
        self._cell_angle = (
            cell_data["cellAngle"]
            if cell_data and "cellAngle" in cell_data
            else 120
        )
        self._azimuth = (
            cell_data["azimuth"] if cell_data and "azimuth" in cell_data else 0
        )

    @property
    def termination_points(self) -> list[ORanTerminationPoint]:
        result: list[ORanTerminationPoint] = super().termination_points
        result.append(
            ORanTerminationPoint({"id": self.name, "name": self.name})
        )
        return result

    def to_topology_nodes(self) -> list[dict[str, dict]]:
        # a cell is not a node it is a Termination Point
        result: list[dict[str, dict]] = []  # super().to_topology_nodes()
        return result

    def to_topology_links(self) -> list[dict[str, dict]]:
        # as a cell is not a node, it does not have links
        result: list[dict[str, dict]] = []  # super().to_topology_links()
        return result

    def toKml(self) -> ET.Element:
        placemark: ET.Element = ET.Element("Placemark")
        name: ET.Element = ET.SubElement(placemark, "name")
        name.text = self.name
        style: ET.Element = ET.SubElement(placemark, "styleUrl")
        style.text = "#" + self.__class__.__name__
        multi_geometry: ET.Element = ET.SubElement(placemark, "MultiGeometry")
        polygon: ET.Element = ET.SubElement(multi_geometry, "Polygon")
        outer_boundary: ET.Element = ET.SubElement(polygon, "outerBoundaryIs")
        linear_ring: ET.Element = ET.SubElement(outer_boundary, "LinearRing")
        coordinates: ET.Element = ET.SubElement(linear_ring, "coordinates")

        points: list[Point] = Hexagon.polygon_corners(
            self.layout, self.position
        )
        method = GeoLocation(
            self.parent.parent.parent.parent.parent.parent.geoLocation
        ).point_to_geo_location
        geo_locations: list[GeoLocation] = list(map(method, points))
        text: list[str] = []

        index: int = 1 + int(self._azimuth / self._cell_angle)
        network_center: GeoLocation = GeoLocation(
            self.parent.parent.parent.parent.parent.parent.geoLocation
        )

        intersect1: Point = Point(
            (points[(2 * index + 1) % 6].x + points[(2 * index + 2) % 6].x)
            / 2,
            (points[(2 * index + 1) % 6].y + points[(2 * index + 2) % 6].y)
            / 2,
        )
        intersect_geo_location1: GeoLocation = (
            network_center.point_to_geo_location(intersect1)
        )

        intersect2: Point = Point(
            (points[(2 * index + 3) % 6].x + points[(2 * index + 4) % 6].x)
            / 2,
            (points[(2 * index + 3) % 6].y + points[(2 * index + 4) % 6].y)
            / 2,
        )
        intersect_geo_location2: GeoLocation = (
            network_center.point_to_geo_location(intersect2)
        )

        tower: GeoLocation = GeoLocation(self.geoLocation)

        cell_polygon: list[GeoLocation] = []
        cell_polygon.append(tower)
        cell_polygon.append(intersect_geo_location1)
        cell_polygon.append(geo_locations[(2 * index + 2) % 6])
        cell_polygon.append(geo_locations[(2 * index + 3) % 6])
        cell_polygon.append(intersect_geo_location2)
        # close polygon
        cell_polygon.append(tower)

        for geo_location in cell_polygon:
            text.append(
                f"{'%.6f' % geo_location.longitude},{'%.6f' % geo_location.latitude},{'%.6f' % geo_location.aboveMeanSeaLevel}"
            )
        coordinates.text = " ".join(text)

        return placemark

    def toSvg(self) -> None:
        return None
