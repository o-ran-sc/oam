# *******************************************************************************
# * ============LICENSE_START========================================================================
# * Copyright (C) 2024 highstreet technologies GmbH Intellectual Property. All rights reserved.
# * =================================================================================================
# * Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
# * in compliance with the License. You may obtain a copy of the License at
# *
# * http://www.apache.org/licenses/LICENSE-2.0
# *
# * Unless required by applicable law or agreed to in writing, software distributed under the License
# * is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
# * or implied. See the License for the specific language governing permissions and limitations under
# * the License.
# * ============LICENSE_END==========================================================================

# Top level makefile to build all

## help:                Show the help.
.PHONY: help
help:
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@fgrep "##" Makefile | fgrep -v fgrep | sed 's/##/ -/g'

## install-prereqisites: Create kubernetes all-in one infrastructure
.PHONY: install-prereqisites
install-prereqisites:
	(cd infrastructure; ./install_prerequisites.sh)
	(cd infrastructure/scripts; ./install-kubeone.sh; ./create_key_kubeone.sh)
	(cd infrastructure/scripts; ./install_helm.sh)
	
## prepare-templates: fills templates (k8s, application and metrics) with machine specific parameters
.PHONY: prepare-templates
prepare-templates:
	# for k8s/kubeone
	(cd infrastructure/scripts/; ./setup-k8s-cluster-template.sh)
	# for metrics and smo stack
	(cd application; ./setup-smo-template.sh)
	


## create-infrastructure: Create kubernetes all-in one infrastructure
.PHONY: create-infrastructure
create-infrastructure:
# TODO: create kubeone.yaml from template file
    
	(cd infrastructure; kubeone apply -m kubeone.yaml)
	(cd infrastructure; mkdir -p ~/.kube; cp o-ran-sc-test-cluster-kubeconfig ~/.kube/config)
	kubectl wait --for=condition=ready node -l node-role.kubernetes.io/control-plane=
	echo "wait k8s cluster operable 60s"
	sleep 60
	(cd infrastructure; kubectl apply -f certs/selfsigned-cluster-issuer.yaml)
	(cd infrastructure/scripts; ./install-kafka-strimzi.sh)
	(cd infrastructure/scripts; ./install-mariadb-operator.sh)


## destroy-infrastructure: Destroys kubernetes all-in-one infrastructure
.PHONY: destroy-infrastructure
destroy-infrastructure:
	(cd infrastructure; kubeone reset)


## deploy-smo: Deploys SMO tailered for O-RAN-SC
.PHONY: deploy-smo
deploy-smo:
	(cd application; sudo mkdir -p /dockerdata-nfs/onap/mariadb/; sudo chmod 777 /dockerdata-nfs/onap/mariadb/; kubectl apply -f maria-db-pv.yaml)
	kubectl patch pv onap-mariadb -p '{"spec":{"claimRef": null}}'
	(cd application; ./deploy_smo_from_repo.sh)
	kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=sdnc-web --timeout 1800s --namespace onap
	(cd application;  ./patch-pmbulk.sh)

## undeploy-smo: Un-Deploys SMO 
.PHONY: undeploy-smo
undeploy-smo:
	helm undeploy onap -n onap
	for topic in $$(kubectl get kafkatopic -n onap -o name); do   kubectl patch $$topic -n onap --type=json -p '[{"op": "remove", "path": "/metadata/finalizers"}]'; done
	kubectl delete ns onap
	sudo rm -rf /dockerdata-nfs/onap
	
## deploy-metric: Deploys grafana and influxdb for PM data
.PHONY: deploy-metric
deploy-metric:
	(cd metrics; ./deploy-metric-stack.sh )
	(cd metrics; ./deploy-pm-ms.sh )

## undeploy-metric: Deploys grafana and influxdb for PM data
.PHONY: undeploy-metric
undeploy-metric:
	(cd metrics; ./undeploy-metric-stack.sh )
	helm uninstall -n metric pm-metric-service

## deploy-test-nfs: Deploys test network functions
.PHONY: deploy-test-nfs
deploy-test-nfs:
	(cd tests/network-simulation; ./start-network-simulation.sh )

## undeploy-test-nfs: un-deploys test network functions
.PHONY: undeploy-test-nfs
undeploy-test-nfs:
	(cd tests/network-simulation; ./stop-network-simulation.sh )





	



