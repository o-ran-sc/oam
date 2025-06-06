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
#
# inspired by http://www.redblobgames.com/grids/hexagons/

# !/usr/bin/python3

from __future__ import division, print_function

from typing import NamedTuple


class Point(NamedTuple):
    x: float
    y: float

    def __str__(self) -> str:
        return f"{self.x},{self.y}"
