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

# inspired by https://github.com/rochacbruno/python-project-template

"""
network_generation base module.

This is the principal module of the network_generation project.
"""

from network_generation.model.python.o_ran_network import ORanNetwork

# example constant variable
NAME = "network_generation"


class NetworkGenerator:
    """
    Class containing all methods to generate a network.
    The generation process is influenced by a configuration in json format.
    """

    __configuration: dict = {}

    # constructor
    def __init__(self, configuration: dict):
        self.__configuration = configuration

    # getters
    def configuration(self) -> dict:
        """
        Getter returning the object configuration
        :return A NetworkGenerator configuration
        """
        return self.__configuration

    # returns a JSON serializable object
    def generate(self) -> ORanNetwork:
        """
        Method to start the generation process.
        :return The ORanNetwork object.
        """
        return ORanNetwork(self.configuration())
