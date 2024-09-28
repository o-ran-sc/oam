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

from network_generation.model.python.o_ran_termination_point import (
    ORanTerminationPoint,
)
from network_generation.model.python.type_definitions import (
    AdministrativeState,
    OperationalState,
)


def test_o_ran_termination_point() -> None:
    o_ran_termination_point: ORanTerminationPoint = ORanTerminationPoint({
        "name": "my-name",
        "supporter": "my-supporter"
    })
    assert o_ran_termination_point.name == "my-name"
    assert o_ran_termination_point.administrativeState.value == "locked"
    assert o_ran_termination_point.supporter == "my-supporter"
    assert len(str(o_ran_termination_point)) == 357

    o_ran_termination_point = ORanTerminationPoint(
        {
            "id": "my-id",
            "administrativeState": AdministrativeState.UNLOCKED,
            "operationalState": OperationalState.ENABLED,
            "supporter": "my_personal_fan"
        }
    )
    assert len(o_ran_termination_point.id) == 36
    assert o_ran_termination_point.administrativeState.value == "unlocked"
    assert o_ran_termination_point.operationalState.value == "enabled"
    assert o_ran_termination_point.supporter == "my_personal_fan"
    assert len(str(o_ran_termination_point)) == 359
