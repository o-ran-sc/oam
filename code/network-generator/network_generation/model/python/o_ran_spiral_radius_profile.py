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

import network_generation.model.python.hexagon as Hexagon
from network_generation.model.python.cube import Cube
from network_generation.model.python.hexagon import Hex


class SpiralRadiusProfile:
    def __init__(self, data: [dict[str, dict] | None] = None):
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
        self._nrDuCellsPerSector: int = value

    def oRanDuDirections(self) -> list[Hex]:
        q: int = 2 * self._oRanDuSpiralRadiusOfTowers + 1
        r: int = -self._oRanDuSpiralRadiusOfTowers - 1
        s: int = -q - r
        return [
            Hex(q, r, s),
            Hex(-s, -q, -r),
            Hex(r, s, q),
            Hex(-q, -r, -s),
            Hex(s, q, r),
            Hex(-r, -s, -q),
        ]

    def oRanDuNeighbor(self, cube: Cube, direction: int):
        return Hexagon.hex_add(cube, self.oRanDuDirections()[direction])

    def oRanDuRing(self, center: Hex, radius: int) -> list[Hex]:
        if radius <= 0:
            raise ValueError(
                "Invalid radius. The radius around the hex center must be greater than 0 rings."
            )
        results: list[Hex] = []
        hex: Hex = Hexagon.hex_add(
            center, Hexagon.hex_scale(self.oRanDuDirections()[4], radius)
        )
        for i in range(6):
            for j in range(radius):
                results.append(hex)
                hex = self.oRanDuNeighbor(hex, i)
        return results

    def oRanDuSpiral(self, o_ran_du_center: Hex, radius: int) -> list[Hex]:
        result: list[Hex] = [o_ran_du_center]
        for k in range(1, radius + 1):
            result.extend(self.oRanDuRing(o_ran_du_center, k))
        return result

    def oRanCuDirections(self) -> list[Hex]:
        q: int = (
            2 * self.oRanCuSpiralRadiusOfODus
            + 3
            * self.oRanCuSpiralRadiusOfODus
            * self.oRanDuSpiralRadiusOfTowers
            + self.oRanDuSpiralRadiusOfTowers
            + 1
        )
        r: int = (
            self.oRanDuSpiralRadiusOfTowers - self.oRanCuSpiralRadiusOfODus
        )
        s: int = -q - r
        return [
            Hex(+q, +r, +s),
            Hex(-s, -q, -r),
            Hex(+r, +s, +q),
            Hex(-q, -r, -s),
            Hex(+s, +q, +r),
            Hex(-r, -s, -q),
        ]

    def oRanCuNeighbor(self, cube: Hex, direction: int) -> list[Hex]:
        return Hexagon.hex_add(cube, self.oRanCuDirections()[direction])

    def oRanCuRing(self, center: Hex, radius: int):
        if not (radius > 0):
            raise ValueError(
                "Invalid radius. The radius around the hex center must be greater than 0 rings."
            )

        results: list[Hex] = []
        hex: Hex = Hexagon.hex_add(
            center, Hexagon.hex_scale(self.oRanCuDirections()[4], radius)
        )
        for i in range(6):
            for j in range(radius):
                results.append(hex)
                hex = self.oRanCuNeighbor(hex, i)
        return results

    def oRanCuSpiral(self, center: Hex, radius: int) -> list[Hex]:
        result: list[Hex] = [center]
        for k in range(1, radius + 1):
            result += self.oRanCuRing(center, k)
        return result

    def oRanNearRtRicDirections(self) -> list[Hex]:
        q0: int = (
            2 * self.oRanCuSpiralRadiusOfODus
            + 3
            * self.oRanCuSpiralRadiusOfODus
            * self.oRanDuSpiralRadiusOfTowers
            + self.oRanDuSpiralRadiusOfTowers
            + 1
        )
        r0: int = (
            self.oRanDuSpiralRadiusOfTowers - self.oRanCuSpiralRadiusOfODus
        )

        q: int = 3 * q0 - self.oRanNearRtRicSpiralRadiusOfOCus
        r: int = -r0 - self.oRanNearRtRicSpiralRadiusOfOCus

        profile_id: str = self.id[0 : len(self.id) - 1]
        if profile_id in {"111", "112", "113", "114"}:
            q: int = 21 + 14 * (self.oRanNearRtRicSpiralRadiusOfOCus - 1)
            r: int = -7 * self.oRanNearRtRicSpiralRadiusOfOCus
        elif profile_id in {"121", "122", "123", "124"}:
            q: int = 25 + 13 * (self.oRanNearRtRicSpiralRadiusOfOCus - 1)
            r: int = 9 + 10 * (self.oRanNearRtRicSpiralRadiusOfOCus - 1)
        elif profile_id in {"131", "132"}:
            q: int = 49 + 30 * (self.oRanNearRtRicSpiralRadiusOfOCus - 1)
            r: int = -21 - 34 * (self.oRanNearRtRicSpiralRadiusOfOCus - 1)
        elif profile_id == "133":
            q: int = 74
            r: int = 37
        elif profile_id == "134":
            q: int = 93
            r: int = 50
        elif profile_id in {"211", "212", "213", "214"}:
            q: int = 34 + 23 * (self.oRanNearRtRicSpiralRadiusOfOCus - 1)
            r: int = -10 * self.oRanNearRtRicSpiralRadiusOfOCus - 1
        elif profile_id in {"221", "222", "223", "224"}:
            q: int = 57 + 38 * (self.oRanNearRtRicSpiralRadiusOfOCus - 1)
            r: int = -19 * self.oRanNearRtRicSpiralRadiusOfOCus
        elif profile_id in {"231", "232", "233", "234"}:
            q: int = 80 + 53 * (self.oRanNearRtRicSpiralRadiusOfOCus - 1)
            r: int = -28 * self.oRanNearRtRicSpiralRadiusOfOCus - 1
        elif profile_id in {"241", "242", "243", "244"}:
            q: int = 103 + 68 * (self.oRanNearRtRicSpiralRadiusOfOCus - 1)
            r: int = -39 * self.oRanNearRtRicSpiralRadiusOfOCus + 2 * (
                self.oRanNearRtRicSpiralRadiusOfOCus - 1
            )
        elif profile_id in {"311", "312", "313", "314"}:
            q: int = 47 + 32 * (self.oRanNearRtRicSpiralRadiusOfOCus - 1)
            r: int = -11 - 13 * (self.oRanNearRtRicSpiralRadiusOfOCus - 1)
        elif profile_id in {"321", "322", "323", "324"}:
            q: int = 79 + 53 * (self.oRanNearRtRicSpiralRadiusOfOCus - 1)
            r: int = -24 - 25 * (self.oRanNearRtRicSpiralRadiusOfOCus - 1)
        elif profile_id in {"331", "332", "333", "334"}:
            q: int = 111 + 75 * (self.oRanNearRtRicSpiralRadiusOfOCus - 1)
            r: int = -37 - 37 * (self.oRanNearRtRicSpiralRadiusOfOCus - 1)
        else:
            # Handle the default case or raise a warning
            pass

        s: int = -q - r
        return [
            Hex(q, r, s),
            Hex(-s, -q, -r),
            Hex(r, s, q),
            Hex(-q, -r, -s),
            Hex(s, q, r),
            Hex(-r, -s, -q),
        ]

    def oRanNearRtRicNeighbor(self, cube: Hex, direction: int):
        return Hexagon.hex_add(cube, self.oRanNearRtRicDirections()[direction])

    def oRanNearRtRicRing(self, center: Hex, radius: int) -> list[Hex]:
        if not (radius > 0):
            raise ValueError(
                "Invalid radius. The radius around the hex center must be greater than 0 rings."
            )

        results: list[Hex] = []
        hex: Hex = Hexagon.hex_add(
            center,
            Hexagon.hex_scale(self.oRanNearRtRicDirections()[4], radius),
        )
        for i in range(6):
            for j in range(radius):
                results.append(hex)
                hex = self.oRanNearRtRicNeighbor(hex, i)
        return results

    def oRanNearRtRicSpiral(self, center: Hex, radius: int) -> list[Hex]:
        result: list[Hex] = [center]
        for k in range(1, radius + 1):
            result += self.oRanNearRtRicRing(center, k)
        return result
