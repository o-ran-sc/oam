#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# Function to display usage information
usage() {
    echo "Usage: "
    echo "Start solution with out certificates:  $0 "
    echo "With certificates: $0 --cert <certificate_file> --key <key_file>"
    echo "  --cert    Path to the certificate file."
    echo "  --key     Path to the private key file."
    exit 1
}

deploy(){
    if [ -z "$1" ]; then
        docker compose -f $SCRIPT_DIR/smo/common/docker-compose.yaml up -d --wait
    else 
        docker compose -f $SCRIPT_DIR/smo/common/docker-compose.yaml -f $SCRIPT_DIR/smo/common/docker-compose-gateway-cert.override.yaml up -d --wait
    fi
    python3 create_users.py $SCRIPT_DIR/users.csv -o $SCRIPT_DIR/smo/common/identity/authentication.json
    python3 $SCRIPT_DIR/smo/common/identity/config.py
    docker compose -f $SCRIPT_DIR/smo/oam/docker-compose.yaml up -d
}

# Parse parameters
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --cert) CERT_FILE="$2"; shift ;;
        --key) KEY_FILE="$2"; shift ;;
        --help) usage; exit 0;;
        *) echo "Start solution without external certificates...";;
    esac
    shift
done



# Validate that both --cert and --key were provided
if [ -z "$CERT_FILE" ] && [ -z "$KEY_FILE" ]; then
    deploy
    
else
    # Check if the certificate file exists
    if [ -f "$CERT_FILE" ]; then
        echo "Certificate file found: $CERT_FILE"
        cp -f $CERT_FILE $SCRIPT_DIR/smo/common/gateway/certs/mydomain_cert.pem
    else
        echo "Error: Certificate file not found at $CERT_FILE"
        exit 1
    fi
    
    # Check if the key file exists
    if [ -f "$KEY_FILE" ]; then
        echo "Key file found: $KEY_FILE"
        cp -f $KEY_FILE $SCRIPT_DIR/smo/common/gateway/certs/mydomain_key.pem
    else
        echo "Error: Key file not found at $KEY_FILE"
        exit 1
    fi
    deploy "cert"
fi




