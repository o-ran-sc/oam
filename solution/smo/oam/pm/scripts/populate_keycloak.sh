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

# Script intended to be sourced by other script to add functions to the keycloak rest API

#KC_URL=http://localhost:8462
KC_URL=https://identity.smo.o-ran-sc.org
echo "Keycloak url: "$KC_URL

__get_admin_token() {
    echo "Get admin token"
    ADMIN_TOKEN=""
    while [ "${#ADMIN_TOKEN}" -lt 20 ]; do
        ADMIN_TOKEN=$(curl -k -s -X POST --max-time 2     "$KC_URL/realms/master/protocol/openid-connect/token"     -H "Content-Type: application/x-www-form-urlencoded"     -d "username=admin" -d "password=Kp8bJ4SXszM0WXlhak3eHlcse2gAw84vaoGGmJvUy2U" -d 'grant_type=password' -d "client_id=admin-cli"  |  jq -r '.access_token')
        if [ "${#ADMIN_TOKEN}" -lt 20 ]; then
            echo "Could not get admin token, retrying..."
            echo "Retrieved token: $ADMIN_TOKEN"
        fi
    done
    echo "Admin token: ${ADMIN_TOKEN:0:10}..."
    echo $ADMIN_TOKEN > .admin_token
    __ADM_TOKEN_TS=$SECONDS
}

__check_admin_token() {
    __diff=$(($SECONDS-$__ADM_TOKEN_TS))
    if [ $__diff -gt 15 ]; then
        __get_admin_token
    fi
}

__get_admin_token

indent1() { sed 's/^/ /'; }
indent2() { sed 's/^/  /'; }

decode_token() {
    echo "Decoding access_token"
    echo $1 | jq -R 'split(".") | .[0,1] | @base64d | fromjson'
}

decode_jwt() {
    echo "Decoding jwt"
    echo $1 | jq -r .access_token | jq -R 'split(".") | .[0,1] | @base64d | fromjson'
}

list_realms() {
    echo "Listing all realms"
    __check_admin_token
    curl -k -s \
        -X GET \
        -H "Authorization: Bearer ${ADMIN_TOKEN}" \
        "$KC_URL/admin/realms" | jq -r '.[].id' | indent2
}
delete_realms() {
    echo "$@"
    for realm in "$@"; do
        echo "Attempt to delete realm: $realm"
        __check_admin_token
        curl -k -s \
        -X DELETE \
        -H "Authorization: Bearer ${ADMIN_TOKEN}" \
        "$KC_URL/admin/realms/$realm" | indent1
        if [ $? -ne 0 ]; then
            echo "Command failed"
            exit 1
        fi
        echo " OK"
    done
}

