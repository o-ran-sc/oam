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
Provides functions to convert the Network into different formats
"""

import json
from model.python.o_ran_network import ORanNetwork
import xml.etree.ElementTree as ET


class NetworkViewer:
    """
    This class contains all functions converting the Network into different formats
    """
    __network: ORanNetwork = None

    # constructor
    def __init__(self, network: ORanNetwork):
        self.__network = network

    # json format

    def json(self) -> 'NetworkViewer':
        """
        Getter returns the class as json object
        :return The class itself, as it is json serializable
        """
        return self

    def show_as_json(self) -> dict:
        """
        Method printing the class in json format.
        """
        print(self.__network.json())

    def show(self):
        """
        Method printing the network
        """
        print(self.__network)

    def save(self, filename: str):
        """
        Method saving the class content to a file in json format.
        :param filename: A valid path to a file on the system.
        :type filename: string
        """
        with open(filename, "w", encoding='utf-8') as json_file:
            output = self.__network.toTopology()
            json.dump(output, json_file,
                      ensure_ascii=False, indent=2)
            print("File '" + filename + "' saved!")

    def readStylesFromFile(self) -> str:
        """
        Method reading the css styles from known file
        return: content of the file as string
        """
        with open('view/svg.style.css') as styles:
            content = styles.read()
            return content

    def svg(self, filename: str):
        """
        Method saving the class content to a file in xml/svg format.

        :param filename: A valid path to a file on the system.
        :type filename: string
        """
        root = self.__network.toSvg()
        style = ET.Element("style")
        style.text = self.readStylesFromFile()
        root.findall(".//desc")[0].append(style)
        ET.ElementTree(root).write(filename,
                                      encoding="utf-8",
                                      xml_declaration=True
                                      )
        print("File '" + filename + "' saved!")

    def kml(self, filename: str):
        """
        Method saving the class content to a file in xml/kml format.

        :param filename: A valid path to a file on the system.
        :type filename: string
        """
        root = self.__network.toKml()
        style = ET.Element("style")
        style.text = self.readStylesFromFile()
        root.append(style)
        ET.ElementTree(root).write(filename,
                                      encoding="utf-8",
                                      xml_declaration=True
                                      )
        print("File '" + filename + "' saved!")
