#!/bin/bash

################################################################################
# Copyright 2023 highstreet technologies GmbH
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
################################################################################

# Excluded images is an array containing the name of the docker images we want to exclude from the analysis.
# Please modify it according to your needs.

# Installing syft
# curl -sSfL https://raw.githubusercontent.com/anchore/syft/main/install.sh | sh -s -- -b /usr/local/bin

# Installing grype
# curl -sSfL https://raw.githubusercontent.com/anchore/grype/main/install.sh | sh -s -- -b /usr/local/bin

SYFT=$(which syft)
if [ -z "$SYFT" ]; then
    echo "Unable to find syft. Please install."
    exit 1
fi

GRYPE=$(which grype)
if [ -z "$GRYPE" ]; then
    echo "Unable to find grype. Please install."
    exit 1
fi

mkdir -p out

excluded_images=()

image_names=($(docker ps --format '{{.Image}}' | tr ' ' '\n' | sort -u | tr '\n' ' '))

# avoid doublicates
for ele in "${excluded_images[@]}"; do
 image_names=(${image_names[@]/*${ele}*/})
done

echo "Analysing following images: ${image_names[*]}"

for image in "${image_names[@]}"; do
  image_name_no_repo="${image##*/}"
  echo "Creating SBOM for ${image} in ${image_name_no_repo}.sbom.spdx.json..."
  ${SYFT} -q ${image} -o spdx-json --file out/${image_name_no_repo}.sbom.spdx.json
  echo "Creating Vulnerabilities for ${image} in ${image_name_no_repo}.vulnerabilities.vex.json..."
  ${GRYPE} -q ${image} -o embedded-cyclonedx-vex-json --file out/${image_name_no_repo}.vulnerabilities.vex.json
done

echo "Done!"
