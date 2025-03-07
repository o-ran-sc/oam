# Copyright 2024 highstreet technologies USA Corp.
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
Module for a class representing a O-RAN Network
"""

import os
import uuid
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from typing import Any, cast, Dict, List, Union

import network_generation.model.python.hexagon as Hexagon
from network_generation.model.python.geo_location import GeoLocation, IGeoLocation
from network_generation.model.python.hexagon import Layout
from network_generation.model.python.o_ran_object import IORanObject, ORanObject
from network_generation.model.python.o_ran_smo import ORanSmo
from network_generation.model.python.o_ran_spiral_radius_profile import SpiralRadiusProfile
from network_generation.model.python.point import Point


# Define the "IORanNetwork" interface
class IORanNetwork(IORanObject):
    network: Any


class ORanNetwork(ORanObject):
    """
    Class representing an O-RAN Network object.
    """

    __my_default_value: IORanNetwork = cast(IORanNetwork, ORanObject.default())
    __my_network_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, "Operator A"))
    # Get the current date and time in UTC
    __current_time = datetime.now(timezone.utc)
    # Format the time string as required
    __time_string = __current_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    __my_valid_for = {
        "startDateTime": f'{__current_time.strftime("%Y")}-01-01T00:00:00Z',
        "endDateTime": f'{__current_time.strftime("%Y")}-12-31T23:59:59Z',
    }

    # constructor
    def __init__(
        self,
        configuration: dict[str, dict],
        data: dict[str, Any] = cast(dict[str, Any], __my_default_value),
        **kwargs: dict[str, Any],
    ) -> None:
        o_ran_network_data: IORanNetwork = self._to_o_ran_network_data(data)
        super().__init__(cast(dict[str, Any], o_ran_network_data), **kwargs)
        self.__configuration = configuration

        self.name = str(configuration.get("name", "WhiteNetwork"))
        self.operationalState = str(configuration.get("operationalState", "disabled"))
        self._center: IGeoLocation = cast(
            IGeoLocation, configuration["center"]
        )

        # Calculate layout size using the configuration values.
        nr_cell_du = configuration["pattern"]["nrCellDu"]
        size = int(
            int(nr_cell_du["maxReach"])
            / (1 + int(nr_cell_du["cellScaleFactorForHandoverArea"]) / 100)
        )
        layout = Layout(
            Hexagon.layout_flat, Point(size, size), Point(0, 0)
        )  # 1 pixel = 1 meter
        self._spiral_radius_profile: SpiralRadiusProfile = SpiralRadiusProfile({
            "oRanSmoSpiralRadiusOfNearRtRics": configuration["pattern"][
                "smo"]["nearRtRicSpiralRadius"],
            "oRanNearRtRicSpiralRadiusOfOCus": configuration["pattern"][
                "nearRtRic"]["oRanCuSpiralRadius"],
            "oRanCuSpiralRadiusOfODus": configuration["pattern"]["oRanCu"][
                "oRanDuSpiralRadius"],
            "oRanDuSpiralRadiusOfTowers": configuration["pattern"][
                "oRanDu"]["towerSpiralRadius"],
        })
        self._o_ran_smo = ORanSmo({
            "name": "O-RAN-SMO",
            "geoLocation": self.center,
            "layout": layout,
            "parent": self,
            "network": self,
            "operationalState": self.operationalState
        })

    def _to_o_ran_network_data(self, data: dict[str, Any]) -> IORanNetwork:
        result: IORanNetwork = self.__my_default_value
        for key, key_type in IORanNetwork.__annotations__.items():
            if key in data:
                result[key] = data[key]  # type: ignore
        return result

    @property
    def center(self) -> GeoLocation:
        """
        Getter for a json object representing the O-RAN Network.
        :return O-RAN Network as json object.
        """
        return GeoLocation(self._center)

    @property
    def spiral_radius_profile(self) -> SpiralRadiusProfile:
        """
        Getter for a json object representing the SpiralRadiusProfile.
        :return SpiralRadiusProfile.
        """
        return self._spiral_radius_profile

    @property
    def configuration(self) -> dict[str, Any]:
        """
        Getter for a json object representing the O-RAN Network.
        :return O-RAN Network as json object.
        """
        return self.__configuration

    def __update_value_by_uuid(self, data: dict[str, Any], target_uuid: str, param_name: str, new_value: str) -> bool:
        """
        Recursively searches for an object with the target UUID and updates its parameter value.

        :param data: The JSON dictionary (can be a list or dict).
        :param target_uuid: The UUID to find.
        :param param_name: The parameter key to modify.
        :param new_value: The new value to set.
        :return: True if updated, False otherwise.
        """
        if isinstance(data, dict):
            # If 'uuid' matches, update the parameter
            if data.get("o-ran-sc-network:uuid") == target_uuid:
                if param_name in data:
                    data[param_name] = new_value
                    return True  # Stop recursion as we found and updated it

            # Recursively search in nested dictionaries or lists
            for _, value in data.items():
                if isinstance(value, (dict, list)) and self.__update_value_by_uuid(value, target_uuid, param_name, new_value):
                    return True  # Stop searching after finding the target

        elif isinstance(data, list):
            # Iterate over list items
            for item in data:
                if self.__update_value_by_uuid(item, target_uuid, param_name, new_value):
                    return True  # Stop searching after finding the target

        return False  # UUID not found

    def to_topology(self) -> Dict[str, Any]:
        """
        Generate and return the network topology as a dictionary.
        """
        profile = self.configuration.get("disabledResourcesProfile", {})
        resource_types = profile.keys()
        nodes: List[Dict[str, Any]] = self._o_ran_smo.to_topology_nodes()

        # Initialize identifier lists for each resource type.
        identifier_lists: Dict[str, List[str]] = {identifier: [] for identifier in resource_types}

        for node in nodes:
            node_type = node.get("o-ran-sc-network:type")
            node_uuid = node.get("o-ran-sc-network:uuid")
            if node_type in resource_types and node_uuid:
                identifier_lists[node_type].append(node_uuid)

            termination_points = node.get("ietf-network-topology:termination-point", [])
            for tp in termination_points:
                if tp.get("o-ran-sc-network:type") == "o-ran-sc-network:cell":
                    # Create key for cells if not already present.
                    if "o-ran-sc-network:cell" not in identifier_lists:
                        identifier_lists["o-ran-sc-network:cell"] = []
                    cell_uuid = tp.get("o-ran-sc-network:uuid")
                    if cell_uuid:
                        identifier_lists["o-ran-sc-network:cell"].append(cell_uuid)

        disabled_resources: List[int] = []
        for resource_type in resource_types:
            profile_percentage = profile[resource_type]
            total_nodes = len(identifier_lists[resource_type])
            max_disabled = round(profile_percentage * total_nodes / 100)
            disabled_resources.append(max_disabled)
            identifier_lists[resource_type].sort()
            identifier_lists[resource_type] = identifier_lists[resource_type][:max_disabled]
            for identifier in identifier_lists[resource_type]:
                self.__update_value_by_uuid(
                    nodes,
                    identifier,
                    "o-ran-sc-network:operational-state",
                    "disabled"
                )

        links: List[Dict[str, Any]] = self._o_ran_smo.to_topology_links()
        return {
            "ietf-network:networks": {
                "network": [
                    {
                        "network-id": self.id,
                        "o-ran-sc-network:name": self.name,
                        "o-ran-sc-network:operational-state": self.operationalState,
                        "node": nodes,
                        "ietf-network-topology:link": links,
                    }
                ],
            }
        }

    def to_directory(self, parent_dir: str) -> None:
        """
        Export the network topology to a specified directory.
        """
        self._o_ran_smo.to_directory(os.path.join(parent_dir, self.id))

    def toKml(self) -> ET.Element:
        """
        Generate a KML representation of the network.

        Returns:
            An xml.etree.ElementTree.Element representing the KML.
        """
        root = ET.Element("kml", xmlns="http://www.opengis.net/kml/2.2")
        document = ET.SubElement(root, "Document")
        open_elem = ET.SubElement(document, "open")
        open_elem.text = "1"
        name_elem = ET.SubElement(document, "name")
        name_elem.text = self.name

        document.append(self._o_ran_smo.toKml())
        return root

    def toSvg(self) -> ET.Element:
        """
        Getter for a xml/svg Element object representing the Network.
        :return Network as SVG object.
        """
        root: ET.Element = ET.Element(
            "svg",
            # width=str(self.__svg_width()),
            # height=str(self.__svg_height()),
            # viewBox=" ".join([
            #     str(-3*self.FONTSIZE),
            #     str(-3*self.FONTSIZE),
            #     str(self.__svg_width()),
            #     str(self.__svg_height())]
            # ),
            xmlns="http://www.w3.org/2000/svg",
        )
        desc = ET.Element("desc")
        desc.text = "\n context: " + self.id + "\n name: " + self.name
        root.append(desc)

        title = ET.Element("title")
        title.text = str(self.configuration["name"])
        root.append(title)

        # root.append(self.__context.svg(x, y))
        return root

    def json(self) -> Dict[str, Any]:
        """
        Return a JSON representation of the network.
        """
        return super().json()

    def to_teiv_data(self) -> Dict[str, Any]:
        """
        Return the network data formatted for TEIV.

        Returns:
            A dictionary containing TEIV entities and relationships.
        """
        entities = self._o_ran_smo.add_teiv_data_entities()
        relationships = self._o_ran_smo.add_teiv_data_relationships()
        return {"entities": [entities], "relationships": [relationships]}