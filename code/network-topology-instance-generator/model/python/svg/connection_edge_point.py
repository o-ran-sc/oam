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
from typing import Dict
from lxml import etree
from model.python.svg.svg import Svg


class ConnectionEdgePoint(Svg):
    """
    Class representing an SVG Element object as Connection Node Edge Point
    """

    # overwrite
    def svg_main(self) -> etree.Element:
        """
        Mothod generating the main SVG Element shaping the TAPI object
        :return SVG Element as main representations for the TAPI object
        """
        main = etree.Element("ellipse")
        main.attrib['cx'] = str(self.center_x())
        main.attrib['cy'] = str(self.center_y())
        main.attrib['rx'] = str(2 * self.FONTSIZE)
        main.attrib['ry'] = str(self.FONTSIZE)
        main.attrib['class'] = " ".join(
            [self.type_name(), self.tapi_object().role()])
        return main

    def svg_label(self) -> etree.Element:
        label = etree.Element('text')
        label.attrib['x'] = str(self.center_x())
        # +4px for font-size 14px (think of chars like 'gjy')
        label.attrib['y'] = str(self.center_y() + 4)
        label.text = self.__label_by_protocol(self.tapi_object().protocol())
        return label

    def __label_by_protocol(self, protocol) -> str:
        mapping: Dict[str, str] = {
            "netconf": "NC",
            "ves": "VES",
            "file": "FTP",
            "nas":"NAS",
            "ofh": "OFH",
            "radio": "RF",
            "rest": "REST",
            "restconf": "RC",
            "sctp": "SCTP",
            "unknown": "-"
        }
        search = protocol.split(":")[1]
        if search in mapping:
            return mapping[search]
        return protocol
