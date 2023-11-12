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

from network_generation.model.python.countries import Country
from network_generation.model.python.type_definitions import (
    AdministrativeState,
    AddressType,
    AlarmState,
    LifeCycleState,
    OperationalState,
    UsageState,
    Utilization,
)


def test_type_definitions() -> None:
    administrative_state: AdministrativeState = AdministrativeState.LOCKED
    assert administrative_state.name == "LOCKED"

    address_type: AddressType = {
        "street": "Hähnelstraße 6",
        "building": "b001",
        "room": "EG rechts",
        "city": "Berlin",
        "zip": "12159",
        "state": "Berlin",
        "country": Country.Germany,
    }
    assert (
        str(address_type)
        == "{'street': 'Hähnelstraße 6', 'building': 'b001', "
        + "'room': 'EG rechts', 'city': 'Berlin', 'zip': '12159', "
        + "'state': 'Berlin', 'country': <Country.Germany: 'Germany'>}"
    )

    alarm_state: AlarmState = 1
    assert alarm_state == 1

    life_cycle_state: LifeCycleState = LifeCycleState.PLANNED
    assert str(life_cycle_state.name) == "PLANNED"

    operational_state: OperationalState = OperationalState.ENABLED
    assert str(operational_state.name) == "ENABLED"

    usage_state: UsageState = UsageState.UNUSED
    assert str(usage_state.name) == "UNUSED"

    utilization: Utilization = 1
    assert utilization == 1
