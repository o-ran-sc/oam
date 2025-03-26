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

FROM golang:1.20.3-buster AS build

WORKDIR /app

COPY main.go .
RUN go mod init main
RUN go mod tidy

RUN go build -o /pm-rapp

FROM gcr.io/distroless/base-debian11

WORKDIR /
## Copy from "build" stage
COPY --from=build /pm-rapp .

ENTRYPOINT ["/pm-rapp"]
