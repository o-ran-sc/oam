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
A Class representing an O-RAN radio unit (ORanRu)
"""
from model.python.o_ran_object import IORanObject
from model.python.o_ran_node import ORanNode
import xml.etree.ElementTree as ET


# Define the "IORanRu" interface
class IORanRu(IORanObject):
    def __init__(self, cell_count: int, **kwargs):
        super().__init__(**kwargs)
        self._cell_count = cell_count


# Define an abstract O-RAN Node class
class ORanRu(ORanNode, IORanRu):
    def __init__(self, o_ran_ru_data: IORanRu = None, **kwargs):
        super().__init__(o_ran_ru_data, **kwargs)
        self._cell_count = o_ran_ru_data["cellCount"] if o_ran_ru_data and "cellCount" in o_ran_ru_data else 1

    def toKml(self) -> None:
        return None

    def toSvg(self) -> None:
        return None
