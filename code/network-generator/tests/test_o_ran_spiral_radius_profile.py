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

from network_generation.model.python.hexagon import Hex
from network_generation.model.python.o_ran_spiral_radius_profile import (
    SpiralRadiusProfile,
)


def test_o_ran_spiral_radius_profile() -> None:
    srp: SpiralRadiusProfile = SpiralRadiusProfile()
    assert srp.count == 7 * 7 * 7 * 7
    assert srp.id == "1111"

    assert str(srp.oRanDuSpiral(Hex(0, 0, 0), 0)[0]) == "q: 0, r: 0, s: 0"

    assert str(srp.oRanCuSpiral(Hex(1, 2, -3), 1)[1]) == "q: -6, r: 9, s: -3"

    assert (
        str(srp.oRanNearRtRicSpiral(Hex(-1, 1, 0), 2)[2])
        == "q: 6, r: 15, s: -21"
    )
