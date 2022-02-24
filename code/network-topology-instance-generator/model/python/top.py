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


class Top:
    """
    The abstract "Top" class adds common functions
    """

    FONTSIZE: int = 10  # see svg.style.css file
    __configuration: dict
    __data: dict

    def __init__(self, configuration) -> None:
        self.__configuration = configuration

    def configuration(self) -> dict:
        """
        Returns the object initial configuration.
        """
        raise NotImplementedError('subclasses must override configuration()!')

    def data(self) -> dict:
        """
        Returns the class data.
        """
        raise NotImplementedError('subclasses must override data()!')

    def identifier(self) -> str:
        """
        Returns the name of the class object.
        """
        raise NotImplementedError('subclasses must override identifier()!')

    def json(self) -> dict:
        """
        Returns the class content in json format.
        """
        raise NotImplementedError('subclasses must override json()!')

    def name(self) -> str:
        """
        Returns the identifier of the class object.
        It is preferred a UUID according to RFC4122.
        """
        raise NotImplementedError('subclasses must override name()!')

    def svg(self, svg_x: int, svg_y: int) -> etree.Element:
        """
        Returns an lxml.etree.Element object.
        """
        raise NotImplementedError('subclasses must override svg()!')
