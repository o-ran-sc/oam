#!/bin/bash

check_error() {
    if [ $1 -ne 0 ]; then
        echo "Failed $2"
        echo -e "${RED}Exiting...${RESET}"
        exit 1
    fi
}

populate_keycloak() {
# Create realm in keycloak
    . scripts/populate_keycloak.sh

    create_realms nonrtric-realm
    while [ $? -ne 0 ]; do
        create_realms nonrtric-realm
    done

    # Create client for admin calls
    cid="console-setup"
    create_clients nonrtric-realm $cid
    check_error $?
    generate_client_secrets nonrtric-realm $cid
    check_error $?

    echo ""

    cid="console-setup"
    __get_admin_token
    TOKEN=$(get_client_token nonrtric-realm $cid)

    cid="kafka-producer-pm-xml2json"
    create_clients nonrtric-realm $cid
    check_error $?
    generate_client_secrets nonrtric-realm $cid
    check_error $?

    export XML2JSON_CLIENT_SECRET=$(< .sec_nonrtric-realm_$cid)

    cid="pm-producer-json2kafka"
    create_clients nonrtric-realm $cid
    check_error $?
    generate_client_secrets nonrtric-realm $cid
    check_error $?

    export JSON2KAFKA_CLIENT_SECRET=$(< .sec_nonrtric-realm_$cid)

    cid="dfc"
    create_clients nonrtric-realm $cid
    check_error $?
    generate_client_secrets nonrtric-realm $cid
    check_error $?

    export DFC_CLIENT_SECRET=$(< .sec_nonrtric-realm_$cid)

    cid="nrt-pm-log"
    create_clients nonrtric-realm $cid
    check_error $?
    generate_client_secrets nonrtric-realm $cid
    check_error $?

    export PMLOG_CLIENT_SECRET=$(< .sec_nonrtric-realm_$cid)
}

setup_pm() {
    chmod 666 config/pmpr/token-cache/jwt.txt
    envsubst < docker-compose.yaml > docker-compose_gen.yaml
    docker compose -p pm -f docker-compose_gen.yaml up -d
}

setup_influx() {
    data_dir=./config/influxdb2/data
    mkdir -p $data_dir
    envsubst < docker-compose-influxdb.yaml > docker-compose-influxdb_gen.yaml
    docker compose -p influx -f docker-compose-influxdb_gen.yaml up -d
}

create_topics() {
echo "Creating topics: $TOPICS, may take a while ..."            
for t in $TOPICS; do
    retcode=1
    rt=43200000
    echo "Creating topic $t with retention $(($rt/1000)) seconds"
    while [ $retcode -ne 0 ]; do
        result=$(docker exec -it kafka ./bin/kafka-topics.sh \
		--create --topic $t --config retention.ms=$rt  --bootstrap-server kafka:9092)
        retcode=$?
        if [[ "$result" = *"already exists"* ]]; then
            echo -e "${YELLOW}WARN: Topic - $t - already exists${RESET}"
            retcode=0 #avoid the infinite while loop
        fi
    done
done
}

create_docker_networks() {
echo "Creating Docker Netowrks: $DNETWORKS"
for net in $DNETWORKS; do
    docker network inspect $net 2> /dev/null 1> /dev/null
    if [ $? -ne 0 ]; then
        docker network create $net
    else
        echo "  Network: $net exits"
    fi
done
}

#MAIN
RED="\e[31m"
YELLOW="\e[33m"
RESET="\e[0m"

export $(grep -v '^#' .env | xargs -d '\n')
export KAFKA_NUM_PARTITIONS=10
export TOPICS="file-ready collected-file json-file-ready-kp json-file-ready-kpadp pmreports"
export DNETWORKS="oam smo dmz"

create_docker_networks
populate_keycloak
create_topics
scripts/clean-shared-volume.sh
. scripts/get_influxdb2_token.sh
setup_influx
check_error $?

# Wait for influxdb2 to start
echo 'Waiting for influxdb2 to be ready'
until [ $(curl -s -w '%{http_code}' -o /dev/null 'http://localhost:8086/health') -eq 200 ];
do
        echo -n '.'
        sleep 1
done
echo ""

export INFLUXDB2_INSTANCE=influxdb2

INFLUXDB2_TOKEN=$(get_influxdb2_token $INFLUXDB2_INSTANCE)
echo $INFLUXDB2_TOKEN
export INFLUXDB2_TOKEN

setup_pm
check_error $?
            