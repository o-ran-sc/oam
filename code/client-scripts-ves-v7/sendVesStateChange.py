#!/usr/bin/env python
################################################################################
# Copyright 2021 highstreet technologies GmbH
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

################################################################################
# Send a VES event for domain 'stateChange'

# importing the sys, json, requests library
import sys
import getopt
import json
import requests
from globalVesEventEmitter import getInitData, saveExample, sendVesEvent

# Construct VES body and send
def performJob(domain, pnfId):
    initData = getInitData(domain)
    initData['pnfId'] = pnfId

    print('################################################################################')
    print('# send VES ' + domain)

    initData['body']['event']['commonEventHeader']['domain'] = initData['domain']
    initData['body']['event']['commonEventHeader']['eventId'] = initData['fqdn'] + \
        '_' + initData['eventTime']
    initData['body']['event']['commonEventHeader']['eventName'] = initData['domain'] + \
        '_' + initData['config']['settings']['eventType']
    initData['body']['event']['commonEventHeader']['eventType'] = initData['config']['settings']['eventType']
    initData['body']['event']['commonEventHeader']['sequence'] = initData['config']['settings']['sequence']
    initData['body']['event']['commonEventHeader']['reportingEntityName'] = initData['fqdn']
    initData['body']['event']['commonEventHeader']['sourceName'] = initData['pnfId']
    initData['body']['event']['commonEventHeader']['startEpochMicrosec'] = initData['timestamp']
    initData['body']['event']['commonEventHeader']['lastEpochMicrosec'] = initData['timestamp']
    initData['body']['event']['commonEventHeader']['nfNamingCode'] = initData['pnfId']
    initData['body']['event']['commonEventHeader']['nfVendorName'] = 'O-RAN-SC OAM'

    initData['body']['event']['stateChangeFields']['additionalFields']['eventTime'] = initData['eventTime']
    initData['body']['event']['stateChangeFields']['stateInterface'] = initData['interface']

    # Save example body
    saveExample(initData)

    # Send VES Event
    sendVesEvent(initData)


# Analysing command line parameters
def main(argv):
    domain = 'stateChange'
    usage = 'sendVesStateChange.py --pnfId <physical-network-function-nwuid>'
    pnfId = ''
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["pnfId="])
    except getopt.GetoptError:
        print(usage)
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print(usage)
            sys.exit()
        elif opt in ("-p", "--pnfId"):
            pnfId = arg
            performJob(domain, pnfId)


if __name__ == "__main__":
    main(sys.argv[1:])
