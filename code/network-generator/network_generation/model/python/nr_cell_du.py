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
from network_generation.model.python.point import Point
from network_generation.model.python.o_ran_termination_point import (
    ORanTerminationPoint,
)


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
        self.type = "o-ran-sc-network:cell"
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

    def to_topology_nodes(self) -> list[dict[str, Any]]:
        # a cell is not a node it is a Termination Point
        result: list[dict[str, Any]] = []  # super().to_topology_nodes()
        return result

    def to_topology_links(self) -> list[dict[str, Any]]:
        # as a cell is not a node, it does not have links
        result: list[dict[str, Any]] = []  # super().to_topology_links()
        return result

    # returns a list of geo-locations as cell polygon
    def get_cell_polygons(self) -> list[GeoLocation]:
        points: list[Point] = Hexagon.polygon_corners(self.layout, self.position)
        method = (
            self.parent.parent.parent.parent.parent.parent.geo_location.point_to_geo_location
        )
        geo_locations: list[GeoLocation] = list(map(method, points))
        index: int = 1 + int(self._azimuth / self._cell_angle)
        network_center: GeoLocation = (
            self.parent.parent.parent.parent.parent.parent.geo_location
        )

        p1: int = (2 * index + 1) % 6
        p2: int = (2 * index + 2) % 6
        intersect1: Point = Point(
            (points[p1].x + points[p2].x) / 2,
            (points[p1].y + points[p2].y) / 2,
        )
        intersect_gl1: GeoLocation = network_center.point_to_geo_location(intersect1)

        p3: int = (2 * index + 3) % 6
        p4: int = (2 * index + 4) % 6
        intersect2: Point = Point(
            (points[p3].x + points[p4].x) / 2,
            (points[p3].y + points[p4].y) / 2,
        )
        intersect_gl2: GeoLocation = network_center.point_to_geo_location(intersect2)

        tower = self.geo_location

        cell_polygon: list[GeoLocation] = []
        cell_polygon.append(tower)
        cell_polygon.append(intersect_gl1)
        cell_polygon.append(geo_locations[(2 * index + 2) % 6])
        cell_polygon.append(geo_locations[(2 * index + 3) % 6])
        cell_polygon.append(intersect_gl2)
        # close polygon
        cell_polygon.append(tower)

        if self.cell_scale_factor > 0:
            scaled_cell_polygon: list[GeoLocation] = []

            arc: float = self.azimuth * math.pi / 180
            meterToDegree: float = 2 * math.pi * GeoLocation().equatorialRadius / 360
            centerX: float = self.layout.size.x * 0.5 * math.sin(arc)
            centerY: float = self.layout.size.y * 0.5 * math.cos(arc)
            cell_center: GeoLocation = GeoLocation(
                {
                    "latitude": tower.latitude + centerY / meterToDegree,
                    "longitude": tower.longitude + centerX / meterToDegree,
                    "aboveMeanSeaLevel": tower.aboveMeanSeaLevel,
                }
            )
            point_index: int = 0
            scale: float = 1 + self.cell_scale_factor / 100
            for gl in cell_polygon:
                lng_new: float = (
                    1 * scale * (gl.longitude - cell_center.longitude)
                ) + cell_center.longitude
                lat_new: float = (
                    1 * scale * (gl.latitude - cell_center.latitude)
                ) + cell_center.latitude

                data: IGeoLocation = {
                    "latitude": lat_new,
                    "longitude": lng_new,
                    "aboveMeanSeaLevel": gl.aboveMeanSeaLevel,
                }

                scaled_cell_polygon.append(GeoLocation(data))
                point_index += 1
            cell_polygon = scaled_cell_polygon
        return cell_polygon

    def toKml(self) -> ET.Element:
        nr_cell_du = super().toKml()
        multi_geometry = nr_cell_du.find('Placemark/MultiGeometry')

        polygon: ET.Element = ET.SubElement(multi_geometry, "Polygon")
        outer_boundary: ET.Element = ET.SubElement(polygon, "outerBoundaryIs")
        linear_ring: ET.Element = ET.SubElement(outer_boundary, "LinearRing")
        coordinates: ET.Element = ET.SubElement(linear_ring, "coordinates")

        cell_polygon: list[GeoLocation] = self.get_cell_polygons()
        text: list[str] = []
        for gl in cell_polygon:
            strs: list[str] = [
                str("%.6f" % float(gl.longitude)),
                str("%.6f" % float(gl.latitude)),
                str("%.6f" % float(gl.aboveMeanSeaLevel)),
            ]
            text.append(",".join(strs))
        coordinates.text = " ".join(text)
        return nr_cell_du

    def toSvg(self) -> ET.Element:
        return ET.Element("to-be-implemented")

    def to_directory(self, parent_dir: str) -> None:
        pass

    def get_geojson_href(self) -> str:
        return f"https://{self.network.host}/area/o-ran-network.geo.json/features?properties.name={self.name}"

    def to_termination_point(self) -> ORanTerminationPoint:
        tp = ORanTerminationPoint({
            "name": self.name,
            "type": self.type,
            "operationalState": self.operationalState,
            "network": self.network
        })
        return tp

    def to_geojson_feature(self) -> list[dict[str, Any]]:
        cell_polygon: list[GeoLocation] = self.get_cell_polygons()
        coordinates: list = []
        for gl in cell_polygon:
            cord: list[float] = [gl.longitude, gl.latitude]
            coordinates.append(cord)
        return [
            {
                "type": "Feature",
                "properties": {
                    "type": "PropertiesOdu",
                    "name": self.name,
                    "uuid": self.id,
                    "function": self.type,
                    "newRadioCellGlobalIdentity": {
                        "publicLandMobileNetworkIdentifier": "123-45",
                        "newRadioCellIdentity": "0x0FFFFFFFFF",
                    }
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [coordinates],
                },
            }
        ]

    def to_tmf686_vertex(self) -> list[dict[str, Any]]:
        # a cell is not a node it is a Termination Point
        result: list[dict[str, Any]] = []  # super().to_topology_nodes()
        return result

    def to_tmf686_edge(self) -> list[dict[str, Any]]:
        # as a cell is not a node, it does not have links
        result: list[dict[str, Any]] = []  # super().to_topology_links()
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
            entity_type: str = "o-ran-smo-teiv-ran:NRCellDU",
            attributes: dict[str, Any] = {}
    ) -> dict[str, list[dict[str, Any]]]:
        return super().add_teiv_data_entities(entity_type, attributes)

    def add_teiv_data_relationships(
            self,
            id: str = "",
            aside: str = "",
            bside: str = "",
            rel_type: str = ""
    ) -> dict[str, list[dict[str, Any]]]:
        result: dict[str, list[dict[str, Any]]] = {}
        return result
