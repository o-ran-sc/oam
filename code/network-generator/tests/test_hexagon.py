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

from network_generation.model.python.hexagon import (
    DoubledCoord,
    Hex,
    Layout,
    OffsetCoord,
)
import network_generation.model.python.hexagon as Hexagon
from network_generation.model.python.point import Point

# Tests


def complain(name: str) -> None:
    print("FAIL {0}".format(name))


def equal_hex(name: str, a: Hex, b: Hex) -> None:
    if not (a.q == b.q and a.s == b.s and a.r == b.r):
        complain(name)


def equal_offsetcoord(name: str, a: OffsetCoord, b: OffsetCoord) -> None:
    if not (a.col == b.col and a.row == b.row):
        complain(name)


def equal_doubledcoord(name: str, a: DoubledCoord, b: DoubledCoord) -> None:
    if not (a.col == b.col and a.row == b.row):
        complain(name)


def equal_int(name: str, a: int, b: int) -> None:
    if not (a == b):
        complain(name)


def equal_hex_array(name: str, a: list[Hex], b: list[Hex]) -> None:
    equal_int(name, len(a), len(b))
    for i in range(0, len(a)):
        equal_hex(name, a[i], b[i])


def test_hex_arithmetic() -> None:
    equal_hex(
        "hex_add",
        Hex(4, -10, 6),
        Hexagon.hex_add(Hex(1, -3, 2), Hex(3, -7, 4)),
    )
    equal_hex(
        "hex_subtract",
        Hex(-2, 4, -2),
        Hexagon.hex_subtract(Hex(1, -3, 2), Hex(3, -7, 4)),
    )


def test_hex_direction() -> None:
    equal_hex("hex_direction", Hex(0, -1, 1), Hexagon.hex_direction(2))


def test_hex_neighbor() -> None:
    equal_hex(
        "hex_neighbor", Hex(1, -3, 2), Hexagon.hex_neighbor(Hex(1, -2, 1), 2)
    )


def test_hex_diagonal() -> None:
    equal_hex(
        "hex_diagonal",
        Hex(-1, -1, 2),
        Hexagon.hex_diagonal_neighbor(Hex(1, -2, 1), 3),
    )


def test_hex_distance() -> None:
    equal_int(
        "hex_distance",
        7,
        int(Hexagon.hex_distance(Hex(3, -7, 4), Hex(0, 0, 0))),
    )


def test_hex_rotate_right() -> None:
    equal_hex(
        "hex_rotate_right",
        Hexagon.hex_rotate_right(Hex(1, -3, 2)),
        Hex(3, -2, -1),
    )


def test_hex_rotate_left() -> None:
    equal_hex(
        "hex_rotate_left",
        Hexagon.hex_rotate_left(Hex(1, -3, 2)),
        Hex(-2, -1, 3),
    )


def test_hex_round() -> None:
    a = Hex(0, 0, 0)
    b = Hex(1, -1, 0)
    c = Hex(0, -1, 1)
    equal_hex(
        "hex_round 1",
        Hex(5, -10, 5),
        Hexagon.hex_round(
            Hexagon.hex_lerp(Hex(0, 0, 0), Hex(10, -20, 10), 0.5)
        ),
    )
    equal_hex(
        "hex_round 2",
        Hexagon.hex_round(a),
        Hexagon.hex_round(Hexagon.hex_lerp(a, b, 0.499)),
    )
    equal_hex(
        "hex_round 3",
        Hexagon.hex_round(b),
        Hexagon.hex_round(Hexagon.hex_lerp(a, b, 0.501)),
    )
    equal_hex(
        "hex_round 4",
        Hexagon.hex_round(a),
        Hexagon.hex_round(
            Hex(
                a.q * 0.4 + b.q * 0.3 + c.q * 0.3,
                a.r * 0.4 + b.r * 0.3 + c.r * 0.3,
                a.s * 0.4 + b.s * 0.3 + c.s * 0.3,
            )
        ),
    )
    equal_hex(
        "hex_round 5",
        Hexagon.hex_round(c),
        Hexagon.hex_round(
            Hex(
                a.q * 0.3 + b.q * 0.3 + c.q * 0.4,
                a.r * 0.3 + b.r * 0.3 + c.r * 0.4,
                a.s * 0.3 + b.s * 0.3 + c.s * 0.4,
            )
        ),
    )


def test_hex_linedraw() -> None:
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
        Hexagon.hex_linedraw(Hex(0, 0, 0), Hex(1, -5, 4)),
    )


def test_layout() -> None:
    h = Hex(3, 4, -7)
    flat = Layout(Hexagon.layout_flat, Point(10.0, 15.0), Point(35.0, 71.0))
    equal_hex(
        "layout",
        h,
        Hexagon.hex_round(
            Hexagon.pixel_to_hex(flat, Hexagon.hex_to_pixel(flat, h))
        ),
    )
    pointy = Layout(
        Hexagon.layout_pointy, Point(10.0, 15.0), Point(35.0, 71.0)
    )
    equal_hex(
        "layout",
        h,
        Hexagon.hex_round(
            Hexagon.pixel_to_hex(pointy, Hexagon.hex_to_pixel(pointy, h))
        ),
    )


