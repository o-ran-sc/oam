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

from __future__ import division
from __future__ import print_function
import collections
import math
from typing import NamedTuple

from network_generation.model.python.point import Point
from network_generation.model.python.geo_location import GeoLocation


class Hex:
    def __init__(self, q: int, r: int, s: int):
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


def hex_rotate_left(a) -> Hex:
    return Hex(-a.s, -a.q, -a.r)


def hex_rotate_right(a) -> Hex:
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


def hex_length(hex: Hex) -> int:
    return (abs(hex.q) + abs(hex.r) + abs(hex.s)) // 2


def hex_distance(a: Hex, b: Hex) -> int:
    return hex_length(hex_subtract(a, b))


def hex_round(hex: Hex) -> Hex:
    qi = int(round(hex.q))
    ri = int(round(hex.r))
    si = int(round(hex.s))
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


def hex_lerp(a: Hex, b: Hex, t: int) -> Hex:  # linearly interpolation
    return Hex(
        a.q * (1.0 - t) + b.q * t, a.r * (1.0 - t) + b.r * t, a.s * (1.0 - t) + b.s * t
    )


def hex_linedraw(a: Hex, b: Hex) -> list[hex]:
    N = hex_distance(a, b)
    a_nudge = Hex(a.q + 1e-06, a.r + 1e-06, a.s - 2e-06)
    b_nudge = Hex(b.q + 1e-06, b.r + 1e-06, b.s - 2e-06)
    results: list[hex] = []
    step = 1.0 / max(N, 1)
    for i in range(0, N + 1):
        results.append(hex_round(hex_lerp(a_nudge, b_nudge, step * i)))
    return results


OffsetCoord = collections.namedtuple("OffsetCoord", ["col", "row"])

EVEN: int = 1
ODD: int = -1


def qoffset_from_cube(offset: int, hex: Hex) -> OffsetCoord:
    col = hex.q
    row = hex.r + (hex.q + offset * (hex.q & 1)) // 2
    if offset != EVEN and offset != ODD:
        raise ValueError("offset must be EVEN (+1) or ODD (-1)")
    return OffsetCoord(col, row)


def qoffset_to_cube(offset: int, hex: Hex) -> Hex:
    q = hex.col
    r = hex.row - (hex.col + offset * (hex.col & 1)) // 2
    s = -q - r
    if offset != EVEN and offset != ODD:
        raise ValueError("offset must be EVEN (+1) or ODD (-1)")
    return Hex(q, r, s)


def roffset_from_cube(offset: int, hex: Hex) -> OffsetCoord:
    col = hex.q + (hex.r + offset * (hex.r & 1)) // 2
    row = hex.r
    if offset != EVEN and offset != ODD:
        raise ValueError("offset must be EVEN (+1) or ODD (-1)")
    return OffsetCoord(col, row)


def roffset_to_cube(offset: int, hex: Hex) -> Hex:
    q = hex.col - (hex.row + offset * (hex.row & 1)) // 2
    r = hex.row
    s = -q - r
    if offset != EVEN and offset != ODD:
        raise ValueError("offset must be EVEN (+1) or ODD (-1)")
    return Hex(q, r, s)


DoubledCoord = collections.namedtuple("DoubledCoord", ["col", "row"])


def qdoubled_from_cube(hex: Hex):
    col = hex.q
    row = 2 * hex.r + hex.q
    return DoubledCoord(col, row)


def qdoubled_to_cube(hex: Hex) -> Hex:
    q = hex.col
    r = (hex.row - hex.col) // 2
    s = -q - r
    return Hex(q, r, s)


def rdoubled_from_cube(hex: Hex) -> DoubledCoord:
    col = 2 * hex.q + hex.r
    row = hex.r
    return DoubledCoord(col, row)


def rdoubled_to_cube(hex: Hex):
    q = (hex.col - hex.row) // 2
    r = hex.row
    s = -q - r
    return Hex(q, r, s)


