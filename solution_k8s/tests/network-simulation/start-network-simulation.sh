#!/bin/sh

# Copyright 2022 highstreet technologies
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

dep_dir=o-ran-sc-dep-repo
rm -rf ./$dep_dir
git clone https://gerrit.o-ran-sc.org/r/it/dep.git $dep_dir

helm cm-push -f $dep_dir/smo-install/tests_oom/ru-simulator local
helm cm-push -f $dep_dir/smo-install/tests_oom/du-simulator local

helm repo update

helm install --debug oran-ru-simulator local/ru-simulator -n network --create-namespace -f ru-sim.override.yaml
helm install --debug oran-du-simulator local/du-simulator -n network --create-namespace -f du-sim.override.yaml