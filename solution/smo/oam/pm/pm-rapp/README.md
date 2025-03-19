

## Basic rAPP for demo purpose

### Manual build, tag and push to image repo

Build for docker or local kubernetes\
`./build.sh no-push [<image-tag>]`

Build for remote kubernetes - an externally accessible image repo (e.g. docker hub) is needed  \
`./build.sh <external-image-repo> [<image-tag>]`

## Function

The rApp starts a job subscription and prints (option) the received data to standard out. The purpose with this app is to simulate a real app subscribing to data.

The rapp can be configured to used plain text, plain text SSL or plain text SASL towards kafka.


### Configuration

The container expects the following environment variables:

- APPID : Should be a unique name (for example the name of the POD).

- APPNS : Should be the name of namespace.

- KAFKA_SERVER : Host and port of the kafka bootstrap server.

- TOPIC : The kafka topic where data is delivered by the job.

- ICS : Host and port to the information coordinator server.

The remaining env vars are optional.

- JWT_FILE : File path to mounted file where a valid token is stored. If used, the app expects the file to be regularly updated by a sidecar container. Only for SASL plain text towards kafka.

- SSLPATH : Path to mounted cert and key for secure kafka communication. Only for secure plaintext interface towards kafka.

- GZIP : If set (any value) the payload from kafka is expected to be in gzip format.

- LOG_PAYLOAD : If set (any value) the received payload is printed to standard out.

The following are optional and used only if the app fetches the token instead of a configured sidecar. Only for SASL plain text towards kafka.

- CREDS_GRANT_TYPE : Grant type (keycloak)
- CREDS_CLIENT_SECRET : Client secret (keycloak)
- CREDS_CLIENT_ID : Client id (keycloak)
- AUTH_SERVICE_URL : Url to keycloak for requesting a token.



The subscription json is expected on the path "/config/jobDefinition.json".
The rapp set topic and bootstrapserver from the above env vars before subscribing to the data.



## License

Copyright (C) 2023 Nordix Foundation. All rights reserved.
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.