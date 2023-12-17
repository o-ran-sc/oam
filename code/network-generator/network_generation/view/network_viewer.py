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
Provides functions to convert the Network into different formats
"""

import gzip
import json
from typing_extensions import Buffer
import zipfile
import xml.etree.ElementTree as ET
from typing import Any

from network_generation.model.python.o_ran_network import ORanNetwork


class NetworkViewer:
    """
    This class contains all functions converting the Network into
    different formats
    """

    # constructor
    def __init__(self, network: ORanNetwork) -> None:
        self.__network = network

    # json format

    def json(self) -> "NetworkViewer":
        """
        Getter returns the class as json object
        :return The class itself, as it is json serializable
        """
        return self

    def show_as_json(self) -> None:
        """
        Method printing the class in json format.
        """
        print(self.__network.json())

    def show(self) -> None:
        """
        Method printing the network
        """
        print(self.__network)

    def save(self, filename: str, compressed: bool = True) -> None:
        """
        Method saving the class content to a file in json format.
        :param filename: A valid path to a file on the system.
        :param compressed: if True, svg is stored as svgz format.
        :type filename: string
        """
        output: dict[str, Any] = self.__network.to_topology()
        if compressed is True:
            with gzip.open(f'{filename}-operational.json.gz', 'wb') as zf:
                zf.write(json.dumps(output, indent=2).encode('utf-8'))
            print(f'File "{filename}-operational.json.gz" saved!')
        else:
            with open(
                f'{filename}-operational.json', "w", encoding="utf-8"
            ) as jf:
                json.dump(output, jf, ensure_ascii=False, indent=2)
            print(f'File "{filename}-operational.json" saved!')

    def readStylesFromFile(self) -> str:
        """
        Method reading the css styles from known file
        return: content of the file as string
        """
        with open("network_generation/view/svg.style.css") as styles:
            content = styles.read()
            return content

    def svg(self, filename: str, compressed: bool = True) -> None:
        """
        Method saving the class content to a file in xml/svg format.

        :param filename: A valid path to a file on the system.
        :param compressed: if True, svg is stored as svgz format.
        :type filename: string
        """
        root = self.__network.toSvg()
        style = ET.Element("style")
        style.text = self.readStylesFromFile()
        root.findall(".//desc")[0].append(style)

        if compressed is True:
            svg_output: Buffer = ET.tostring(
                root, encoding="utf-8", xml_declaration=True)
            with gzip.open(f'{filename}.svgz', 'wb') as zf:
                zf.write(svg_output)
            print(f'File "{filename}.svgz" saved!')
        else:
            ET.ElementTree(root).write(
                f'{filename}.svg', encoding="utf-8", xml_declaration=True
            )
            print(f'File "{filename}.svg" saved!')

    def kml(self, filename: str, compressed: bool = True) -> None:
        """
        Method saving the class content to a file in xml/kml format.

        :param filename: A valid path to a file on the system.
        :param compressed: if True, kml is stored as kmz format.
        :type filename: string
        """
        root = self.__network.toKml()
        with open("network_generation/view/kml.styles.json") as kml_styles:
            styles: dict[str, dict] = json.load(kml_styles)
            for key, value in styles.items():
                # add style
                style = ET.Element("Style", {"id": key})
                line_style = ET.SubElement(style, "LineStyle")
                color = ET.SubElement(line_style, "color")
                color.text = str(value["stroke"]["color"])
                width = ET.SubElement(line_style, "width")
                width.text = str(value["stroke"]["width"])
                poly_style = ET.SubElement(style, "PolyStyle")
                fill = ET.SubElement(poly_style, "color")
                fill.text = str(value["fill"]["color"])
                root.findall(".//Document")[0].append(style)

        kml: str = ET.tostring(
            root, encoding="utf-8", xml_declaration=True)
        if compressed is True:
            with zipfile.ZipFile(
                f'{filename}.kmz', 'w', zipfile.ZIP_DEFLATED
            ) as zf:
                zf.writestr(f'{filename.split("/")[1]}.kml', data=kml)
            print(f'File "{filename}.kmz" saved!')
        else:
            kml_file = open(f'{filename}.kml', 'w')
            kml_file.write(kml)
            kml_file.close()
            print(f'File "{filename}.kml" saved!')
