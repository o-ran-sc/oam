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
from typing import List
from model.python.hexagon import Hex

class SpiralRadiusProfile:
    def __init__(self, data=None):
        self._oRanSmoSpiralRadiusOfNearRtRics = data.get("oRanSmoSpiralRadiusOfNearRtRics", 1) if data else 1
        self._oRanNearRtRicSpiralRadiusOfOCus = data.get("oRanNearRtRicSpiralRadiusOfOCus", 1) if data else 1
        self._oRanCuSpiralRadiusOfODus = data.get("oRanCuSpiralRadiusOfODus", 1) if data else 1
        self._oRanDuSpiralRadiusOfTowers = data.get("oRanDuSpiralRadiusOfTowers", 1) if data else 1

    @property
    def id(self):
        return f"{self._oRanDuSpiralRadiusOfTowers}{self._oRanCuSpiralRadiusOfODus}{self._oRanNearRtRicSpiralRadiusOfOCus}{self._oRanSmoSpiralRadiusOfNearRtRics}"

    @property
    def count(self):
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
    def oRanSmoSpiralRadiusOfNearRtRics(self):
        return self._oRanSmoSpiralRadiusOfNearRtRics

    @oRanSmoSpiralRadiusOfNearRtRics.setter
    def oRanSmoSpiralRadiusOfNearRtRics(self, value):
        self._oRanSmoSpiralRadiusOfNearRtRics = value

    @property
    def oRanNearRtRicSpiralRadiusOfOCus(self):
        return self._oRanNearRtRicSpiralRadiusOfOCus

    @oRanNearRtRicSpiralRadiusOfOCus.setter
    def oRanNearRtRicSpiralRadiusOfOCus(self, value):
        self._oRanNearRtRicSpiralRadiusOfOCus = value

    @property
    def oRanCuSpiralRadiusOfODus(self):
        return self._oRanCuSpiralRadiusOfODus

    @oRanCuSpiralRadiusOfODus.setter
    def oRanCuSpiralRadiusOfODus(self, value):
        self._oRanCuSpiralRadiusOfODus = value

    @property
    def oRanDuSpiralRadiusOfTowers(self):
        return self._oRanDuSpiralRadiusOfTowers

    @oRanDuSpiralRadiusOfTowers.setter
    def oRanDuSpiralRadiusOfTowers(self, value):
        self._oRanDuSpiralRadiusOfTowers = value

    @property
    def sectors(self):
        return self._sectors

    @sectors.setter
    def sectors(self, value):
        self._sectors = value

    @property
    def nrDuCellsPerSector(self):
        return self._nrDuCellsPerSector

    @nrDuCellsPerSector.setter
    def nrDuCellsPerSector(self, value):
        self._nrDuCellsPerSector = value

    def oRanDuDirections(self):
        q = 2 * self._oRanDuSpiralRadiusOfTowers + 1
        r = - self._oRanDuSpiralRadiusOfTowers - 1
        s = -q - r
        return [
            Hex(q, r, s), Hex(-s, -q, -r), Hex(r, s, q),
            Hex(-q, -r, -s), Hex(s, q, r), Hex(-r, -s, -q)
        ]

    def oRanDuNeighbor(self, cube, direction):
        return Hex.add(cube, self.oRanDuDirections[direction])

    def oRanDuRing(self, center, radius):
        if radius <= 0:
            raise ValueError('Invalid radius. The radius around the hex center must be greater than 0 rings.')
        results = []
        hex = Hex.add(center, Hex.scale(self.oRanDuDirections[4], radius))
        for i in range(6):
            for j in range(radius):
                results.append(hex)
                hex = self.oRanDuNeighbor(hex, i)
        return results

    def oRanDuSpiral(self, center, radius):
        result = [center]
        for k in range(1, radius + 1):
            result.extend(self.oRanDuRing(center, k))
        return result

    def oRanCuDirections(self):
        q0 = 2 * self._oRanCuSpiralRadiusOfODus + 3 * self._oRanCuSpiralRadiusOfODus * self._oRanDuSpiralRadiusOfTowers + self._oRanDuSpiralRadiusOfTowers + 1
        r0 = self._oRanDuSpiralRadiusOfTowers - self._oRanCuSpiralRadiusOfODus
        q = 3 * q0 - self._oRanNearRtRicSpiralRadiusOfOCus
        r = -r0 - self._oRanNearRtRicSpiralRadiusOfOCus
        switch_id = self.id[2:-1]
        if switch_id in ("111", "112", "113", "114"):
            q = 21 + 14
