# Copyright 2023 highstreet technologies USA CORP.
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
A Class representing a 3GPP new radio cell du (NrCellDu)
"""
import math
import xml.etree.ElementTree as ET
from typing import Any, cast

import network_generation.model.python.hexagon as Hexagon
from network_generation.model.python.geo_location import (
    GeoLocation,
    IGeoLocation,
)
from network_generation.model.python.o_ran_node import IORanNode, ORanNode
from network_generation.model.python.o_ran_termination_point import (
    ORanTerminationPoint,
)
from network_generation.model.python.point import Point


# Define the "INrCellDu" interface
class INrCellDu(IORanNode):
    cellAngle: int
    cellScaleFactorForHandoverArea: int
    maxReach: int
    azimuth: int


default_value: INrCellDu = cast(
    INrCellDu,
    {
        **ORanNode.default(),
        **{
            "cellAngle": 120,
            "cellScaleFactorForHandoverArea": 0,
            "maxReach": 100,
            "azimuth": 120,
        },
    },
)


# Define an abstract O-RAN Node class
class NrCellDu(ORanNode):
    def __init__(
        self,
        data: dict[str, Any] = cast(dict[str, Any], default_value),
        **kwargs: dict[str, Any]
    ) -> None:
        cell_data: INrCellDu = self._to_cell_data(data)
        super().__init__(cast(dict[str, Any], cell_data), **kwargs)
        self._cell_angle: int = int(str(cell_data["cellAngle"]))
        self._cell_scale_factor: int = int(
            str(cell_data["cellScaleFactorForHandoverArea"])
        )
        self._maxReach: int = int(str(cell_data["maxReach"]))
        self._azimuth: int = int(str(cell_data["azimuth"]))

    def _to_cell_data(self, data: dict[str, Any]) -> INrCellDu:
        result: INrCellDu = default_value
        for key, key_type in INrCellDu.__annotations__.items():
            if key in data:
                result[key] = data[key]  # type: ignore
        return result

    @property
    def cell_angle(self) -> int:
        return self._cell_angle

    @cell_angle.setter
    def cell_angle(self, value: int) -> None:
        self._cell_angle = value

    @property
    def cell_scale_factor(self) -> int:
        return self._cell_scale_factor

    @cell_scale_factor.setter
    def cell_scale_factor(self, value: int) -> None:
        self._cell_scale_factor = value

    @property
    def maxReach(self) -> int:
        return self._maxReach

    @maxReach.setter
    def maxReach(self, value: int) -> None:
        self._maxReach = value

    @property
    def azimuth(self) -> int:
        return self._azimuth

    @azimuth.setter
    def azimuth(self, value: int) -> None:
        self._azimuth = value

    def termination_points(self) -> list[ORanTerminationPoint]:
        result: list[ORanTerminationPoint] = super().termination_points()
        result.append(ORanTerminationPoint({"id": self.name, "name": self.name}))
        return result

    def to_topology_nodes(self) -> list[dict[str, Any]]:
        # a cell is not a node it is a Termination Point
        result: list[dict[str, Any]] = []  # super().to_topology_nodes()
        return result

    def to_topology_links(self) -> list[dict[str, Any]]:
        # as a cell is not a node, it does not have links
        result: list[dict[str, Any]] = []  # super().to_topology_links()
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

        points: list[Point] = Hexagon.polygon_corners(self.layout, self.position)
        method = (
            self.parent.parent.parent.parent.parent.parent.geo_location.point_to_geo_location
        )
        geo_locations: list[GeoLocation] = list(map(method, points))
        text: list[str] = []

        index: int = 1 + int(self._azimuth / self._cell_angle)
        network_center: GeoLocation = (
            self.parent.parent.parent.parent.parent.parent.geo_location
        )

        intersect1: Point = Point(
            (points[(2 * index + 1) % 6].x + points[(2 * index + 2) % 6].x) / 2,
            (points[(2 * index + 1) % 6].y + points[(2 * index + 2) % 6].y) / 2,
        )
        intersect_geo_location1: GeoLocation = network_center.point_to_geo_location(
            intersect1
        )

        intersect2: Point = Point(
            (points[(2 * index + 3) % 6].x + points[(2 * index + 4) % 6].x) / 2,
            (points[(2 * index + 3) % 6].y + points[(2 * index + 4) % 6].y) / 2,
        )
        intersect_geo_location2: GeoLocation = network_center.point_to_geo_location(
            intersect2
        )

        tower: GeoLocation = GeoLocation(cast(IGeoLocation, self.geo_location))
        # TODO: Why a cast is required

        cell_polygon: list[GeoLocation] = []
        cell_polygon.append(tower)
        cell_polygon.append(intersect_geo_location1)
        cell_polygon.append(geo_locations[(2 * index + 2) % 6])
        cell_polygon.append(geo_locations[(2 * index + 3) % 6])
        cell_polygon.append(intersect_geo_location2)
        # close polygon
        cell_polygon.append(tower)

        for gl in cell_polygon:
            strs: list[str] = [
                str("%.6f" % float(gl.longitude)),
                str("%.6f" % float(gl.latitude)),
                str("%.6f" % float(gl.aboveMeanSeaLevel)),
            ]
            text.append(",".join(strs))
        coordinates.text = " ".join(text)

        if self.cell_scale_factor > 0:
            scaled_polygon: ET.Element = ET.SubElement(multi_geometry, "Polygon")
            scaled_outer_boundary: ET.Element = ET.SubElement(scaled_polygon, "outerBoundaryIs")
            scaled_linear_ring: ET.Element = ET.SubElement(scaled_outer_boundary, "LinearRing")
            scaled_coordinates: ET.Element = ET.SubElement(scaled_linear_ring, "coordinates")

            arc: float = self.azimuth * math.pi / 180
            meterToDegree: float = 2 * math.pi * GeoLocation().equatorialRadius / 360
            translateX: float = (
                self.layout.size.x
                * (self.cell_scale_factor / 100)
                * math.sin(arc)
            )
            translateY: float = (
                self.layout.size.y
                * (self.cell_scale_factor / 100)
                * math.cos(arc)
            )
            centerX: float = self.layout.size.x * 0.5 * math.sin(arc)
            centerY: float = self.layout.size.y * 0.5 * math.cos(arc)
            cell_center : GeoLocation = GeoLocation(
                {
                    "latitude": tower.latitude + centerY / meterToDegree,
                    "longitude": tower.longitude + centerX / meterToDegree,
                    "aboveMeanSeaLevel": tower.aboveMeanSeaLevel,
                }
            )
            point_index: int = 0
            text = []
            for gl in cell_polygon:
                scale: float = 1 + self.cell_scale_factor / 100
                lng_new: float = ( 1 * scale * (gl.longitude - cell_center.longitude) ) + cell_center.longitude
                lat_new: float = ( 1 * scale * ( gl.latitude - cell_center.latitude ) ) + cell_center.latitude
                scaled_strs: list[str] = [
                    str("%.6f" % float(lng_new)),
                    str("%.6f" % float(lat_new)),
                    str("%.6f" % float(gl.aboveMeanSeaLevel)),
                ]
                text.append(",".join(scaled_strs))
                point_index += 1
            scaled_coordinates.text = " ".join(text)
        return placemark

    def toSvg(self) -> ET.Element:
        return ET.Element("to-be-implemented")
