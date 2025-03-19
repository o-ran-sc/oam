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

# args: <influxdb2-instance> <namespace>
get_influxdb2_token() {
	if [ $# -ne 1 ]; then
    	echo"get_influxdb2_token needs 1 arg, <influxdb2-instance> " $@
		exit 1
	fi

	__influxdb2_access_token=""
	while [ -z "$__influxdb2_access_token" ]; do
		export __influxdb2_access_token=$(docker exec $1 influx config ls --json | jq -r .default.token)
		if [ $? -ne 0 ]; then
			__influxdb2_access_token=""
			sleep 1
		fi
	done
	echo -n $__influxdb2_access_token
	return 0
}
