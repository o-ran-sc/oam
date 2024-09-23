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
from typing import Any, Generator
import pytest


@pytest.fixture(autouse=True)
def get_path_name(request: pytest.FixtureRequest) -> str:
    return os.path.dirname(os.path.abspath(request.path.name))


# each test runs on cwd to its temp dir
@pytest.fixture(autouse=True)
def go_to_tmpdir(request: pytest.FixtureRequest) -> Generator[None, Any, None]:
    # Get the fixture dynamically by its name.
    tmpdir = request.getfixturevalue("tmpdir")
    # ensure local test created packages can be imported
    sys.path.insert(0, str(tmpdir))
    # Chdir only for the duration of the test.
    with tmpdir.as_cwd():
        yield