create_realms() {
    echo "Creating realms: $@"
    while [ $# -gt 0 ]; do
        echo " Attempt to create realm: $1"
        __check_admin_token
cat > .jsonfile1 <<- "EOF"
{
"realm":"$__realm_name",
"enabled":true
}
EOF
        export __realm_name=$1
        envsubst < .jsonfile1 > .jsonfile2
        curl -k -s \
        -X POST \
        -H "Authorization: Bearer ${ADMIN_TOKEN}" \
        -H "Content-Type: application/json" \
        -d @".jsonfile2" \
        "$KC_URL/admin/realms" | indent2
        if [ $? -ne 0 ]; then
            echo "Command failed"
            exit 1
        fi
        echo "  OK"
        shift
    done
}

create_clients() {
    __realm=$1
    shift
    echo "Attempt to create clients $@ for realm: $__realm"

cat > .jsonfile1 <<- "EOF"
{
   "clientId":"$__client_name",
   "publicClient": false,
   "serviceAccountsEnabled": true,
   "rootUrl":"https://example.com/example/",
   "adminUrl":"https://example.com/example/"
}
EOF
    while [ $# -gt 0 ]; do
        echo " Creating client: $1"
        __check_admin_token
        export __client_name=$1
        envsubst < .jsonfile1 > .jsonfile2
        curl -k -s \
        -X POST \
        -H "Authorization: Bearer ${ADMIN_TOKEN}" \
        -H "Content-Type: application/json" \
        -d @".jsonfile2" \
        "$KC_URL/admin/realms/$__realm/clients" | indent1
        if [ $? -ne 0 ]; then
            echo "Command failed"
            exit 1
        fi
        echo " OK"
        shift
    done
}

__get_client_id() {
    __client_data=$(curl -k -s \
        -X GET \
        -H "Authorization: Bearer ${ADMIN_TOKEN}" \
        "$KC_URL/admin/realms/$1/clients?clientId=$2")
    if [ $? -ne 0 ]; then
        return 1
    fi
    __client_id=$(echo $__client_data |  jq -r '.[0].id')
    echo $__client_id
    return 0
}

generate_client_secrets() {
    __realm=$1
    shift
    echo "Attempt to generate secret for clients $@ in realm $__realm"
    while [ $# -gt 0 ]; do
        __check_admin_token
        __client_id=$(__get_client_id $__realm $1)
        if [ $? -ne 0 ]; then
            echo "Command failed"
            exit 1
        fi
        echo " Client id for client $1 in realm $__realm: "$__client_id | indent1
        echo "  Creating secret"
        __client_secret=$(curl -k -s \
                -X POST \
                -H "Authorization: Bearer ${ADMIN_TOKEN}" \
                "$KC_URL/admin/realms/$__realm/clients/$__client_id/client-secret")
        if [ $? -ne 0 ]; then
            echo "Command failed"
            exit 1
        fi
        __client_secret=$(curl -k -s \
                -X GET \
                -H "Authorization: Bearer ${ADMIN_TOKEN}" \
                "$KC_URL/admin/realms/$__realm/clients/$__client_id/client-secret")
        if [ $? -ne 0 ]; then
            echo "Command failed"
            exit 1
        fi
        __client_secret=$(echo $__client_secret | jq -r .value)
        echo "  Client secret for client $1 in realm $__realm: "$__client_secret | indent1
        echo $__client_secret > ".sec_$__realm""_$1"
        echo "   OK"
        shift
    done
}

create_client_roles() {
    # <realm-name> <client-name> [<role-name>]+
    __check_admin_token
    __client_id=$(__get_client_id $1 $2)
    if [ $? -ne 0 ]; then
        echo "Command failed"
        exit 1
    fi
    __realm=$1
    shift; shift;
    while [ $# -gt 0 ]; do

cat > .jsonfile1 <<- "EOF"
{
   "name":"$__role"
}
EOF
        export __role=$1
        envsubst < .jsonfile1 > .jsonfile2
        curl -k -s \
        -X POST \
        -H "Authorization: Bearer ${ADMIN_TOKEN}" \
        -H "Content-Type: application/json" \
        -d @".jsonfile2" \
        "$KC_URL/admin/realms/$__realm/clients/$__client_id/roles" | indent1
        if [ $? -ne 0 ]; then
            echo "Command failed"
            exit 1
        fi
        shift
    done
}

__get_service_account_id() {
    # <realm-name> <client-id>
    __service_account_data=$(curl -k -s \
        -X GET \
        -H "Authorization: Bearer ${ADMIN_TOKEN}" \
        "$KC_URL/admin/realms/$1/clients/$2/service-account-user")
    if [ $? -ne 0 ]; then
        return 1
    fi
    __service_account_id=$(echo $__service_account_data |  jq -r '.id')
    echo $__service_account_id
    return 0
}

__get_client_available_role_id() {
    # <realm-name> <service-account-id> <client-id> <client-role-name>
    __client_role_data=$(curl -k -s \
        -X GET \
        -H "Authorization: Bearer ${ADMIN_TOKEN}" \
        "$KC_URL/admin/realms/$1/users/$2/role-mappings/clients/$3/available")
    if [ $? -ne 0 ]; then
        return 1
    fi
    #__client_role_id=$(echo $__client_role_data |  jq -r '.id')
    __client_role_id=$(echo $__client_role_data | jq  -r '.[] | select(.name=="'$4'") | .id ')
    echo $__client_role_id
    return 0
}

__get_client_mapped_role_id() {
    # <realm-name> <service-account-id> <client-id> <client-role-name>
    __client_role_data=$(curl -s \
        -X GET \
        -H "Authorization: Bearer ${ADMIN_TOKEN}" \
        "$KC_URL/admin/realms/$1/users/$2/role-mappings/clients/$3")
    if [ $? -ne 0 ]; then
        return 1
    fi
    #__client_role_id=$(echo $__client_role_data |  jq -r '.id')
    __client_role_id=$(echo $__client_role_data | jq  -r '.[] | select(.name=="'$4'") | .id ')
    echo $__client_role_id
    return 0
}

add_client_roles_mapping()  {
    # <realm-name> <client-name> [<role-name>]+
    echo "Attempt to add roles ${@:3} to client $2 in realm $1"
    __check_admin_token
    __realm=$1
    __client=$2
    __client_id=$(__get_client_id $__realm $__client)
    if [ $? -ne 0 ]; then
        echo "Command failed"
        exit 1
    fi
    echo " Client id for client $__client in realm $__realm: "$__client_id | indent1
    __service_account_id=$(__get_service_account_id $__realm $__client_id)
    if [ $? -ne 0 ]; then
        echo "Command failed"
        exit 1
    fi
    echo " Service account id for client $__client in realm $__realm: "$__service_account_id | indent1
    shift; shift
    __cntr=0
    __all_roles=$@
    while [ $# -gt 0 ]; do
        if [ $__cntr -eq 0 ]; then
            echo "[" > .jsonfile2
        fi
        __client_role_id=$(__get_client_available_role_id $__realm $__service_account_id $__client_id $1)
        if [ $? -ne 0 ]; then
            echo "Command failed"
            exit 1
        fi

        __role='{"name":"'$1'","id":"'$__client_role_id'","composite": false,"clientRole": true}'
        if [ $__cntr -gt 0 ]; then
            echo "," >> .jsonfile2
        fi
        echo $__role >> .jsonfile2
        let __cntr=__cntr+1
        shift
    done
    echo "]" >> .jsonfile2
    echo "  Adding roles $__all_roles to client $__client in realm $__realm"

    curl -k -s \
    -X POST \
    -H "Authorization: Bearer ${ADMIN_TOKEN}" \
    -H "Content-Type: application/json" \
    -d @".jsonfile2" \
    "$KC_URL/admin/realms/$__realm/users/$__service_account_id/role-mappings/clients/$__client_id" | indent2
    if [ $? -ne 0 ]; then
        echo "Command failed"
        exit 1
    fi
    echo "  OK"
}



remove_client_roles_mapping()  {
    # <realm-name> <client-name> [<role-name>]+
    echo "Attempt to removed roles ${@:3} from client $2 in realm $1"
    __check_admin_token
    __realm=$1
    __client=$2
    __client_id=$(__get_client_id $__realm $__client)
    if [ $? -ne 0 ]; then
        echo "Command failed"
        exit 1
    fi
    echo " Client id for client $__client in realm $__realm: "$__client_id | indent1
    __service_account_id=$(__get_service_account_id $__realm $__client_id)
    if [ $? -ne 0 ]; then
        echo "Command failed"
        exit 1
    fi
    echo " Service account id for client $__client in realm $__realm: "$__service_account_id | indent1
    shift; shift
    __cntr=0
    __all_roles=$@
    while [ $# -gt 0 ]; do
        if [ $__cntr -eq 0 ]; then
            echo "[" > .jsonfile2
        fi
        __client_role_id=$(__get_client_mapped_role_id $__realm $__service_account_id $__client_id $1)
        if [ $? -ne 0 ]; then
            echo "Command failed"
            exit 1
        fi

        __role='{"name":"'$1'","id":"'$__client_role_id'","composite": false,"clientRole": true}'
        if [ $__cntr -gt 0 ]; then
            echo "," >> .jsonfile2
        fi
        echo $__role >> .jsonfile2
        let __cntr=__cntr+1
        shift
    done
    echo "]" >> .jsonfile2
    echo "  Removing roles $__all_roles from client $__client in realm $__realm"

    curl -k -s \
    -X DELETE \
    -H "Authorization: Bearer ${ADMIN_TOKEN}" \
    -H "Content-Type: application/json" \
    -d @".jsonfile2" \
    "$KC_URL/admin/realms/$__realm/users/$__service_account_id/role-mappings/clients/$__client_id" | indent2
    if [ $? -ne 0 ]; then
        echo "Command failed"
        exit 1
    fi
    echo "  OK"
}

add_client_hardcoded-claim-mapper() {
# <realm-name> <client-name> <mapper-name> <claim-name> <claim-value>
    __check_admin_token
    __realm=$1
    __client=$2
    export __mapper_name=$3
    export __claim_name=$4
    export __claim_value=$5

    __client_id=$(__get_client_id $__realm $__client)
    if [ $? -ne 0 ]; then
        echo " Fatal error when getting client id, response: "$?
        exit 1
    fi
    cat > .jsonfile1 <<- "EOF"
{
    "name": "$__mapper_name",
    "protocol": "openid-connect",
    "protocolMapper": "oidc-hardcoded-claim-mapper",
    "consentRequired": false,
    "config": {
      "claim.value": "$__claim_value",
      "userinfo.token.claim": "true",
      "id.token.claim": "true",
      "access.token.claim": "true",
      "claim.name": "$__claim_name",
      "access.tokenResponse.claim": "false"
    }
}
EOF
    envsubst < .jsonfile1 > .jsonfile2
    curl -k -s \
    -X POST \
    -H "Authorization: Bearer ${ADMIN_TOKEN}" \
    -H "Content-Type: application/json" \
    -d @".jsonfile2" \
    "$KC_URL/admin/realms/nonrtric-realm/clients/"$__client_id"/protocol-mappers/models" | indent2
    if [ $? -ne 0 ]; then
        echo "Command failed"
        exit 1
    fi
    set +x
    cat .jsonfile2
    echo "  OK"
}

# Get a client token
# args: <realm-name> <client-name>
get_client_token() {
    __check_admin_token
    __realm=$1
    __client=$2
    __client_id=$(__get_client_id $__realm $__client)
    if [ $? -ne 0 ]; then
        echo " Fatal error when getting client id, response: "$?
        exit 1
    fi

    __client_secret=$(curl -k -s -f \
            -X GET \
            -H "Authorization: Bearer ${ADMIN_TOKEN}" \
            "$KC_URL/admin/realms/$__realm/clients/$__client_id/client-secret")
    if [ $? -ne 0 ]; then
        echo " Fatal error when getting client secret, response: "$?
        exit 1
    fi

    __client_secret=$(echo $__client_secret | jq -r .value)

	__TMP_TOKEN=$(curl -k -s -f -X POST $KC_URL/realms/$__realm/protocol/openid-connect/token   \
                  -H Content-Type:application/x-www-form-urlencoded \
                  -d client_id="$__client" -d client_secret="$__client_secret" -d grant_type=client_credentials)
	if [ $? -ne 0 ]; then
		echo " Fatal error when getting client token, response: "$?
		exit 1
	fi

	echo $__TMP_TOKEN| jq -r .access_token
	return 0
}
