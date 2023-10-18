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
An abstract Class for O-RAN Objects
"""
from abc import ABC, abstractmethod
from typing import Dict

import model.python.hexagon as Hexagon
from model.python.hexagon import Hex, Layout, Point
from model.python.o_ran_spiral_radius_profile import SpiralRadiusProfile
from model.python.top import ITop, Top
from model.python.type_definitions import (
    AddressType,
)
from model.python.geo_location import GeoLocation


# Define the "IORanObject" interface
class IORanObject(ITop):
    def __init__(
        self,
        address: AddressType = None,
        geoLocation: GeoLocation = None,
        url: str = None,
        position: Hex = None,
        layout: Layout = None,
        spiralRadiusProfile: SpiralRadiusProfile = None,
        parent  = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.address = address
        self.geoLocation = geoLocation
        self.url = url
        self.position = position
        self.layout = layout
        self.spiralRadiusProfile  = spiralRadiusProfile,
        self.parent  = parent


# Define an abstract O-RAN Object class
class ORanObject(Top, IORanObject):
    def __init__(self, of: IORanObject = None, **kwargs):
        super().__init__(**kwargs)
        self.address = of["address"] if of and "address" in of else None
        self.geoLocation = (
            of["geoLocation"] if of and "geoLocation" in of else GeoLocation()
        )
        self.url = of["url"] if of and "url" in of else self.id
        self.position = of["position"] if of and "position" in of else Hex(0,0,0)
        self.layout = of["layout"] if of and "layout" in of else Layout(Hexagon.layout_flat, Point(1,1), Point(0,0))
        self.spiralRadiusProfile = of["spiralRadiusProfile"] if of and "spiralRadiusProfile" in of else SpiralRadiusProfile()
        self.parent = of["parent"] if of and "parent" in of else None

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, value):
        self._address = value

    @property
    def geoLocation(self):
        return self._geographicalLocation

    @geoLocation.setter
    def geoLocation(self, value):
        self._geographicalLocation = value

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        self._url = value

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value

    @property
    def layout(self):
        return self._layout

    @layout.setter
    def layout(self, value):
        self._layout = value

    @property
    def spiralRadiusProfile(self):
        return self._spiralRadiusProfile

    @spiralRadiusProfile.setter
    def spiralRadiusProfile(self, value):
        self._spiralRadiusProfile = value

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value):
        self._parent = value

    def json(self):
        result :Dict = super().json()
        result['address'] = self.address
        result['geoLocation'] = self.geoLocation
        result['url'] = self.url
        result['layout'] = self.layout
        result['spiralRadiusProfile'] = self.spiralRadiusProfile
        result['parent'] = self.parent
        return result

    def __str__(self):
        return str(self.json())
    
    @abstractmethod
    def toTopology(self):
        pass

    @abstractmethod
    def toKml(self):
        pass

    @abstractmethod
    def toSvg(self):
        pass
