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

# !/usr/bin/python3
"""
Module containing a class for parameter validation
"""
import json
import os
import os.path
from pathlib import Path
from typing import Any

import jsonschema


class ParameterValidator:
    """
    Class validating the configuration as input for the generator.
    """

    __config_file: str = "not-assigned"
    __config_dir: str = "not-assigned"
    __configuration: dict = {}
    __configuration_schema_file: str = (
        os.path.dirname(os.path.realpath(__file__))
        + "/model/jsonSchema/configuration.schema.json"
    )
    __config_schema: dict = {}
    __error_message: str = ""
    __is_valid: bool = False

    # constructor
    def __init__(self, args: list[str]) -> None:
        self.args = args
        # Ensure there is an argument provided
        if len(self.args) <= 1:
            return

        target_path = Path(self.args[1])
        if target_path.is_dir():
            self.__config_dir = str(target_path)
            # Iterate over all JSON files in the directory
            self.__is_valid = True
            for json_file in target_path.glob("*.json"):
                self.__is_valid = self.is_valid and self.__process(str(json_file))
        elif target_path.is_file():
            self.__is_valid = self.__process(str(target_path))
        

    def __process(self, config_file: str) -> bool:
        print(f'Process: {config_file}')
        self.__config_file = config_file       
        if os.path.isfile(self.__config_file) is False:
            print("File", self.__config_file, "does not exist.")
        else:
            with open(self.__config_file) as content:
                self.__configuration[self.__config_file] = json.load(content)

        if os.path.isfile(self.__configuration_schema_file) is False:
            print("File", self.__configuration_schema_file, "does not exist.")
        else:
            with open(self.__configuration_schema_file) as content:
                self.__config_schema = json.load(content)
        
        return self.__is_json_valid(
            self.__configuration[self.__config_file], 
            self.__config_schema
        )
        

    def configuration_dir(self) -> str:
        """
        Getter for the configuration directory.
        :return Directory for files of the init configurations.
        """
        return self.__config_dir

    def configuration_file(self) -> str:
        """
        Getter for the configuration filename.
        :return Filename (path) for the init configuration.
        """
        return self.__config_file

    def configuration(self) -> list:
        """
        Getter for the configuration as input parameter.
        :return Init configurations as list.
        """
        return self.__configuration

    def is_valid(self) -> bool:
        """
        Getter for the validation result.
        :return Init configuration as dict.
        """
        return self.__is_valid

    def error_message(self) -> str:
        """
        Getter for the error message after validation process or an
        empty sting,  when configuration is valid.
        :return Error message as string.
        """
        return self.__error_message

    # private

    def __is_json_valid(
        self, json_data: dict[str, Any], json_schema: dict[str, Any]
    ) -> bool:
        """
        Method validating json against a schema
        """
        try:
            jsonschema.validate(instance=json_data, schema=json_schema)
            self.__error_message = ""
        except jsonschema.exceptions.ValidationError as err:
            self.__error_message = err
            return False
        return True
