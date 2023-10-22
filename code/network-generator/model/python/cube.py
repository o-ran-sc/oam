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
#
# inspired by http://www.redblobgames.com/grids/hexagons/

#!/usr/bin/python
from model.python.hexagon import Hex


class Cube:
    @staticmethod
    def direction_vectors() -> list[Hex]:
        q, r, s = 1, 0, -1
        return [
            Hex(q, r, s),
            Hex(-s, -q, -r),
            Hex(r, s, q),
            Hex(-q, -r, -s),
            Hex(s, q, r),
            Hex(-r, -s, -q),
        ]

    @staticmethod
    def direction(direction: int) -> Hex:
        if direction < 0 or direction > 5:
            raise ValueError(
                "Invalid direction. The direction value must be in the range of [0..5]."
            )
        return Cube.direction_vectors()[direction]

    @staticmethod
    def add(hex: Hex, vec: Hex) -> Hex:
        return Hex(hex.q + vec.q, hex.r + vec.r, hex.s + vec.s)

    @staticmethod
    def neighbor(cube: Hex, direction: int) -> Hex:
        return Cube.add(cube, Cube.direction(direction))

    @staticmethod
    def scale(hex: Hex, factor: int) -> Hex:
        return Hex(hex.q * factor, hex.r * factor, hex.s * factor)

    @staticmethod
    def ring(center: Hex, radius: int) -> list[Hex]:
        if not (radius > 0):
            raise ValueError(
                "Invalid radius. The radius around the hex center must be greater than 0 rings."
            )
        results: list[Hex] = []
        hex: Hex = Cube.add(center, Cube.scale(Cube.direction(4), radius))
        for i in range(6):
            for j in range(radius):
                results.append(hex)
                hex = Cube.neighbor(hex, i)
        return results

    @staticmethod
    def spiral(center: Hex, radius: int) -> list[Hex]:
        result: list[Hex] = [center]
        for k in range(1, radius + 1):
            result.extend(Cube.ring(center, k))
        return result
