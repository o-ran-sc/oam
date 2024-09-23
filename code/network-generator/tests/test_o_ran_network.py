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

from typing import Any
from network_generation.base import NetworkGenerator
from network_generation.parameter_validator import ParameterValidator
from network_generation.model.python.o_ran_network import ORanNetwork


def test_o_ran_network(get_path_name) -> None:
    config_file: str = get_path_name + "/test_config.json"

    validator: ParameterValidator = ParameterValidator(
        ["command", config_file]
    )

    if validator.is_valid():
        configuration: dict = validator.configuration()
        generator: NetworkGenerator = NetworkGenerator(
            configuration["network"]
        )
        o_ran_network: ORanNetwork = generator.generate()

        assert len(o_ran_network.id) == 36
        assert o_ran_network.administrativeState.value == "locked"
        topology: dict[str, Any] = o_ran_network.to_topology()
        assert len(topology["ietf-network:networks"]["network"]) == 1

        # ["network-id"] == (
        #     o_ran_network.id)
