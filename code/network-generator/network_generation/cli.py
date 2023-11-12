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

import os
import sys

from network_generation.base import NetworkGenerator
from network_generation.model.python.o_ran_network import ORanNetwork
from network_generation.parameter_validator import ParameterValidator
from network_generation.view.network_viewer import NetworkViewer

"""
CLI interface for network_generation project.
Module as entry point to generate an ietf topology json
"""


def main() -> None:  # pragma: no cover
    """
    The main function executes on commands:
    `python -m network_generation`.

    """
    validator: ParameterValidator = ParameterValidator(sys.argv)

    if validator.is_valid():
        configuration: dict = validator.configuration()
        generator: NetworkGenerator = NetworkGenerator(
            configuration["network"]
        )
        network: ORanNetwork = generator.generate()
        viewer: NetworkViewer = NetworkViewer(network)

        output_folder: str = configuration["output-folder"]
        # If folder doesn't exist, then create it.
        if not os.path.isdir(output_folder):
            os.makedirs(output_folder)

        name: str = configuration["network"]["name"]
        filename: str = ""

        # topology json
        if configuration["generation-tasks"]["topology"] is True:
            filename = output_folder + "/" + name + "-operational.json"
            viewer.json().save(filename)

        # svg xml
        if configuration["generation-tasks"]["svg"] is True:
            filename = output_folder + "/" + name + ".svg"
            viewer.svg(filename)

        # kml xml
        if configuration["generation-tasks"]["kml"] is True:
            filename = output_folder + "/" + name + ".kml"
            viewer.kml(filename)

    else:
        print(validator.error_message())
