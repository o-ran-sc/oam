#!/bin/bash
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cat $SCRIPT_DIR/append_to_etc_hosts.txt >> /etc/hosts
cat /etc/hosts