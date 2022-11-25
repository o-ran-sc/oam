#!/bin/bash
################################################################################
#
# Copyright 2019 highstreet technologies GmbH and others
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

################################################################################
# Script to demo interface tests

################################################################################
# send SDN-R heartbeat
./sendHeartbeat.sh

################################################################################
# send pnf registration event
./pnfRegister.sh pnf2
./pnfRegister.sh FYNG
./pnfRegister.sh R2D2
./pnfRegister.sh 7DEV
./pnfRegister.sh nSky
./pnfRegister.sh 1OSF
./pnfRegister.sh SDNR

################################################################################
# raise fault
./sendFault.sh pnf2 lossOfSignal CRITICAL
./sendFault.sh FYNG TCA MAJOR
./sendFault.sh R2D2 TCA MINOR
./sendFault.sh 7DEV signalIsLost CRITICAL
./sendFault.sh nSky LossOfSignalAlarm CRITICAL
./sendFault.sh 1OSF HAAMRunningInLowerModulation MAJOR
./sendFault.sh SDNR connectionLossNe MAJOR

################################################################################
# clear fault
./sendFault.sh pnf2 lossOfSignal NORMAL
./sendFault.sh FYNG TCA NORMAL
./sendFault.sh R2D2 TCA NORMAL
./sendFault.sh 7DEV signalIsLost NORMAL
./sendFault.sh nSky LossOfSignalAlarm NORMAL
./sendFault.sh 1OSF HAAMRunningInLowerModulation NORMAL
./sendFault.sh SDNR connectionLossNe NORMAL

################################################################################
# raise stndDefined Alarm
./sendStndDefinedNotifyAlarm.sh pnf2 lossOfSignal CRITICAL new
./sendStndDefinedNotifyAlarm.sh FYNG TCA MAJOR new
./sendStndDefinedNotifyAlarm.sh R2D2 TCA MINOR new
./sendStndDefinedNotifyAlarm.sh 7DEV signalIsLost CRITICAL new
./sendStndDefinedNotifyAlarm.sh nSky LossOfSignalAlarm CRITICAL new
./sendStndDefinedNotifyAlarm.sh 1OSF HAAMRunningInLowerModulation MAJOR new
./sendStndDefinedNotifyAlarm.sh SDNR connectionLossNe MAJOR new

################################################################################
# clear stndDefined Alarm
./sendStndDefinedNotifyAlarm.sh pnf2 lossOfSignal CRITICAL cleared
./sendStndDefinedNotifyAlarm.sh FYNG TCA MAJOR cleared
./sendStndDefinedNotifyAlarm.sh R2D2 TCA MINOR cleared
./sendStndDefinedNotifyAlarm.sh 7DEV signalIsLost CRITICAL cleared
./sendStndDefinedNotifyAlarm.sh nSky LossOfSignalAlarm CRITICAL neclearedw
./sendStndDefinedNotifyAlarm.sh 1OSF HAAMRunningInLowerModulation MAJOR cleared
./sendStndDefinedNotifyAlarm.sh SDNR connectionLossNe MAJOR cleared

################################################################################
# raise threshold crossed alerts
./sendTca.sh pnf2 TCA CONT
./sendTca.sh FYNG TCA SET
./sendTca.sh R2D2 TCA CONT
./sendTca.sh 7DEV thresholdCrossed SET
./sendTca.sh nSky RSLBelowThreshold CONT
./sendTca.sh 1OSF TCA SET

################################################################################
# clear threshold crossed alerts
./sendTca.sh pnf2 TCA CLEAR
./sendTca.sh FYNG TCA CLEAR
./sendTca.sh R2D2 TCA CLEAR
./sendTca.sh 7DEV thresholdCrossed CLEAR
./sendTca.sh nSky RSLBelowThreshold CLEAR
./sendTca.sh 1OSF TCA CLEAR

################################################################################
# send 15min performance measurement data
./send15minPm.sh pnf2
./send15minPm.sh FYNG
./send15minPm.sh R2D2
./send15minPm.sh 7DEV
./send15minPm.sh nSky
./send15minPm.sh 1OSF

################################################################################
# send o1-notify-pnf-registration
./sendStndDefinedO1NotifyPnfRegistration.sh pnf2
./sendStndDefinedO1NotifyPnfRegistration.sh FYNG
./sendStndDefinedO1NotifyPnfRegistration.sh R2D2
./sendStndDefinedO1NotifyPnfRegistration.sh 7DEV
./sendStndDefinedO1NotifyPnfRegistration.sh nSky
./sendStndDefinedO1NotifyPnfRegistration.sh 1OSF

################################################################################
# send o1-notify-pnf-registration
./sendStndDefinedNotifyFileReady.sh pnf2
./sendStndDefinedNotifyFileReady.sh FYNG
./sendStndDefinedNotifyFileReady.sh R2D2
./sendStndDefinedNotifyFileReady.sh 7DEV
./sendStndDefinedNotifyFileReady.sh nSky
./sendStndDefinedNotifyFileReady.sh 1OSF
