#!/usr/bin/env python
################################################################################
# Copyright 2024 highstreet technologies
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os
import re
import time

# Specify the directory containing the files
directory_path = "."

# Define the regular expression to search for revision dates
revision_date_regex = r"revision\s*\"{0,1}(\d{4}-\d{2}-\d{2})"

# Loop over each file in the directory
for file_name in os.listdir(directory_path):
    # Check if the file is a .yang file
    if file_name.endswith(".yang"):
        # Get the full file path
        file_path = os.path.join(directory_path, file_name)

        # Open the file and read its contents
        with open(file_path, "r") as f:
            yang_contents = f.read()

        # Find all revision dates within the yang contents
        matches = re.findall(revision_date_regex, yang_contents)
        print(file_name, matches)

        # Get the latest revision date
        latest_revision_date = max(matches) if matches else None

        # If a revision date was found, create the new file name with the revision date
        if latest_revision_date:
            # Format the latest revision date as "YYYY-MM-DD"
            revision_date = time.strptime(latest_revision_date, "%Y-%m-%d")
            revision_date_str = time.strftime("%Y-%m-%d", revision_date)

            # Create the new file name with the revision date
            file_name_with_date = f"{os.path.splitext(file_path)[0]}@{revision_date_str}{os.path.splitext(file_path)[1]}"

            # Rename the file with the revision date
            os.rename(file_path, file_name_with_date)

            # Create a symbolic link to the previous file name
            previous_file_link = f"{os.path.splitext(file_path)[0]}{os.path.splitext(file_path)[1]}"
            os.symlink(file_name_with_date, previous_file_link)
