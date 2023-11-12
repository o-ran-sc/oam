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

from network_generation.model.python.geo_location import (
    IGeoLocation,
    GeoLocation,
)
from network_generation.model.python.point import Point


def test_geo_location() -> None:
    geo_location: GeoLocation = GeoLocation()
    expected: str = "{'latitude': 0, 'longitude': 0, 'aboveMeanSeaLevel': 0}"
    assert str(geo_location) == expected

    data: IGeoLocation = {
        "latitude": 40.1234,
        "longitude": -30.2345,
        "aboveMeanSeaLevel": 50,
    }
    geo_location = GeoLocation(data)
    expected = (
        "{'latitude': 40.1234, 'longitude': -30.2345, 'aboveMeanSeaLevel': 50}"
    )
    assert str(geo_location) == expected

    geo_location = geo_location.point_to_geo_location(Point(0, 0))
    assert str(geo_location) == expected
