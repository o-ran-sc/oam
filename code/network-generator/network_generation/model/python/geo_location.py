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

# !/usr/bin/python3

"""
A collection of TypeDefinitions for a geographical location
"""
import math
from typing import Any, TypedDict, cast

from typing_extensions import Required

from network_generation.model.python.point import Point


class IGeoLocation(TypedDict):
    latitude: Required[float]
    longitude: Required[float]
    aboveMeanSeaLevel: Required[float]


default_value: IGeoLocation = {
    "latitude": 0,
    "longitude": 0,
    "aboveMeanSeaLevel": 0,
}


class GeoLocation:
    @staticmethod
    def default() -> dict[str, Any]:
        return cast(dict[str, Any], default_value)

    _equatorialRadius = 6378137  # meters
    _polarRadius = 6356752  # meters

    def __init__(self, data: IGeoLocation = default_value) -> None:
        self.latitude = data["latitude"]
        self.longitude = data["longitude"]
        self.aboveMeanSeaLevel = data["aboveMeanSeaLevel"]

    @property
    def equatorialRadius(self) -> int:
        return GeoLocation._equatorialRadius

    @property
    def polarRadius(self) -> int:
        return GeoLocation._polarRadius

    @property
    def latitude(self) -> float:
        return self._latitude

    @latitude.setter
    def latitude(self, value: float) -> None:
        if not (-90 <= value <= 90):
            msg: str = "Invalid latitude. Latitude must be between -90 and 90."
            raise ValueError(msg)
        self._latitude = value

    @property
    def longitude(self) -> float:
        return self._longitude

    @longitude.setter
    def longitude(self, value: float) -> None:
        if not (-180 <= value <= 180):
            raise ValueError(
                "Invalid longitude. Longitude must be between -180 and 180."
            )
        self._longitude = value

    @property
    def aboveMeanSeaLevel(self) -> float:
        return self._aboveMeanSeaLevel

    @aboveMeanSeaLevel.setter
    def aboveMeanSeaLevel(self, value: float) -> None:
        if not (-180 <= value <= 180):
            raise ValueError(
                "Invalid longitude. Longitude must be between -180 and 180."
            )
        self._aboveMeanSeaLevel = value

    def json(self) -> dict[str, float]:
        return {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "aboveMeanSeaLevel": self.aboveMeanSeaLevel,
        }

    def __str__(self) -> str:
        return str(self.json())

    def point_to_geo_location(self, point: Point) -> Any:
        """
        A static function which converts a point in pixels into a geographical
        location when the self is represented as Point(0,0)
        @param point : The point to be converted
        returns The converted GeoLocation object.
        """
        new_lat = self.latitude + (point.y / self.equatorialRadius) * (
            180 / math.pi
        )
        new_lon = self.longitude + (point.x / self.equatorialRadius) * (
            180 / math.pi
        ) / math.cos(self.latitude * math.pi / 180)

        geo_location: IGeoLocation = {
            "longitude": new_lon,
            "latitude": new_lat,
            "aboveMeanSeaLevel": self.aboveMeanSeaLevel,
        }
        return GeoLocation(geo_location)
