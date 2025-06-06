# Copyright 2024 highstreet technologies
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

# !/usr/bin/python3

"""
A collection of TypeDefinitions
"""
from enum import Enum
from typing import TypedDict

from network_generation.model.python.countries import Country

# from typing import Any, TypedDict, TypeVar


# from network_generation.model.python.o_ran_node import IORanNode
# from network_generation.model.python.o_ran_object import IORanObject
# from network_generation.model.python.top import ITop

# Generic Types based on inheritance
# IORanType = TypeVar("IORanType", ITop, IORanObject, IORanNode)


# Define AdministrativeState enum
class AdministrativeState(Enum):
    LOCKED = "locked"
    UNLOCKED = "unlocked"
    SHUTTING_DOWN = "shutting down"


# Define AlarmState type
AlarmState = int


# Define Address type
class AddressType(TypedDict):
    street: str
    building: str
    room: str
    city: str
    zip: str
    state: str
    country: Country


# Define OperationalState enum
class OperationalState(Enum):
    ENABLED = "enabled"
    DISABLED = "disabled"


# Define LifeCycleState enum
class LifeCycleState(Enum):
    PLANNED = "planned"
    ORDERED = "ordered"
    INSTALLED = "installed"
    COMMISSIONED = "commissioned"
    TO_BE_DESTROYED = "to be destroyed"
    DESTROYED = "destroyed"


# Define UsageState enum
class UsageState(Enum):
    USED = "used"
    UNUSED = "unused"


Utilization = int
