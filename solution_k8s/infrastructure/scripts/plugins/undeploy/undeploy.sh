#!/bin/sh

# Copyright 2024 highstreet technologies
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

usage() {
cat << EOF
Delete an umbrella Helm Chart, and its subcharts, that was previously deployed using 'Helm deploy'.

Example of deleting all Releases that have the prefix 'demo'.
  $ helm undeploy demo

  $ helm undeploy demo --purge

Usage:
  helm undeploy [RELEASE] [flags]

Flags:
      --purge     remove the releases from the store and make its name free for later use
EOF
}

undeploy() {
  RELEASE=$1
  FLAGS=$2

  reverse_list=
  for item in $(helm ls -q --all | grep $RELEASE)
  do
    reverse_list="$item $reverse_list"
  done
  for item in $reverse_list
  do
    helm del $item $FLAGS
  done
}

if [ -z "$1" ]; then
  echo "Error: command 'undeploy' requires a release name"
  exit 1
fi

case "${1:-"help"}" in
  "help")
    usage
    ;;
  "--help")
    usage
    ;;
  "-h")
    usage
    ;;
  *)
    undeploy $1 $(echo ${@} | sed 's/^ *[^ ]* *//')
    ;;
esac

exit 0
