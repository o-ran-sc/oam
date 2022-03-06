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
Provides functions to convert the Network into different formats
"""

import json
from lxml import etree
from model.python.tapi_common_context import TapiCommonContext


class NetworkViewer:
    """
    This class contains all functions converting the Network into different formats
    """
    __network: TapiCommonContext = None

    # constructor
    def __init__(self, network: TapiCommonContext):
        self.__network = network

    # json format

    def json(self) -> 'NetworkViewer':
        """
        Getter returns the class as json object
        :return The class itsself, as it is json serializable
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
            output = self.__network.json()
            json.dump(output, json_file,
                      ensure_ascii=False, indent=2)
            for key in ["Node", "Link"]:
                print(key + "s:", len(output
                                      ["tapi-common:context"]
                                      ["tapi-topology:topology-context"]
                                      ["topology"][0][key.lower()])
                      )
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
        root = self.__network.svg(0, 0)
        # not preferred see OAM-257
        # root.addprevious(
        #     etree.ProcessingInstruction("xml-stylesheet",
        #                                 'href="svg.style.css" type="text/css"')
        # )
        style = etree.Element("style")
        style.text = self.readStylesFromFile()
        root.getchildren()[0].addnext(style)
        etree.ElementTree(root).write(filename,
                                      encoding="utf-8",
                                      xml_declaration=True,
                                      doctype=(
                                          '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"\n'
                                          '  "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">'
                                      ),
                                      pretty_print=True
                                      )
        print("File '" + filename + "' saved!")
