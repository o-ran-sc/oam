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
A Class representing a Tower to mount O-RAN RUx
"""
from typing import Any, Dict

from model.python.o_ran_object import IORanObject
from model.python.o_ran_node import ORanNode


# Define an abstract O-RAN Node class
class Tower(ORanNode):
    def __init__(self, of: IORanObject = None, **kwargs):
        super().__init__(of, **kwargs)

    def toKml(self):
        return None

    def toSvg(self):
        return None
