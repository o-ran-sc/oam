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

# !/usr/bin/python

"""
A Class representing an O-RAN distributed unit (ORanDu)
"""
import xml.etree.ElementTree as ET
import os
from typing import Any, cast

from network_generation.model.python.o_ran_node import IORanNode, ORanNode
from network_generation.model.python.o_ran_termination_point import (
    ORanTerminationPoint,
)


# Define the "IORanDu" interface
class IORanDu(IORanNode):
    o_ran_ru_count: int


default_value: IORanDu = cast(
    IORanDu,
    {
        **ORanNode.default(),
        **{"oRanRuCount": 1},
    },
)


# Define an abstract O-RAN Node class
class ORanDu(ORanNode):
    def __init__(
        self,
        data: dict[str, Any] = cast(dict[str, Any], default_value),
        **kwargs: dict[str, Any]
    ) -> None:
        o_ran_du_data: IORanDu = self._to_o_ran_du_data(data)
        super().__init__(cast(dict[str, Any], o_ran_du_data), **kwargs)
        self._o_ran_ru_count = (
            o_ran_du_data["oRanRuCount"]
            if o_ran_du_data and "oRanRuCount" in o_ran_du_data
            else 1
        )
        self.type = "ntsim-ng-o-du"

    def _to_o_ran_du_data(self, data: dict[str, Any]) -> IORanDu:
        result: IORanDu = default_value
        for key, key_type in IORanDu.__annotations__.items():
            if key in data:
                result[key] = data[key]  # type: ignore
        return result

    def termination_points(self) -> list[ORanTerminationPoint]:
        result: list[ORanTerminationPoint] = super().termination_points()
        phy_tp: str = "-".join([self.name, "phy".upper()])
        result.append(ORanTerminationPoint({"id": phy_tp, "name": phy_tp}))
        for interface in ["e2", "o1", "ofhm", "ofhc", "ofhu", "ofhs"]:
            id: str = "-".join([self.name, interface.upper()])
            result.append(
                ORanTerminationPoint(
                    {"id": id, "name": id, "supporter": phy_tp, "parent": self}
                )
            )
        return result

    def to_topology_nodes(self) -> list[dict[str, Any]]:
        result: list[dict[str, Any]] = super().to_topology_nodes()
        return result

    def to_topology_links(self) -> list[dict[str, Any]]:
        result: list[dict[str, Any]] = super().to_topology_links()
        for interface in ["e2", "o1"]:
            link_id: str = "".join(
                [interface, ":", self.name, "<->", self.parent.name]
            )
            source_tp: str = "-".join([self.name, interface.upper()])
            dest_tp: str = "-".join([self.parent.name, interface.upper()])
            result.append(
                {
                    "link-id": link_id,
                    "source": {
                        "source-node": self.name,
                        "source-tp": source_tp,
                    },
                    "destination": {
                        "dest-node": self.parent.name,
                        "dest-tp": dest_tp,
                    },
                }
            )
        return result

    def toKml(self) -> ET.Element:
        o_ran_du: ET.Element = ET.Element("Folder")
        open: ET.Element = ET.SubElement(o_ran_du, "open")
        open.text = "1"
        name: ET.Element = ET.SubElement(o_ran_du, "name")
        name.text = self.name
        # for tower in self.towers:
        #     o_ran_du.append(tower.toKml())
        return o_ran_du

    def toSvg(self) -> ET.Element:
        return ET.Element("to-be-implemented")

    def to_directory(self, parent_dir: str) -> None:
        parent_path = os.path.join(parent_dir, self.type)
        path = os.path.join(parent_path, self.name)
        if not os.path.exists(parent_path):
            os.makedirs(parent_path, exist_ok=True)
        if not os.path.exists(path):
            os.mkdir(path)
