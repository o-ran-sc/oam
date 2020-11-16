################################################################################
# Copyright 2020 highstreet technologies GmbH and others
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

################################################################################
# OpenDaylight docker file

FROM adoptopenjdk/openjdk11:alpine-slim

ENV ODL_VERSION=0.13.0

RUN apk update && \
    apk add bash && \
    apk add wget && \ 
    mkdir /opt/opendaylight

WORKDIR /opt

RUN wget https://nexus.opendaylight.org/content/repositories/opendaylight.release/org/opendaylight/integration/opendaylight/${ODL_VERSION}/opendaylight-${ODL_VERSION}.tar.gz

RUN tar -xvzf opendaylight-${ODL_VERSION}.tar.gz -C opendaylight --strip-components 1 && \
    rm -rf opendaylight-${ODL_VERSION}.tar.gz

COPY ./org.apache.karaf.features.cfg /opt/opendaylight/etc/org.apache.karaf.features.cfg
COPY ./org.ops4j.pax.logging.cfg /opt/opendaylight/etc/org.ops4j.pax.logging.cfg

WORKDIR /opt/opendaylight

EXPOSE 8181 8101

CMD ["./bin/karaf", "server"]
