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
An abstract Class for O-RAN Functions
"""
from abc import ABC, abstractmethod
from typing import Dict

from model.python.Top import ITop, Top
from model.python.TypeDefinitions import (
    AddressType,
)
from model.python.GeoLocation import GeoLocation


# Define the "IORanFunction" interface
class IORanFunction(ITop):
    def __init__(
        self,
        address: AddressType = None,
        geoLocation: GeoLocation = None,
        url: str = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.address = address
        self.geoLocation = geoLocation
        self.url = url


# Define an abstract O-RAN Function class
class ORanFunction(ABC, Top, IORanFunction):
    def __init__(self, of: IORanFunction = None, **kwargs):
        super().__init__(**kwargs)
        self.address = of["address"] if of and "address" in of else None
        self.geoLocation = (
            of["geoLocation"] if of and "geoLocation" in of else GeoLocation()
        )
        self.url = of["url"] if of and "url" in of else self.id

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

    def json(self):
        result :Dict = super().json()
        result['address'] = self.address
        result['geoLocation'] = self.geoLocation.json()
        result['url'] = self.url
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
