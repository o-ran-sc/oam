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
from abc import abstractmethod
from typing import Dict

from model.python.top import ITop, Top
from model.python.geo_location import GeoLocation


# Define the "IORanObject" interface
class IORanObject(ITop):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


# Define an abstract O-RAN Object class
class ORanObject(Top, IORanObject):
    def __init__(self, of: IORanObject = None, **kwargs):
        super().__init__(**kwargs)

    def json(self):
        result: Dict = super().json()
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
