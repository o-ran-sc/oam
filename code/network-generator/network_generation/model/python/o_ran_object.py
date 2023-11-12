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

# !/usr/bin/python

"""
An abstract Class for O-RAN Objects
"""
from typing import Any, cast

from network_generation.model.python.top import ITop, Top, default_value

# Define the "IORanObject" interface
# class IORanObject(ITop):
IORanObject = ITop


# Define an abstract O-RAN Object class
class ORanObject(Top):
    @staticmethod
    def default() -> dict[str, Any]:
        return cast(dict[str, Any], default_value)

    def __init__(
        self, data: dict[str, Any] = default(), **kwargs: dict[str, Any]
    ) -> None:
        super().__init__(data, **kwargs)

    def json(self) -> dict[str, Any]:
        return {
            **super().json(),
            "id": self.id,
            "name": self.name,
            "administrativeState": self.administrativeState,
            "operationalState": self.operationalState,
            "lifeCycleState": self.lifeCycleState,
            "alarmState": self.alarmState,
            "usageState": self.usageState,
            "utilization": self.utilization,
        }
