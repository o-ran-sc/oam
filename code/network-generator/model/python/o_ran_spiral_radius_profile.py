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

from dataclasses import dataclass
from typing import Any

from model.python.cube import Cube
from model.python.hexagon import Hex


class SpiralRadiusProfile:
    def __init__(self, data: [dict[str, Any] | None] = None):
        self._oRanSmoSpiralRadiusOfNearRtRics = (
            data.get("oRanSmoSpiralRadiusOfNearRtRics", 1) if data else 1
        )
        self._oRanNearRtRicSpiralRadiusOfOCus = (
            data.get("oRanNearRtRicSpiralRadiusOfOCus", 1) if data else 1
        )
        self._oRanCuSpiralRadiusOfODus = (
            data.get("oRanCuSpiralRadiusOfODus", 1) if data else 1
        )
        self._oRanDuSpiralRadiusOfTowers = (
            data.get("oRanDuSpiralRadiusOfTowers", 1) if data else 1
        )

    @property
    def id(self) -> str:
        return f"{self._oRanDuSpiralRadiusOfTowers}{self._oRanCuSpiralRadiusOfODus}{self._oRanNearRtRicSpiralRadiusOfOCus}{self._oRanSmoSpiralRadiusOfNearRtRics}"

    @property
    def count(self) -> int:
        towers = 1
        dus = 1
        cus = 1
        rics = 1

        for ru in range(self._oRanDuSpiralRadiusOfTowers + 1):
            towers = towers + 6 * ru

        for du in range(self._oRanCuSpiralRadiusOfODus + 1):
            dus = dus + 6 * du

        for cu in range(self._oRanNearRtRicSpiralRadiusOfOCus + 1):
            cus = cus + 6 * cu

        for ric in range(self._oRanSmoSpiralRadiusOfNearRtRics + 1):
            rics = rics + 6 * ric

        return towers * dus * cus * rics

    @property
    def oRanSmoSpiralRadiusOfNearRtRics(self) -> int:
        return self._oRanSmoSpiralRadiusOfNearRtRics

    @oRanSmoSpiralRadiusOfNearRtRics.setter
    def oRanSmoSpiralRadiusOfNearRtRics(self, value: int):
        self._oRanSmoSpiralRadiusOfNearRtRics = value

    @property
    def oRanNearRtRicSpiralRadiusOfOCus(self) -> int:
        return self._oRanNearRtRicSpiralRadiusOfOCus

    @oRanNearRtRicSpiralRadiusOfOCus.setter
    def oRanNearRtRicSpiralRadiusOfOCus(self, value: int):
        self._oRanNearRtRicSpiralRadiusOfOCus = value

    @property
    def oRanCuSpiralRadiusOfODus(self) -> int:
        return self._oRanCuSpiralRadiusOfODus

    @oRanCuSpiralRadiusOfODus.setter
    def oRanCuSpiralRadiusOfODus(self, value: int):
        self._oRanCuSpiralRadiusOfODus = value

    @property
    def oRanDuSpiralRadiusOfTowers(self) -> int:
        return self._oRanDuSpiralRadiusOfTowers

    @oRanDuSpiralRadiusOfTowers.setter
    def oRanDuSpiralRadiusOfTowers(self, value: int):
        self._oRanDuSpiralRadiusOfTowers = value

    @property
    def sectors(self) -> int:
        return self._sectors

    @sectors.setter
    def sectors(self, value: int):
        self._sectors = value

    @property
    def nrDuCellsPerSector(self) -> int:
        return self._nrDuCellsPerSector

    @nrDuCellsPerSector.setter
    def nrDuCellsPerSector(self, value: int):
        self._nrDuCellsPerSector = value

    def oRanDuDirections(self) -> list[Hex]:
        q = 2 * self._oRanDuSpiralRadiusOfTowers + 1
        r = -self._oRanDuSpiralRadiusOfTowers - 1
        s = -q - r
        return [
            Hex(q, r, s),
            Hex(-s, -q, -r),
            Hex(r, s, q),
            Hex(-q, -r, -s),
            Hex(s, q, r),
            Hex(-r, -s, -q),
        ]

    def oRanDuNeighbor(self, cube: Cube, direction: int):
        return Hex.add(cube, self.oRanDuDirections[direction])

    def oRanDuRing(self, center: Hex, radius: int) -> list[Hex]:
        if radius <= 0:
            raise ValueError(
                "Invalid radius. The radius around the hex center must be greater than 0 rings."
            )
        results: list[Hex] = []
        hex = Hex.add(center, Hex.scale(self.oRanDuDirections[4], radius))
        for i in range(6):
            for j in range(radius):
                results.append(hex)
                hex = self.oRanDuNeighbor(hex, i)
        return results

    def oRanDuSpiral(self, center: Hex, radius: int) -> list[Hex]:
        result: list[Hex] = [center]
        for k in range(1, radius + 1):
            result.extend(self.oRanDuRing(center, k))
        return result

    def oRanNearRtRicDirections(self) -> list[Hex]:
        q0 = (
            2 * self.oRanCuSpiralRadiusOfODus
            + 3 * self.oRanCuSpiralRadiusOfODus * self.oRanDuSpiralRadiusOfORus
            + self.oRanDuSpiralRadiusOfORus
            + 1
        )
        r0 = self.oRanDuSpiralRadiusOfORus - self.oRanCuSpiralRadiusOfODus

        q = 3 * q0 - self.oRanNearRtRicSpiralRadiusOfOCus
        r = -r0 - self.oRanNearRtRicSpiralRadiusOfOCus

        profile_id = self.id[2:-1]

        if profile_id in {"111", "112", "113", "114"}:
            q = 21 + 14 * (self.oRanNearRtRicSpiralRadiusOfOCus - 1)
            r = -7 * self.oRanNearRtRicSpiralRadiusOfOCus
        elif profile_id in {"121", "122", "123", "124"}:
            q = 25 + 13 * (self.oRanNearRtRicSpiralRadiusOfOCus - 1)
            r = 9 + 10 * (self.oRanNearRtRicSpiralRadiusOfOCus - 1)
        elif profile_id in {"131", "132"}:
            q = 49 + 30 * (self.oRanNearRtRicSpiralRadiusOfOCus - 1)
            r = -21 - 34 * (self.oRanNearRtRicSpiralRadiusOfOCus - 1)
        elif profile_id == "133":
            q = 74
            r = 37
        elif profile_id == "134":
            q = 93
            r = 50
        elif profile_id in {"211", "212", "213", "214"}:
            q = 34 + 23 * (self.oRanNearRtRicSpiralRadiusOfOCus - 1)
            r = -10 * self.oRanNearRtRicSpiralRadiusOfOCus - 1
        elif profile_id in {"221", "222", "223", "224"}:
            q = 57 + 38 * (self.oRanNearRtRicSpiralRadiusOfOCus - 1)
            r = -19 * self.oRanNearRtRicSpiralRadiusOfOCus
        elif profile_id in {"231", "232", "233", "234"}:
            q = 80 + 53 * (self.oRanNearRtRicSpiralRadiusOfOCus - 1)
            r = -28 * self.oRanNearRtRicSpiralRadiusOfOCus - 1
        elif profile_id in {"241", "242", "243", "244"}:
            q = 103 + 68 * (self.oRanNearRtRicSpiralRadiusOfOCus - 1)
            r = -39 * self.oRanNearRtRicSpiralRadiusOfOCus + 2 * (
                self.oRanNearRtRicSpiralRadiusOfOCus - 1
            )
        elif profile_id in {"311", "312", "313", "314"}:
            q = 47 + 32 * (self.oRanNearRtRicSpiralRadiusOfOCus - 1)
            r = -11 - 13 * (self.oRanNearRtRicSpiralRadiusOfOCus - 1)
        elif profile_id in {"321", "322", "323", "324"}:
            q = 79 + 53 * (self.oRanNearRtRicSpiralRadiusOfOCus - 1)
            r = -24 - 25 * (self.oRanNearRtRicSpiralRadiusOfOCus - 1)
        elif profile_id in {"331", "332", "333", "334"}:
            q = 111 + 75 * (self.oRanNearRtRicSpiralRadiusOfOCus - 1)
            r = -37 - 37 * (self.oRanNearRtRicSpiralRadiusOfOCus - 1)
        else:
            # Handle the default case or raise a warning
            pass

        s = -q - r
        return [
            Hex(q, r, s),
            Hex(-s, -q, -r),
            Hex(r, s, q),
            Hex(-q, -r, -s),
            Hex(s, q, r),
            Hex(-r, -s, -q),
        ]
