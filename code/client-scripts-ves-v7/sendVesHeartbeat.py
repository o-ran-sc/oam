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
# Send a VES event for domain 'heartbeat'

# importing the datetime, json, requests, os socket and yaml library
from globalVesEventEmitter import getInitData, saveExample, sendVesEvent

# Globals
domain = 'heartbeat'
initData = getInitData(domain)
print('################################################################################')
print('# send SDN-Controller ' + domain)

initData['body']['event']['commonEventHeader']['domain'] = initData['domain']
initData['body']['event']['commonEventHeader']['eventId'] = initData['fqdn'] + '_' + initData['eventTime']
initData['body']['event']['commonEventHeader']['eventName'] = initData['domain'] + '_' + initData['config']['settings']['eventType']
initData['body']['event']['commonEventHeader']['eventType'] = initData['config']['settings']['eventType']
initData['body']['event']['commonEventHeader']['sequence'] = initData['config']['settings']['sequence']
initData['body']['event']['commonEventHeader']['reportingEntityName'] = initData['fqdn']
initData['body']['event']['commonEventHeader']['sourceName'] =initData['fqdn']
initData['body']['event']['commonEventHeader']['startEpochMicrosec'] = initData['timestamp']
initData['body']['event']['commonEventHeader']['lastEpochMicrosec'] = initData['timestamp']
initData['body']['event']['commonEventHeader']['nfNamingCode'] = 'SDN-Controller'
initData['body']['event']['commonEventHeader']['nfVendorName'] = 'O-RAN-SC OAM'

initData['body']['event']['heartbeatFields']['additionalFields']['eventTime'] = initData['eventTime']

# Save example body
saveExample(initData)

# Send VES Event
sendVesEvent(initData)