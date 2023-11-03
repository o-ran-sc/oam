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
An abstract Class for O-RAN TerminationPoint
"""
from abc import abstractmethod
from model.python.o_ran_object import IORanObject, ORanObject


# Define the "IORanObject" interface
class IORanTerminationPointData(IORanObject):
    def __init__(self, supporter: str = None, parent=None, **kwargs):
        super().__init__(**kwargs)
        self.supporter = supporter
        self.parent = parent


# Define an O-RAN Termination Point (ietf-interface, onf:logical-termination-point) class
class ORanTerminationPoint(ORanObject, IORanTerminationPointData):
    def __init__(self, tp: IORanTerminationPointData = None, **kwargs):
        super().__init__(tp, **kwargs)
        self.supporter = tp["supporter"] if tp and "supporter" in tp else None
        self.parent = tp["parent"] if tp and "parent" in tp else None

    def to_topology(self):
        result: dict[str, dict] = {"tp-id": self.name}
        if self.supporter:
            network_ref: str = ""
            match str(type(self.parent)):
                case "<class 'model.python.o_ran_smo.ORanSmo'>":
                    network_ref = self.parent.parent.id
                case "<class 'model.python.o_ran_near_rt_ric.ORanNearRtRic'>":
                    network_ref = self.parent.parent.parent.id
                case "<class 'model.python.o_ran_cu.ORanCu'>":
                    network_ref = self.parent.parent.parent.parent.id
                case "<class 'model.python.o_ran_du.ORanDu'>":
                    network_ref = self.parent.parent.parent.parent.parent.id
                case "<class 'model.python.o_ran_cloud_du.ORanCloudDu'>":
                    network_ref = self.parent.parent.parent.parent.parent.id
                case "<class 'model.python.o_ran_ru.ORanRu'>":
                    network_ref = self.parent.parent.parent.parent.parent.parent.id
                case _:
                    print("unknown: implement " + str(type(self.parent)))
                    network_ref = "unknown: implement " + str(type(self.parent))

            result["supporting-termination-point"] = [
                {
                    "network-ref": network_ref,
                    "node-ref": self.parent.name,
                    "tp-ref": self.supporter,
                }
            ]
        return result
