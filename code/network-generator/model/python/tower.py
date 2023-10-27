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
A Class representing a Tower to mount O-RAN RUs
It can be interpreted as 'resource pool' for physical network
functions.
"""
from model.python.o_ran_object import IORanObject
from model.python.o_ran_ru import IORanRu, ORanRu
import model.python.hexagon as Hexagon
from model.python.point import Point
from model.python.geo_location import GeoLocation
from model.python.o_ran_node import ORanNode
import xml.etree.ElementTree as ET

# Define the "IORanDu" interface
class ITower(IORanObject):
    def __init__(self, o_ran_ru_count: int, **kwargs):
        super().__init__(**kwargs)
        self._o_ran_ru_count = o_ran_ru_count

# Implement a concrete O-RAN Node class
class Tower(ORanNode):

    def __init__(self, tower_data: ITower = None, **kwargs):
        super().__init__(tower_data, **kwargs)
        self._o_ran_ru_count = tower_data["oRanRuCount"] if tower_data and "oRanRuCount" in tower_data else 3
        self._o_ran_rus: list[ORanRu] = self._create_o_ran_rus()

    def _create_o_ran_rus(self) -> list [ORanRu]:
        result : list [ORanRu] = []
        for index in range(self._o_ran_ru_count):
            s: str = "00" + str(index)
            name: str = "-".join(
                [self.name.replace("Tower", "RU"), s[len(s) - 2 : len(s)]]
            )
            cell_count: int = self.parent.parent.parent.parent.parent.configuration()['pattern']["o-ran-ru"]["nr-cell-du-count"]
            result.append(
                ORanRu(
                    {
                        "name": name,
                        "geoLocation": self.geoLocation,
                        "position": self.position,
                        "layout": self.layout,
                        "spiralRadiusProfile": self.spiralRadiusProfile,
                        "parent": self,
                        "cellCount": cell_count
                    }
                )
            )
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
        points.append(points[0])
        method = GeoLocation(
            self.parent.parent.parent.parent.geoLocation
        ).point_to_geo_location
        geo_locations: list[GeoLocation] = list(map(method, points))
        text: list[str] = []
        for geo_location in geo_locations:
            text.append(
                f"{geo_location.longitude},{geo_location.latitude},{geo_location.aboveMeanSeaLevel}"
            )
        coordinates.text = " ".join(text)

        # cells
        cell_angle = self.parent.parent.parent.parent.parent.configuration()["pattern"]["nr-cell-du"]["cell-angle"]
        for index in range(int(360 / cell_angle)):
            line: ET.Element = ET.SubElement(multi_geometry, "LineString")
            tessellate: ET.Element = ET.SubElement(line, "tessellate")
            tessellate.text = "1"
            coordinates: ET.Element = ET.SubElement(line, "coordinates")

            intersect: Point = Point(
                (points[2 * index+2].x + points[2 * index + 1].x) / 2,
                (points[2 * index+2].y + points[2 * index + 1].y) / 2,
            )
            intersect_geo_location: GeoLocation = GeoLocation(
                self.parent.parent.parent.parent.geoLocation
            ).point_to_geo_location(intersect)
            text: list[str] = []
            text.append(
                f"{intersect_geo_location.longitude},{intersect_geo_location.latitude},{intersect_geo_location.aboveMeanSeaLevel}"
            )
            text.append(
                f"{self.geoLocation['longitude']},{self.geoLocation['latitude']},{self.geoLocation['aboveMeanSeaLevel']}"
            )
            coordinates.text = " ".join(text)

        return placemark

    def toSvg(self) -> None:
        return None
