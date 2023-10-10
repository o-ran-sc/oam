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
from abc import ABC, abstractmethod
from typing import Optional, Dict, Union
from model.python.TypeDefinitions import (
    AddressType,
    AdministrativeState,
    OperationalState,
    UsageState,
    Utilization,
    LifeCycleState,
    AlarmState,
)
from model.python.GeoLocation import GeoLocation


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
class Top(ITop):
    def __init__(self, data=None):
        self._id = data.id if data and data.id else str(uuid.uuid4())
        self._name = (
            data.name if data and data.name else " ".join(["Name", "of", self._id])
        )
        self._administrativeState = (
            data.administrativeState
            if data and data.administrativeState
            else AdministrativeState.LOCKED
        )
        self._operationalState = (
            data.operationalState
            if data and data.operationalState
            else OperationalState.DISABLED
        )
        self._lifeCycleState = (
            data.lifeCycleState
            if data and data.lifeCycleState
            else LifeCycleState.PLANNED
        )
        self._alarmState = (
            data.alarmState if data and data.alarmState else 0
        )
        self._usageState = (
            data.usageState if data and data.usageState else UsageState.UNUSED
        )
        self._utilization = (
            data.utilization if data and data.utilization else 0
        )

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def administrativeState(self):
        return self._administrativeState

    @administrativeState.setter
    def administrativeState(self, value):
        self._administrativeState = value

    @property
    def operationalState(self):
        return self._operationalState

    @operationalState.setter
    def operationalState(self, value):
        self._operationalState = value

    @property
    def lifeCycleState(self):
        return self._lifeCycleState

    @lifeCycleState.setter
    def lifeCycleState(self, value):
        self._lifeCycleState = value

    @property
    def alarmState(self):
        return self._alarmState

    @alarmState.setter
    def alarmState(self, value):
        self._alarmState = value

    @property
    def usageState(self):
        return self._usageState

    @usageState.setter
    def usageState(self, value):
        self._usageState = value

    @property
    def utilization(self):
        return self._utilization

    @utilization.setter
    def utilization(self, value):
        self._utilization = value

    def json(self):
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

    def __str__(self):
        return str(self.json())
