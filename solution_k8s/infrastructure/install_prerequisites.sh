#!/bin/bash

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

# Function to install packages on Rocky Linux
install_packages_rocky() {
    sudo dnf install -y "$@"
}

# Function to install packages on Ubuntu
install_packages_ubuntu() {
    sudo apt update
    sudo apt install -y "$@"

    # if e.g. docker is already installed kubeone might fail
    # this workaround for debian/ubuntu prevents this issue.
    
    if apt-cache madison containerd.io | grep -q '1.6'; then
        echo "containerd.io 1.6.* package is available, proceeding with installation..."
        
        # Install the containerd.io package
        sudo DEBIAN_FRONTEND=noninteractive apt-get install --option Dpkg::Options::=--force-confold --no-install-recommends -y 'containerd.io=1.6.*' --allow-downgrades
    
        # Verify installation
        if containerd --version; then
            echo "containerd.io installed successfully."
        else
            echo "Failed to verify containerd.io installation."
        fi
    else
        echo "containerd.io 1.6.* package is not available in the repositories."
    fi
}

# Determine the distribution
if [ -f /etc/os-release ]; then
    . /etc/os-release
    if [[ "$ID" == "rocky" ]]; then
        install_packages_rocky "unzip" "jq" # Replace with your packages
    elif [[ "$ID" == "ubuntu" ]]; then
        install_packages_ubuntu "unzip" "jq" # Replace with your packages
    else
        echo "Unsupported distribution: $ID"
        exit 1
    fi
else
    echo "/etc/os-release not found. Cannot determine the distribution."
    exit 1
fi
