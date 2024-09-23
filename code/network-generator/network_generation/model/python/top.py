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
An abstract Class for all classes
"""
from abc import ABC, abstractmethod
from typing import Any, TypedDict, cast

from network_generation.model.python.type_definitions import (
    AdministrativeState,
    AlarmState,
    LifeCycleState,
    OperationalState,
    UsageState,
    Utilization,
)


# Define the ITop interface
class ITop(TypedDict):
    id: str
    name: str
    administrativeState: AdministrativeState
    operationalState: OperationalState
    lifeCycleState: LifeCycleState
    alarmState: AlarmState
    usageState: UsageState
    utilization: Utilization


# define default value
default_value: ITop = {
    "id": "be5229af-2660-4bae-8f2c-b9d0f788fad1",
    "name": "NoName",
    "administrativeState": AdministrativeState.LOCKED,
    "operationalState": OperationalState.DISABLED,
    "lifeCycleState": LifeCycleState.PLANNED,
    "alarmState": 0,
    "usageState": UsageState.UNUSED,
    "utilization": 0,
}


# Define the Top class
class Top(ABC):
    @staticmethod
    def default() -> dict[str, Any]:
        return cast(dict[str, Any], default_value)

    def __init__(
        self, data: dict[str, Any] = cast(dict[str, Any], default_value)
    ) -> None:
        super().__init__()
        itop: ITop = self._to_itop_data(data)
        self._id: str = itop["id"]
        self._name: str = itop["name"]
        self._administrativeState: AdministrativeState = itop[
            "administrativeState"
        ]
        self._operationalState: OperationalState = itop["operationalState"]
        self._lifeCycleState: LifeCycleState = itop["lifeCycleState"]
        self._alarmState: AlarmState = itop["alarmState"]
        self._usageState: UsageState = itop["usageState"]
        self._utilization: Utilization = itop["utilization"]

    def _to_itop_data(self, data: dict[str, Any]) -> ITop:
        result: ITop = default_value
        for key, key_type in ITop.__annotations__.items():
            if key in data:
                result[key] = data[key]  # type: ignore
        return result

    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, value: str) -> None:
        self._id = value

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def administrativeState(self) -> AdministrativeState:
        return self._administrativeState

    @administrativeState.setter
    def administrativeState(self, value: AdministrativeState) -> None:
        self._administrativeState = value

    @property
    def operationalState(self) -> OperationalState:
        return self._operationalState

    @operationalState.setter
    def operationalState(self, value: OperationalState) -> None:
        self._operationalState = value

    @property
    def lifeCycleState(self) -> LifeCycleState:
        return self._lifeCycleState

    @lifeCycleState.setter
    def lifeCycleState(self, value: LifeCycleState) -> None:
        self._lifeCycleState = value

    @property
    def alarmState(self) -> AlarmState:
        return self._alarmState

    @alarmState.setter
    def alarmState(self, value: AlarmState) -> None:
        self._alarmState = value

    @property
    def usageState(self) -> UsageState:
        return self._usageState

    @usageState.setter
    def usageState(self, value: UsageState) -> None:
        self._usageState = value

    @property
    def utilization(self) -> Utilization:
        return self._utilization

    @utilization.setter
    def utilization(self, value: Utilization) -> None:
        self._utilization = value

    @abstractmethod
    def json(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "administrativeState": self.administrativeState,
            "operationalState": self.operationalState,
            "lifeCycleState": self.lifeCycleState,
            "alarmState": self.alarmState,
            "usageState": self.usageState,
            "utilization": self.utilization,
        }

    def __str__(self) -> str:
        return str(self.json())
