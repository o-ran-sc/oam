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

"""
A collection of TypeDefinitions for a geographical location
"""
import math
from model.python.hexagon import Point


class IGeoLocationData:

    def __init__(self, latitude: float, longitude: float, aboveMeanSeaLevel: float):
        self.latitude = latitude
        self.longitude = longitude
        self.aboveMeanSeaLevel = aboveMeanSeaLevel

class IGeoLocation:

    def __init__(self, latitude: float = 0, longitude: float = 0, aboveMeanSeaLevel: float = 0):
        self.latitude = latitude
        self.longitude = longitude
        self.aboveMeanSeaLevel = aboveMeanSeaLevel

    def __str__(self):
        return f'lat : {self.latitude} : lon : {self.longitude} : amsl : {self.aboveMeanSeaLevel}'


class GeoLocation(IGeoLocation):
    _equatorialRadius = 6378137  # meters
    _polarRadius = 6356752  # meters

    def __init__(self, geoLocation: IGeoLocationData = None):
        super().__init__(
            geoLocation['latitude'] if geoLocation else 0,
            geoLocation['longitude'] if geoLocation else 0,
            geoLocation['aboveMeanSeaLevel'] if geoLocation else 0
        )

    @property
    def equatorialRadius(self):
        return GeoLocation._equatorialRadius

    @property
    def polarRadius(self):
        return GeoLocation._polarRadius

    def set_latitude(self, value: float):
        if not (-90 <= value <= 90):
            raise ValueError('Invalid latitude. Latitude must be between -90 and 90.')
        self.latitude = value

    def set_longitude(self, value: float):
        if not (-180 <= value <= 180):
            raise ValueError('Invalid longitude. Longitude must be between -180 and 180.')
        self.longitude = value

    def json(self):
        return {
            "latitude": self.latitude, 
            "longitude": self.longitude, 
            "aboveMeanSeaLevel": self.aboveMeanSeaLevel,      
        }
    
    def __str__(self):
        return str(self.json())
    
    def point_to_geo_location(self, point:Point):
        """
        A static function which converts a point in pixels into a geographical location
        when the self is represented as Point(0,0)
        @param point : The point to be converted
        returns The converted GeoLocation object.
        """
        equatorialRadius = 6378137  # meters
        new_lat = self.latitude + (point.y / equatorialRadius) * (180 / math.pi)
        new_lon = self.longitude + (point.x / equatorialRadius) * (180 / math.pi) / math.cos(self.latitude * math.pi / 180)

        geo_location: IGeoLocationData = {
            "longitude": new_lon,
            "latitude": new_lat,
            "aboveMeanSeaLevel": self.aboveMeanSeaLevel
        }
        return GeoLocation(geo_location)