#!/bin/bash
#set -x


echo "Replace variables $(echo -e $vars) in $ENV_FILE"

cat $ENV_FILE_TEMPLATE | envsubst "$(echo -e $vars)" > $ENV_FILE
