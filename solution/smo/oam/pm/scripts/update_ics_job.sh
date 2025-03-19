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

# args: <job-id> <job-index-suffix> [<access-token>]
# job file shall exist in file "".job.json"
update_ics_job() {

    ICS_PORT=8083
    JOB=$(<.job.json)
    echo $JOB
    retcode=1
    echo "Updating job $1"
    while [ $retcode -ne 0 ]; do
        if [ -z "$2" ]; then
            __bearer=""
        else
            __bearer="Authorization: Bearer $TOKEN"
        fi
        STAT=$(curl -s -X PUT -w '%{http_code}' -H accept:application/json -H Content-Type:application/json http://localhost:$ICS_PORT/data-consumer/v1/info-jobs/$1 --data-binary @.job.json -H "$__bearer" )
        retcode=$?
        echo "curl return code: $retcode"
        if [ $retcode -eq 0 ]; then
            status=${STAT:${#STAT}-3}
            echo "http status code: "$status
            if [ "$status" == "200" ]; then
                echo "Job created ok"
            elif [ "$status" == "201" ]; then
                echo "Job created ok"
            else
                retcode=1
            fi
        fi
        sleep 1
    done
}
