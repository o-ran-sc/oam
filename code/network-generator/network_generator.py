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
Module as entry point to generate an ietf topology json
"""
import os
import sys

from view.network_viewer import NetworkViewer
from controller.network_generator import NetworkGenerator
from controller.parameter_validator import ParameterValidator

validator: ParameterValidator = ParameterValidator(sys.argv)

if validator.is_valid():
    configuration = validator.configuration()
    generator = NetworkGenerator(configuration['network'])
    network = generator.generate()
    viewer = NetworkViewer(network)

    output_folder:str = configuration['output-folder']
    # If folder doesn't exist, then create it.
    if not os.path.isdir(output_folder):
        os.makedirs(output_folder)
        
    name: str = configuration['network']['name']

    # topology json
    if configuration['generation-tasks']['topology'] is True:
        filename: str = output_folder + "/" + name + "-operational.json"
        viewer.json().save(filename)

    # svg xml
    if configuration['generation-tasks']['svg'] is True:
        filename: str = output_folder + "/" + name + ".svg"
        viewer.svg(filename)

    # kml xml
    if configuration['generation-tasks']['kml'] is True:
        filename: str = output_folder + "/" + name + ".kml"
        viewer.kml(filename)

else:
    print(validator.error_message())
