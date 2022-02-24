# Copyright 2022 highstreet technologies GmbH
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
Module as entry point to generatate a TAPI topology json
"""
import sys
from controller.parameter_validator import ParameterValidator
from controller.network_generator import TopologyGenerator
from view.network_viewer import NetworkViewer

validator: ParameterValidator = ParameterValidator(sys.argv)

if validator.is_valid():
    configuration = validator.configuration()
    generator = TopologyGenerator(configuration)
    network = generator.generate()
    viewer = NetworkViewer(network)

    filename: str = "output/network.json"
    if configuration['network']['name']:
        filename = "output/" + configuration['network']['name'] + ".json"
    viewer.json().save(filename)
    # viewer.json().showAsJson()

    filename: str = "output/network.svg"
    if configuration['network']['name']:
        filename = "output/" + configuration['network']['name'] + ".svg"
    viewer.svg(filename)

else:
    print(validator.error_message())
