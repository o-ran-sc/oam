#!/bin/bash

# Function to install packages on Rocky Linux
install_packages_rocky() {
    sudo dnf install -y "$@"
}

# Function to install packages on Ubuntu
install_packages_ubuntu() {
    sudo apt update
    sudo apt install -y "$@"
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
