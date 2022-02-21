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
Module for an abstract class called "Top".
This calls should be inherited for common functions
"""
from lxml import etree


class Svg():
    """
    The abstract "SVG" class adds common functions
    """

    __center_x: int = 0
    __center_y: int = 0
    __width: int = 0
    __height: int = 0
    __label: str = "my label"
    __tapi_object = None

    FONTSIZE: int = 10  # see svg.style.css file

    """
    Constructor
    """

    def __init__(self, tapi_object, center_x: int, center_y: int) -> None:
        self.__center_x = center_x
        self.__center_y = center_y
        self.__tapi_object = tapi_object
        self.__label = tapi_object.name().upper()
        self.__width = 4 * self.FONTSIZE # default for 1 CEP == cep.width()
        self.__height = 2 * self.FONTSIZE

    # getter
    def center_x(self) -> int:
        """
        Getter for x coordinate of the SVG center position
        :return Center x coordinate in pixel
        """
        return self.__center_x

    def center_y(self) -> int:
        """
        Getter for y coordinate of the SVG center position
        :return Center y coordinate in pixel
        """
        return self.__center_y

    def width(self) -> int:
        """
        Getter for width of the SVG Element
        :return Width in pixel
        """
        return self.__width

    def height(self) -> int:
        """
        Getter for height of the SVG Element
        :return Height in pixel
        """
        return self.__height

    def label(self) -> str:
        """
        Getter for the short label as displayed of the SVG Element
        :return Label of the TAPI object
        """
        return self.__label

    def tapi_object(self) -> int:
        """
        Getter for the given TAPI object
        :return Python TAPI object
        """
        return self.__tapi_object

    def type_name(self) -> int:
        """
        Getter for the given TAPI object type name
        :return TAPI object type name
        """
        return type(self.tapi_object()).__name__

    def svg_group(self) -> etree.Element:
        """
        Mothod generating the root SVG Element for the TAPI object
        :return SVG Element as root for the TAPI object
        """
        group: etree.Element = etree.Element("g")
        group.attrib["class"] = " ".join(["node", self.type_name()])
        title = etree.Element("title")
        title.text = "\n".join(
            [
                self.type_name(),
                "id: " + self.tapi_object().identifier(),
                "name: " + self.tapi_object().name()
            ]
        )
        group.append(title)
        return group

    def svg_main(self) -> etree.Element:
        """
        Mothod generating the main SVG Element shaping the TAPI object
        :return SVG Element as main representations for the TAPI object
        """
        main = etree.Element("ellipse")
        main.attrib['cx'] = str(self.center_x())
        main.attrib['cy'] = str(self.center_y())
        main.attrib['rx'] = str(int(self.width()/2))
        main.attrib['ry'] = str(int(self.height()/2))
        main.attrib['class'] = " ".join([self.type_name()])
        return main

    def svg_label(self) -> etree.Element:
        """
        Mothod generating the SVG Element of the label of the TAPI object
        :return SVG Element for the label of the TAPI object
        """
        label = etree.Element('text')
        label.attrib['x'] = str(self.center_x())
        # +4px for font-size 14px (think of chars like 'gjy')
        label.attrib['y'] = str(self.center_y() + 4)
        label.text = self.label()
        return label

    def svg_center(self) -> etree.Element:
        """
        Mothod generating the SVG Element of the label of the TAPI object
        :return SVG Element for the label of the TAPI object
        """
        dot = etree.Element('circle')
        dot.attrib['cx'] = str(self.center_x())
        dot.attrib['cy'] = str(self.center_y())
        dot.attrib['r'] = "2"
        dot.attrib['class'] = "dot"
        return dot

    def svg_element(self) -> etree.Element:
        """
        Method generating a SVG Element representing the TAPI Object
        :return A SVG group element including the main shape and a label
        """
        group: etree.Element = self.svg_group()
        group.attrib['id'] = self.tapi_object().identifier()
        group.append(self.svg_main())
        group.append(self.svg_label())
        # group.append(self.svg_center())
        return group
