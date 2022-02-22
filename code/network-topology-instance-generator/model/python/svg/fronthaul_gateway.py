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
Module containing a class representing an SVG Element as O-RAN Fronthaul Gateway
"""
from model.python.svg.connection_edge_point import ConnectionEdgePoint
from model.python.svg.node import Node


class FronthaulGateway(Node):
    """
    Class representing an SVG Element object as O-RAN Fronthaul Gateway
    """

    def width(self) -> int:
        """
        Getter for width of the SVG Element
        :return Width in pixel
        """
        self.__width = max(2, len(self.tapi_object().data()[
                           'owned-node-edge-point'])-2)*ConnectionEdgePoint.width(self)
        return self.__width
