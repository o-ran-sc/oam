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

# !/usr/bin/python

from __future__ import division, print_function

import collections
import math
from typing import NamedTuple

from network_generation.model.python.geo_location import GeoLocation
from network_generation.model.python.point import Point


class Hex:
    def __init__(self, q: float, r: float, s: float) -> None:
        if round(q + r + s) != 0:
            raise ValueError("The sum of q, r, and s must be 0.")
        self.q = q
        self.r = r
        self.s = s

    def __str__(self) -> str:
        return f"q: {self.q}, r: {self.r}, s: {self.s}"


def hex_add(a: Hex, b: Hex) -> Hex:
    return Hex(a.q + b.q, a.r + b.r, a.s + b.s)


def hex_subtract(a: Hex, b: Hex) -> Hex:
    return Hex(a.q - b.q, a.r - b.r, a.s - b.s)


def hex_scale(a: Hex, k: int) -> Hex:
    return Hex(a.q * k, a.r * k, a.s * k)


def hex_rotate_left(a: Hex) -> Hex:
    return Hex(-a.s, -a.q, -a.r)


def hex_rotate_right(a: Hex) -> Hex:
    return Hex(-a.r, -a.s, -a.q)


hex_directions: list[Hex] = [
    Hex(1, 0, -1),
    Hex(1, -1, 0),
    Hex(0, -1, 1),
    Hex(-1, 0, 1),
    Hex(-1, 1, 0),
    Hex(0, 1, -1),
]


def hex_direction(direction: int) -> Hex:
    return hex_directions[direction]


def hex_neighbor(hex: Hex, direction: int) -> Hex:
    return hex_add(hex, hex_direction(direction))


hex_diagonals: list[Hex] = [
    Hex(2, -1, -1),
    Hex(1, -2, 1),
    Hex(-1, -1, 2),
    Hex(-2, 1, 1),
    Hex(-1, 2, -1),
    Hex(1, 1, -2),
]


def hex_diagonal_neighbor(hex: Hex, direction: int) -> Hex:
    return hex_add(hex, hex_diagonals[direction])


def hex_length(hex: Hex) -> float:
    return (abs(hex.q) + abs(hex.r) + abs(hex.s)) // 2


def hex_distance(a: Hex, b: Hex) -> float:
    return hex_length(hex_subtract(a, b))


def hex_round(hex: Hex) -> Hex:
    qi = round(hex.q)
    ri = round(hex.r)
    si = round(hex.s)
    q_diff = abs(qi - hex.q)
    r_diff = abs(ri - hex.r)
    s_diff = abs(si - hex.s)
    if q_diff > r_diff and q_diff > s_diff:
        qi = -ri - si
    else:
        if r_diff > s_diff:
            ri = -qi - si
        else:
            si = -qi - ri
    return Hex(qi, ri, si)


def hex_lerp(a: Hex, b: Hex, t: float) -> Hex:  # linearly interpolation
    return Hex(
        a.q * (1 - t) + b.q * t,
        a.r * (1 - t) + b.r * t,
        a.s * (1 - t) + b.s * t,
    )


def hex_linedraw(a: Hex, b: Hex) -> list[Hex]:
    N: float = hex_distance(a, b)
    a_nudge: Hex = Hex(a.q + 1e-06, a.r + 1e-06, a.s - 2e-06)
    b_nudge: Hex = Hex(b.q + 1e-06, b.r + 1e-06, b.s - 2e-06)
    results: list[Hex] = []
    step: float = 1 / max(N, 1)
    for i in range(0, int(N) + 1):
        results.append(hex_round(hex_lerp(a_nudge, b_nudge, step * i)))
    return results


OffsetCoord = collections.namedtuple("OffsetCoord", ["col", "row"])

EVEN: int = 1
ODD: int = -1


def qoffset_from_cube(offset: float, hex: Hex) -> OffsetCoord:
    col = hex.q
    row = hex.r + (hex.q + offset * (int(hex.q) & 1)) // 2
    if offset != EVEN and offset != ODD:
        raise ValueError("offset must be EVEN (+1) or ODD (-1)")
    return OffsetCoord(col, row)


def qoffset_to_cube(offset: int, offsetCoord: OffsetCoord) -> Hex:
    q = offsetCoord.col
    r = (
        offsetCoord.row
        - (offsetCoord.col + offset * (offsetCoord.col & 1)) // 2
    )
    s = -q - r
    if offset != EVEN and offset != ODD:
        raise ValueError("offset must be EVEN (+1) or ODD (-1)")
    return Hex(q, r, s)


