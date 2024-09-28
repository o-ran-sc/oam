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
An abstract Class for O-RAN TerminationPoint
"""
from typing import Any, cast

from network_generation.model.python.o_ran_object import (
    IORanObject,
    ORanObject
)


# Define the "IORanObject" interface
class IORanTerminationPoint(IORanObject):
    supporter: dict[str, str]


default_value: IORanTerminationPoint = cast(
    IORanTerminationPoint,
    {
        **ORanObject.default(),
        **{
            "supporter": {}
        },
    },
)


# Define an O-RAN Termination Point
# (ietf-interface, onf:logical-termination-point) class
class ORanTerminationPoint(ORanObject):
    @staticmethod
    def default() -> dict[str, Any]:
        return cast(dict[str, Any], default_value)

    def __init__(
        self, data: dict[str, Any] = default(), **kwargs: dict[str, Any]
    ) -> None:
        itp: IORanTerminationPoint = self._to_itp_data(data)
        super().__init__(cast(dict[str, Any], itp), **kwargs)
        self._supporter = cast(dict[str, str], itp["supporter"])

    def _to_itp_data(self, data: dict[str, Any]) -> IORanTerminationPoint:
        result: IORanTerminationPoint = default_value
        for key, key_type in IORanTerminationPoint.__annotations__.items():
            if key in data:
                result[key] = data[key]  # type: ignore
        return result

    @property
    def supporter(self) -> dict[str, str]:
        return self._supporter

    @supporter.setter
    def supporter(self, value: dict[str, str]) -> None:
        self._supporter = value

    def to_topology(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "tp-id": self.name,
            "o-ran-sc-network:uuid": self.id,
            "o-ran-sc-network:type": self.type,
        }
        if self.supporter:
            result["supporting-termination-point"] = [self.supporter]
        return result
