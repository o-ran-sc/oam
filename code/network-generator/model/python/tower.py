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
A Class representing a Tower to mount O-RAN RUx
"""
from typing import Any, Dict

import model.python.hexagon as Hexagon
from model.python.hexagon import Hex, Layout, Point
from model.python.geo_location import GeoLocation

from model.python.o_ran_object import IORanObject
from model.python.o_ran_node import ORanNode
import xml.etree.ElementTree as ET


# Define the "ITower" interface
class ITower(IORanObject):
    def __init__(self, layout: Layout, hex: Hex = None, **kwargs):
        super().__init__(**kwargs)


# Define an abstract O-RAN Node class
class Tower(ORanNode, ITower):
    def __init__(self, tower_data: ITower = None, **kwargs):
        super().__init__(tower_data, **kwargs)

    def toKml(self):
        placemark: ET.Element = ET.Element("Placemark")
        name: ET.Element = ET.SubElement(placemark, "name")
        name.text = self.name
        style: ET.Element = ET.SubElement(placemark, "styleUrl")
        style.text = "#" + self.__class__.__name__
        polygon: ET.Element = ET.SubElement(placemark, "Polygon")
        outer_boundary: ET.Element = ET.SubElement(polygon, "outerBoundaryIs")
        linear_ring: ET.Element = ET.SubElement(outer_boundary, "LinearRing")
        coordinates: ET.Element = ET.SubElement(linear_ring, "coordinates")
        points: list[Point] = Hexagon.polygon_corners(self.layout, self.position)
        points.append(points[0])

        method = GeoLocation(self.geoLocation).point_to_geo_location
        geo_locations: list[GeoLocation] = map(method, points)
        text:list[str] = []
        for geo_location in list(geo_locations):
            text.append(f"{geo_location.longitude},{geo_location.latitude},{geo_location.aboveMeanSeaLevel}")
        coordinates.text = " ".join(text)
        return placemark

    def toSvg(self):
        return None