def roffset_from_cube(offset: float, hex: Hex) -> OffsetCoord:
    col = hex.q + (hex.r + offset * (int(hex.r) & 1)) // 2
    row = hex.r
    if offset != EVEN and offset != ODD:
        raise ValueError("offset must be EVEN (+1) or ODD (-1)")
    return OffsetCoord(col, row)


def roffset_to_cube(offset: float, hex: OffsetCoord) -> Hex:
    q = hex.col - (hex.row + offset * (int(hex.row) & 1)) // 2
    r = hex.row
    s = -q - r
    if offset != EVEN and offset != ODD:
        raise ValueError("offset must be EVEN (+1) or ODD (-1)")
    return Hex(q, r, s)


DoubledCoord = collections.namedtuple("DoubledCoord", ["col", "row"])


def qdoubled_from_cube(hex: Hex) -> DoubledCoord:
    col = hex.q
    row = 2 * hex.r + hex.q
    return DoubledCoord(col, row)


def qdoubled_to_cube(doubledCoord: DoubledCoord) -> Hex:
    q = doubledCoord.col
    r = (doubledCoord.row - doubledCoord.col) // 2
    s = -q - r
    return Hex(q, r, s)


def rdoubled_from_cube(hex: Hex) -> DoubledCoord:
    col = 2 * hex.q + hex.r
    row = hex.r
    return DoubledCoord(col, row)


def rdoubled_to_cube(doubledCoord: DoubledCoord) -> Hex:
    q = (doubledCoord.col - doubledCoord.row) // 2
    r = doubledCoord.row
    s = -q - r
    return Hex(q, r, s)


Orientation = collections.namedtuple(
    "Orientation",
    ["f0", "f1", "f2", "f3", "b0", "b1", "b2", "b3", "start_angle"],
)


# Layout = collections.namedtuple("Layout", ["orientation", "size", "origin"])
class Layout(NamedTuple):
    orientation: Orientation
    size: Point
    origin: Point


layout_pointy: Orientation = Orientation(
    math.sqrt(3.0),
    math.sqrt(3.0) / 2.0,
    0.0,
    3.0 / 2.0,
    math.sqrt(3.0) / 3.0,
    -1.0 / 3.0,
    0.0,
    2.0 / 3.0,
    0.5,
)
layout_flat: Orientation = Orientation(
    3.0 / 2.0,
    0.0,
    math.sqrt(3.0) / 2.0,
    math.sqrt(3.0),
    2.0 / 3.0,
    0.0,
    -1.0 / 3.0,
    math.sqrt(3.0) / 3.0,
    0.0,
)


def hex_to_pixel(layout: Layout, hex: Hex) -> Point:
    M = layout.orientation
    size = layout.size
    origin = layout.origin
    x = (M.f0 * hex.q + M.f1 * hex.r) * size.x
    y = (M.f2 * hex.q + M.f3 * hex.r) * size.y
    return Point(x + origin.x, y + origin.y)


def pixel_to_hex(layout: Layout, p: Point) -> Hex:
    M = layout.orientation
    size = layout.size
    origin = layout.origin
    pt = Point((p.x - origin.x) / size.x, (p.y - origin.y) / size.y)
    q = M.b0 * pt.x + M.b1 * pt.y
    r = M.b2 * pt.x + M.b3 * pt.y
    return Hex(q, r, -q - r)


def hex_corner_offset(layout: Layout, corner: int) -> Point:
    M = layout.orientation
    size = layout.size
    angle = 2.0 * math.pi * (M.start_angle - corner) / 6.0
    return Point(size.x * math.cos(angle), size.y * math.sin(angle))


def polygon_corners(layout: Layout, hex: Hex) -> list[Point]:
    corners: list[Point] = []
    center = hex_to_pixel(layout, hex)
    for i in range(0, 6):
        offset = hex_corner_offset(layout, i)
        corners.append(Point(center.x + offset.x, center.y + offset.y))
    return corners


def hex_to_geo_location(
    layout: Layout, hex: Hex, reference: GeoLocation
) -> GeoLocation:
    hexPoint: Point = hex_to_pixel(layout, hex)
    return reference.point_to_geo_location(hexPoint)
