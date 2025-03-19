#!/bin/bash

#  ============LICENSE_START===============================================
#  Copyright (C) 2023 Nordix Foundation. All rights reserved.
#  ========================================================================
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#  ============LICENSE_END=================================================
#

echo "Deleting files in shared volumes"
SD=$(dirname -- "$0")
echo " script-home: "$SD

cd $SD/..

if [ -d "shared-volume" ]; then
    cd "shared-volume"
    if [ $? -eq 0 ]; then
        if [[ "$PWD" == *"/shared-volume" ]]; then
            CNT=$(find . -maxdepth 2 -name 'A*' | wc -l)
            echo " Deleting $CNT files in $PWD"
            find . -maxdepth 2 -name 'A*' -delete
        else
            echo "Cannot determine if current dir is shared-volume"
            echo "Exiting..."
            exit 1
        fi
    else
        echo "Cannnot cd to shared-volume"
        echo "Exiting..."
        exit 1
    fi
else
    echo "Dir shared-volume not found"
    echo "Exiting..."
    exit 1
fi

echo "DONE"
exit 0
