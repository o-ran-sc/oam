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
An abstract Class for all classes
"""
import uuid
from abc import ABC

from network_generation.model.python.type_definitions import (
    AdministrativeState,
    AlarmState,
    LifeCycleState,
    OperationalState,
    UsageState,
    Utilization,
)


# Define the ITop interface
class ITop:
    def __init__(
        self,
        id: str = None,
        name: str = None,
        administrativeState: AdministrativeState = None,
        operationalState: OperationalState = None,
        lifeCycleState: LifeCycleState = None,
        alarmState: AlarmState = None,
        usageState: UsageState = None,
        utilization: Utilization = None,
    ):
        self.id = id
        self.name = name
        self.administrativeState = administrativeState
        self.operationalState = operationalState
        self.lifeCycleState = lifeCycleState
        self.alarmState = alarmState
        self.usageState = usageState
        self.utilization = utilization


# Define the Top class
class Top(ABC, ITop):
    def __init__(self, data: [dict[str, dict] | None] = None):
        self._id = data["id"] if data and "id" in data else str(uuid.uuid4())
        self._name = (
            data["name"]
            if data and "name" in data
            else " ".join(["Name", "of", self._id])
        )
        self._administrativeState = (
            data["administrativeState"]
            if data and "administrativeState" in data
            else AdministrativeState.LOCKED
        )
        self._operationalState = (
            data["operationalState"]
            if data and "operationalState" in data
            else OperationalState.DISABLED
        )
        self._lifeCycleState = (
            data["lifeCycleState"]
            if data and "lifeCycleState" in data
            else LifeCycleState.PLANNED
        )
        self._alarmState = (
            data["alarmState"] if data and "alarmState" in data else 0
        )
        self._usageState = (
            data["usageState"]
            if data and "usageState" in data
            else UsageState.UNUSED
        )
        self._utilization = (
            data["utilization"] if data and "utilization" in data else 0
        )

    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, value: str):
        self._id = value

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    @property
    def administrativeState(self) -> AdministrativeState:
        return self._administrativeState

    @administrativeState.setter
    def administrativeState(self, value: AdministrativeState):
        self._administrativeState = value

    @property
    def operationalState(self) -> OperationalState:
        return self._operationalState

    @operationalState.setter
    def operationalState(self, value: OperationalState):
        self._operationalState = value

    @property
    def lifeCycleState(self) -> LifeCycleState:
        return self._lifeCycleState

    @lifeCycleState.setter
    def lifeCycleState(self, value: LifeCycleState):
        self._lifeCycleState = value

    @property
    def alarmState(self) -> AlarmState:
        return self._alarmState

    @alarmState.setter
    def alarmState(self, value: AlarmState):
        self._alarmState = value

    @property
    def usageState(self) -> UsageState:
        return self._usageState

    @usageState.setter
    def usageState(self, value: UsageState):
        self._usageState = value

    @property
    def utilization(self) -> Utilization:
        return self._utilization

    @utilization.setter
    def utilization(self, value: Utilization):
        self._utilization = value

    def json(self) -> dict[str, dict]:
        return {
            "id": self.id,
            "name": self.name,
            "administrativeState": self.administrativeState.value,
            "operationalState": self.operationalState.value,
            "lifeCycleState": self.lifeCycleState.value,
            "alarmState": self.alarmState,
            "usageState": self.usageState.value,
            "utilization": self.utilization,
        }

    def __str__(self) -> str:
        return str(self.json())
