# Copyright 2024 highstreet technologies GmbH
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
Provides functions to convert the Network into different formats
"""

import gzip
import json
import xml.etree.ElementTree as ET
import zipfile
from typing import Any

from typing_extensions import Buffer

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

    def to_directory(self, parent_dir: str) -> None:
        """
        Method converting the network to a subdirectory file structure
        """
        self.__network.to_directory(parent_dir)
        print(f'Directory structure saved to "{parent_dir}"')

    def __save_on_disc(
        self, filename: str, compressed: bool, content: Any
    ) -> None:
        if compressed is True:
            with gzip.open(f"{filename}.gz", "wb") as zf:
                zf.write(json.dumps(content, indent=2).encode("utf-8"))
            print(f'File "{filename}.gz" saved!')
        else:
            with open(f"{filename}", "w", encoding="utf-8") as jf:
                json.dump(content, jf, ensure_ascii=False, indent=2)
            print(f'File "{filename}" saved!')

    def __save_on_disc_teiv_cloudevent(
        self, filename: str, content: Any, cloud_event_header: str
    ) -> None:
        with open(f"{filename}", "w", encoding="utf-8") as jf:
            jf.write(cloud_event_header)
            json.dump(content, jf, ensure_ascii=False, indent=2)
        print(f'File "{filename}" saved!')

    def rfc8345(self, filename: str, compressed: bool = True) -> None:
        """
        Method saving the class content to a file in json format.
        :param filename: A valid path to a file on the system.
        :param compressed: if True, svg is stored as json format.
        :type filename: string
        """
        output: dict[str, Any] = self.__network.to_topology()
        file_extension: str = "-operational.json"
        self.__save_on_disc(f"{filename}{file_extension}", compressed, output)

    def teiv(self, filename: str, compressed: bool = True) -> None:
        """
        Method for saving the class content as teiv cloud event
        data in json format and in small chunks of cloud event text files.
        :param filename: A valid path to a file on the system.
        :param compressed: if True, json is stored as gz format.
        :type filename: string
        """
        output: dict[str, list[dict[str, list[dict[str, Any]]]]] = (
            self.__network.to_teiv_data()
        )
        chunk_size: int = 600
        entities = output.get("entities", [])
        relationships = output.get("relationships", [])
        self.save_teiv_as_chunks("entities", entities, chunk_size, filename)
        self.save_teiv_as_chunks(
            "relationships", relationships, chunk_size, filename
        )
        self.__save_on_disc(f"{filename}-teiv-data.json", compressed, output)

    def save_teiv_as_chunks(
        self,
        type: str,
        data: list[dict[str, Any]],
        chunk_size: int,
        filename: str,
    ) -> None:
        """
        Method for saving the class content as teiv cloud event
        data in small chunks of cloud event text files.
        :param type: type of node.
        :param data: the data to be split.
        :param chunk_size: amount of nodes per cloud event
        :param filename: a valid path to a file on the system.
        """
        cloud_event_header = "ce_specversion:::1.0,ce_id:::a30e63c9-d29e" \
            "-46ff-b99a-b63ed83fd237,ce_source:::dmi-plugin:nm-1,ce_type:::" \
            "ran-logical-topology.merge,content-type:::application/yang-" \
            "data+json,ce_time:::2023-11-30T09:05:00Z,ce_dataschema:::https" \
            "://ties:8080/schemas/v1/r1-topology,,,"
        idx = 1
        for items in data:
            for key, value in items.items():
                for i in range(0, len(value), chunk_size):
                    full_filename = f"{filename}-teiv-{type}-data-part" \
                        f"-{idx}-{i // chunk_size + 1}.txt"
                    chunk: dict[str, Any] = {
                        type: [{key: value[i: i + chunk_size]}]
                    }
                    self.__save_on_disc_teiv_cloudevent(
                        full_filename,
                        chunk,
                        cloud_event_header,
                    )
                idx = idx + 1

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
                root, encoding="utf-8", xml_declaration=True
            )
            with gzip.open(f"{filename}.svgz", "wb") as zf:
                zf.write(svg_output)
            print(f'File "{filename}.svgz" saved!')
        else:
            ET.ElementTree(root).write(
                f"{filename}.svg", encoding="utf-8", xml_declaration=True
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
                label_style = ET.SubElement(style, "LabelStyle")
                label_scale = ET.SubElement(label_style, "scale")
                label_scale.text = "0"

                icon_style = ET.SubElement(style, "IconStyle")
                icon_color = ET.SubElement(icon_style, "color")
                icon_color.text = str(value["stroke"]["color"])
                scale = ET.SubElement(icon_style, "scale")
                scale.text = "0.5"
                icon = ET.SubElement(icon_style, "Icon")
                href = ET.SubElement(icon, "href")
                href.text = (
                    "http://maps.google.com/mapfiles/kml/shapes"
                    "/placemark_circle.png")
                line_style = ET.SubElement(style, "LineStyle")
                color = ET.SubElement(line_style, "color")
                color.text = str(value["stroke"]["color"])
                width = ET.SubElement(line_style, "width")
                width.text = str(value["stroke"]["width"])
                poly_style = ET.SubElement(style, "PolyStyle")
                fill = ET.SubElement(poly_style, "color")
                fill.text = str(value["fill"]["color"])
                root.findall(".//Document")[0].append(style)

        kml: str = ET.tostring(root, encoding="utf-8", xml_declaration=True)
        if compressed is True:
            with zipfile.ZipFile(
                f"{filename}.kmz", "w", zipfile.ZIP_DEFLATED
            ) as zf:
                zf.writestr(f'{filename.split("/")[1]}.kml', data=kml)
            print(f'File "{filename}.kmz" saved!')
        else:
            kml_file = open(f"{filename}.kml", "wb")
            # TODO make lint issue
            # network_generation/view/network_viewer.py:160: error:
            # Argument 1 to "write" of "BufcqferedWriter" has incompatible
            # type "str"; expected "Buffer"
            kml_file.write(kml)
            kml_file.close()
            print(f'File "{filename}.kml" saved!')
