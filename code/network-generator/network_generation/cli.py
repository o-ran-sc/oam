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

# inspired by https://github.com/rochacbruno/python-project-template

import os
import sys

from network_generation.base import NetworkGenerator
from network_generation.parameter_validator import ParameterValidator
from network_generation.view.network_viewer import NetworkViewer

"""
CLI interface for network_generation project.
Module as entry point to generate an ietf topology json
"""


def save_viewer_output(
    viewer: NetworkViewer,
    filename: str,
    task: dict[str, str] | dict[str, int],
    method_name: str,
) -> None:
    """
    Save the output using the specified method of NetworkViewer.
    """
    if task["enabled"]:
        method = getattr(viewer, method_name, None)
        if callable(method):
            method(filename, task["compressed"])


def main() -> None:  # pragma: no cover
    """
    The main function executes on commands:
    `python -m network_generation`.
    """
    validator = ParameterValidator(sys.argv)

    if not validator.is_valid():
        print(validator.error_message())
        return

    configuration = validator.configuration()
    generator = NetworkGenerator(configuration["network"])
    network = generator.generate()
    viewer = NetworkViewer(network)

    output_folder = str(configuration["outputFolder"])
    if not os.path.isdir(output_folder):
        os.makedirs(output_folder)

    name = str(configuration["network"]["name"]).lower()
    filename = os.path.join(output_folder, name)

    generation_tasks = configuration["generationTasks"]

    # Dictionary mapping task keys to viewer method names
    task_to_method = {
        "rfc8345": "rfc8345",
        "day0Config": "to_directory",
        "svg": "svg",
        "kml": "kml",
        "teiv": "teiv",
    }

    for task_key, method_name in task_to_method.items():
        save_viewer_output(
            viewer, filename, generation_tasks.get(task_key, {}), method_name
        )
