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
An abstract Class for O-RAN Node
"""
from abc import abstractmethod
from typing import Any, Dict
from model.python.ORanObject import IORanObject, ORanObject

# Define an abstract O-RAN Node class
class ORanNode(ORanObject):
    def __init__(self, of: IORanObject = None, **kwargs):
        super().__init__(of, **kwargs)
        self._terminationPoints = []

    @property
    def terminationPoints(self):
        return self._terminationPoints

    def toTopology(self):
        result:Dict[str, Any] = {
            "node-id": self.name,
            "ietf-network-topology:termination-point": self.terminationPoints
        }
        return result

    @abstractmethod
    def toKml(self):
        pass

    @abstractmethod
    def toSvg(self):
        pass