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
An abstract Class for O-RAN TerminationPoint
"""
from typing import Any, cast

from network_generation.model.python.o_ran_object import (
    IORanObject,
    ORanObject,
)


# Define the "IORanObject" interface
class IORanTerminationPoint(IORanObject):
    supporter: str
    parent: Any


default_value: IORanTerminationPoint = cast(
    IORanTerminationPoint,
    {
        **ORanObject.default(),
        **{
            "supporter": "TerminationPointLayer",
            "parent": None,
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
        self._supporter: str = str(itp["supporter"])
        self._parent: Any = itp["parent"]

    def _to_itp_data(self, data: dict[str, Any]) -> IORanTerminationPoint:
        result: IORanTerminationPoint = default_value
        for key, key_type in IORanTerminationPoint.__annotations__.items():
            if key in data:
                result[key] = data[key]  # type: ignore
        return result

    @property
    def supporter(self) -> str:
        return self._supporter

    @supporter.setter
    def supporter(self, value: str) -> None:
        self._supporter = value

    @property
    def parent(self) -> Any:
        return self._utilization

    @parent.setter
    def parent(self, value: Any) -> None:
        self._parent = value

    def to_topology(self) -> dict[str, Any]:
        result: dict[str, Any] = {"tp-id": self.name}
        if self.supporter and type(self.parent) is not int:
            network_ref: str = ""
            match str(type(self.parent)):
                case "<class 'model.python.o_ran_smo.ORanSmo'>":
                    network_ref = self.parent.parent.id
                case "<class 'model.python.o_ran_near_rt_ric.ORanNearRtRic'>":
                    network_ref = self.parent.parent.parent.id
                case "<class 'model.python.o_ran_cu.ORanCu'>":
                    network_ref = self.parent.parent.parent.parent.id
                case "<class 'model.python.o_ran_du.ORanDu'>":
                    network_ref = self.parent.parent.parent.parent.parent.id
                case "<class 'model.python.o_ran_cloud_du.ORanCloudDu'>":
                    network_ref = self.parent.parent.parent.parent.parent.id
                case "<class 'model.python.o_ran_ru.ORanRu'>":
                    network_ref = (
                        self.parent.parent.parent.parent.parent.parent.id
                    )
                case _:
                    print("unknown: implement " + str(type(self.parent)))
                    network_ref = "unknown: implement " + str(
                        type(self.parent))

            result["supporting-termination-point"] = [
                {
                    "network-ref": network_ref,
                    "node-ref": self.parent.name,
                    "tp-ref": self.supporter,
                }
            ]
        return result
