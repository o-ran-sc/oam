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
A Class representing a 3GPP new radio cell du (NrCellDu)
"""
from model.python.o_ran_object import IORanObject
from model.python.o_ran_node import ORanNode
import xml.etree.ElementTree as ET


# Define the "INrCellDu" interface
class INrCellDu(IORanObject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


# Define an abstract O-RAN Node class
class NrCellDu(ORanNode, INrCellDu):
    def __init__(self, o_ran_smo_data: INrCellDu = None, **kwargs):
        super().__init__(o_ran_smo_data, **kwargs)

    def toKml(self) -> None:
        return None

    def toSvg(self) -> None:
        return None