def test_offset_roundtrip() -> None:
    a = Hex(3, 4, -7)
    b = OffsetCoord(1, -3)
    equal_hex(
        "conversion_roundtrip even-q",
        a,
        Hexagon.qoffset_to_cube(
            Hexagon.EVEN,
            Hexagon.qoffset_from_cube(Hexagon.EVEN, a),
        ),
    )
    equal_offsetcoord(
        "conversion_roundtrip even-q",
        b,
        Hexagon.qoffset_from_cube(
            Hexagon.EVEN,
            Hexagon.qoffset_to_cube(Hexagon.EVEN, b),
        ),
    )
    equal_hex(
        "conversion_roundtrip odd-q",
        a,
        Hexagon.qoffset_to_cube(
            Hexagon.ODD,
            Hexagon.qoffset_from_cube(Hexagon.ODD, a),
        ),
    )
    equal_offsetcoord(
        "conversion_roundtrip odd-q",
        b,
        Hexagon.qoffset_from_cube(
            Hexagon.ODD, Hexagon.qoffset_to_cube(Hexagon.ODD, b)
        ),
    )
    equal_hex(
        "conversion_roundtrip even-r",
        a,
        Hexagon.roffset_to_cube(
            Hexagon.EVEN, Hexagon.roffset_from_cube(Hexagon.EVEN, a)
        ),
    )
    equal_offsetcoord(
        "conversion_roundtrip even-r",
        b,
        Hexagon.roffset_from_cube(
            Hexagon.EVEN, Hexagon.roffset_to_cube(Hexagon.EVEN, b)
        ),
    )
    equal_hex(
        "conversion_roundtrip odd-r",
        a,
        Hexagon.roffset_to_cube(
            Hexagon.ODD, Hexagon.roffset_from_cube(Hexagon.ODD, a)
        ),
    )
    equal_offsetcoord(
        "conversion_roundtrip odd-r",
        b,
        Hexagon.roffset_from_cube(
            Hexagon.ODD, Hexagon.roffset_to_cube(Hexagon.ODD, b)
        ),
    )


def test_offset_from_cube() -> None:
    equal_offsetcoord(
        "offset_from_cube even-q",
        OffsetCoord(1, 3),
        Hexagon.qoffset_from_cube(Hexagon.EVEN, Hex(1, 2, -3)),
    )
    equal_offsetcoord(
        "offset_from_cube odd-q",
        OffsetCoord(1, 2),
        Hexagon.qoffset_from_cube(Hexagon.ODD, Hex(1, 2, -3)),
    )


def test_offset_to_cube() -> None:
    equal_hex(
        "offset_to_cube even-",
        Hex(1, 2, -3),
        Hexagon.qoffset_to_cube(Hexagon.EVEN, OffsetCoord(1, 3)),
    )
    equal_hex(
        "offset_to_cube odd-q",
        Hex(1, 2, -3),
        Hexagon.qoffset_to_cube(Hexagon.ODD, OffsetCoord(1, 2)),
    )


def test_doubled_roundtrip() -> None:
    a = Hex(3, 4, -7)
    b = DoubledCoord(1, -3)
    equal_hex(
        "conversion_roundtrip doubled-q",
        a,
        Hexagon.qdoubled_to_cube(Hexagon.qdoubled_from_cube(a)),
    )
    equal_doubledcoord(
        "conversion_roundtrip doubled-q",
        b,
        Hexagon.qdoubled_from_cube(Hexagon.qdoubled_to_cube(b)),
    )
    equal_hex(
        "conversion_roundtrip doubled-r",
        a,
        Hexagon.rdoubled_to_cube(Hexagon.rdoubled_from_cube(a)),
    )
    equal_doubledcoord(
        "conversion_roundtrip doubled-r",
        b,
        Hexagon.rdoubled_from_cube(Hexagon.rdoubled_to_cube(b)),
    )


def test_doubled_from_cube() -> None:
    equal_doubledcoord(
        "doubled_from_cube doubled-q",
        DoubledCoord(1, 5),
        Hexagon.qdoubled_from_cube(Hex(1, 2, -3)),
    )
    equal_doubledcoord(
        "doubled_from_cube doubled-r",
        DoubledCoord(4, 2),
        Hexagon.rdoubled_from_cube(Hex(1, 2, -3)),
    )


def test_doubled_to_cube() -> None:
    equal_hex(
        "doubled_to_cube doubled-q",
        Hex(1, 2, -3),
        Hexagon.qdoubled_to_cube(DoubledCoord(1, 5)),
    )
    equal_hex(
        "doubled_to_cube doubled-r",
        Hex(1, 2, -3),
        Hexagon.rdoubled_to_cube(DoubledCoord(4, 2)),
    )


def test_hexagon() -> None:
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
