# Copyright 2022 highstreet technologies GmbH
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
Module containing a class representing an SVG Element as Connection Node Edge Point
"""
from lxml import etree
from model.python.svg.connection_edge_point import ConnectionEdgePoint
from model.python.svg.svg import Svg


class NodeEdgePoint(Svg):
    """
    Class representing an SVG Element object as Connection Node Edge Point
    """
    def width(self) -> int:
        """
        Getter for width of the SVG Element
        :return Width in pixel
        """
        self.__width = ConnectionEdgePoint.width(self) * len(self.tapi_object().connection_edge_points())
        return self.__width

    # overwrite
    def svg_main(self) -> etree.Element:
        """
        Mothod generating the main SVG Element shaping the TAPI object
        :return SVG Element as main representations for the TAPI object
        """
        main = super().svg_main()
        main = etree.Element("rect")
        main.attrib["x"] = str(int(self.center_x() - self.width()/2))
        main.attrib["y"] = str(int(self.center_y() - self.height()/2))
        main.attrib["width"] = str(self.width())
        main.attrib["height"] = str(self.height())
        main.attrib["rx"] = str(int(self.FONTSIZE / 2))
        main.attrib['class'] = " ".join(
            [self.type_name(), self.tapi_object().name().lower()])
        return main