Orientation = collections.namedtuple(
    "Orientation", ["f0", "f1", "f2", "f3", "b0", "b1", "b2", "b3", "start_angle"]
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
    return GeoLocation(reference).point_to_geo_location(hexPoint)


# Tests


def complain(name):
    print("FAIL {0}".format(name))


def equal_hex(name, a, b):
    if not (a.q == b.q and a.s == b.s and a.r == b.r):
        complain(name)


def equal_offsetcoord(name, a, b):
    if not (a.col == b.col and a.row == b.row):
        complain(name)


def equal_doubledcoord(name, a, b):
    if not (a.col == b.col and a.row == b.row):
        complain(name)


def equal_int(name, a, b):
    if not (a == b):
        complain(name)


def equal_hex_array(name, a, b):
    equal_int(name, len(a), len(b))
    for i in range(0, len(a)):
        equal_hex(name, a[i], b[i])


def test_hex_arithmetic():
    equal_hex("hex_add", Hex(4, -10, 6), hex_add(Hex(1, -3, 2), Hex(3, -7, 4)))
    equal_hex(
        "hex_subtract", Hex(-2, 4, -2), hex_subtract(Hex(1, -3, 2), Hex(3, -7, 4))
    )


def test_hex_direction():
    equal_hex("hex_direction", Hex(0, -1, 1), hex_direction(2))


def test_hex_neighbor():
    equal_hex("hex_neighbor", Hex(1, -3, 2), hex_neighbor(Hex(1, -2, 1), 2))


def test_hex_diagonal():
    equal_hex("hex_diagonal", Hex(-1, -1, 2), hex_diagonal_neighbor(Hex(1, -2, 1), 3))


def test_hex_distance():
    equal_int("hex_distance", 7, hex_distance(Hex(3, -7, 4), Hex(0, 0, 0)))


def test_hex_rotate_right():
    equal_hex("hex_rotate_right", hex_rotate_right(Hex(1, -3, 2)), Hex(3, -2, -1))


def test_hex_rotate_left():
    equal_hex("hex_rotate_left", hex_rotate_left(Hex(1, -3, 2)), Hex(-2, -1, 3))


def test_hex_round():
    a = Hex(0.0, 0.0, 0.0)
    b = Hex(1.0, -1.0, 0.0)
    c = Hex(0.0, -1.0, 1.0)
    equal_hex(
        "hex_round 1",
        Hex(5, -10, 5),
        hex_round(hex_lerp(Hex(0.0, 0.0, 0.0), Hex(10.0, -20.0, 10.0), 0.5)),
    )
    equal_hex("hex_round 2", hex_round(a), hex_round(hex_lerp(a, b, 0.499)))
    equal_hex("hex_round 3", hex_round(b), hex_round(hex_lerp(a, b, 0.501)))
    equal_hex(
        "hex_round 4",
        hex_round(a),
        hex_round(
            Hex(
                a.q * 0.4 + b.q * 0.3 + c.q * 0.3,
                a.r * 0.4 + b.r * 0.3 + c.r * 0.3,
                a.s * 0.4 + b.s * 0.3 + c.s * 0.3,
            )
        ),
    )
    equal_hex(
        "hex_round 5",
        hex_round(c),
        hex_round(
            Hex(
                a.q * 0.3 + b.q * 0.3 + c.q * 0.4,
                a.r * 0.3 + b.r * 0.3 + c.r * 0.4,
                a.s * 0.3 + b.s * 0.3 + c.s * 0.4,
            )
        ),
    )


def test_hex_linedraw():
    equal_hex_array(
        "hex_linedraw",
        [
            Hex(0, 0, 0),
            Hex(0, -1, 1),
            Hex(0, -2, 2),
            Hex(1, -3, 2),
            Hex(1, -4, 3),
            Hex(1, -5, 4),
        ],
        hex_linedraw(Hex(0, 0, 0), Hex(1, -5, 4)),
    )


def test_layout():
    h = Hex(3, 4, -7)
    flat = Layout(layout_flat, Point(10.0, 15.0), Point(35.0, 71.0))
    equal_hex("layout", h, hex_round(pixel_to_hex(flat, hex_to_pixel(flat, h))))
    pointy = Layout(layout_pointy, Point(10.0, 15.0), Point(35.0, 71.0))
    equal_hex("layout", h, hex_round(pixel_to_hex(pointy, hex_to_pixel(pointy, h))))


def test_offset_roundtrip():
    a = Hex(3, 4, -7)
    b = OffsetCoord(1, -3)
    equal_hex(
        "conversion_roundtrip even-q",
        a,
        qoffset_to_cube(EVEN, qoffset_from_cube(EVEN, a)),
    )
    equal_offsetcoord(
        "conversion_roundtrip even-q",
        b,
        qoffset_from_cube(EVEN, qoffset_to_cube(EVEN, b)),
    )
    equal_hex(
        "conversion_roundtrip odd-q", a, qoffset_to_cube(ODD, qoffset_from_cube(ODD, a))
    )
    equal_offsetcoord(
        "conversion_roundtrip odd-q", b, qoffset_from_cube(ODD, qoffset_to_cube(ODD, b))
    )
    equal_hex(
        "conversion_roundtrip even-r",
        a,
        roffset_to_cube(EVEN, roffset_from_cube(EVEN, a)),
    )
    equal_offsetcoord(
        "conversion_roundtrip even-r",
        b,
        roffset_from_cube(EVEN, roffset_to_cube(EVEN, b)),
    )
    equal_hex(
        "conversion_roundtrip odd-r", a, roffset_to_cube(ODD, roffset_from_cube(ODD, a))
    )
    equal_offsetcoord(
        "conversion_roundtrip odd-r", b, roffset_from_cube(ODD, roffset_to_cube(ODD, b))
    )


def test_offset_from_cube():
    equal_offsetcoord(
        "offset_from_cube even-q",
        OffsetCoord(1, 3),
        qoffset_from_cube(EVEN, Hex(1, 2, -3)),
    )
    equal_offsetcoord(
        "offset_from_cube odd-q",
        OffsetCoord(1, 2),
        qoffset_from_cube(ODD, Hex(1, 2, -3)),
    )


def test_offset_to_cube():
    equal_hex(
        "offset_to_cube even-", Hex(1, 2, -3), qoffset_to_cube(EVEN, OffsetCoord(1, 3))
    )
    equal_hex(
        "offset_to_cube odd-q", Hex(1, 2, -3), qoffset_to_cube(ODD, OffsetCoord(1, 2))
    )


def test_doubled_roundtrip():
    a = Hex(3, 4, -7)
    b = DoubledCoord(1, -3)
    equal_hex(
        "conversion_roundtrip doubled-q", a, qdoubled_to_cube(qdoubled_from_cube(a))
    )
    equal_doubledcoord(
        "conversion_roundtrip doubled-q", b, qdoubled_from_cube(qdoubled_to_cube(b))
    )
    equal_hex(
        "conversion_roundtrip doubled-r", a, rdoubled_to_cube(rdoubled_from_cube(a))
    )
    equal_doubledcoord(
        "conversion_roundtrip doubled-r", b, rdoubled_from_cube(rdoubled_to_cube(b))
    )


def test_doubled_from_cube():
    equal_doubledcoord(
        "doubled_from_cube doubled-q",
        DoubledCoord(1, 5),
        qdoubled_from_cube(Hex(1, 2, -3)),
    )
    equal_doubledcoord(
        "doubled_from_cube doubled-r",
        DoubledCoord(4, 2),
        rdoubled_from_cube(Hex(1, 2, -3)),
    )


def test_doubled_to_cube():
    equal_hex(
        "doubled_to_cube doubled-q", Hex(1, 2, -3), qdoubled_to_cube(DoubledCoord(1, 5))
    )
    equal_hex(
        "doubled_to_cube doubled-r", Hex(1, 2, -3), rdoubled_to_cube(DoubledCoord(4, 2))
    )


def test_all():
    test_hex_arithmetic()
    test_hex_direction()
    test_hex_neighbor()
    test_hex_diagonal()
    test_hex_distance()
    test_hex_rotate_right()
    test_hex_rotate_left()
    test_hex_round()
    test_hex_linedraw()
    test_layout()
    test_offset_roundtrip()
    test_offset_from_cube()
    test_offset_to_cube()
    test_doubled_roundtrip()
    test_doubled_from_cube()
    test_doubled_to_cube()
    print("test finished")


if __name__ == "__main__":
    test_all()
