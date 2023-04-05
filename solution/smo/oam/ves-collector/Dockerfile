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

ARG BASEIMAGE=nexus3.onap.org:10001/onap/org.onap.dcaegen2.collectors.ves.vescollector:1.8.0
FROM ubuntu:22.04 AS stage-0
RUN apt update && apt install -y python3 git
COPY install.py /
COPY externalRepo.json /
COPY externalRepo /opt/app/VESCollector/etc/externalRepo
RUN python3 install.py -c /externalRepo.json -d /opt/app/VESCollector/etc/externalRepo

FROM ${BASEIMAGE}
COPY --from=stage-0 --chown=vescollector:vescollector /opt/app/VESCollector/etc/externalRepo /opt/app/VESCollector/etc/externalRepo