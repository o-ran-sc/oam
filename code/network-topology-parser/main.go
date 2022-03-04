/************************************************************************
* Copyright 2022 highstreet technologies GmbH
*
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
*
*     http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
************************************************************************/

package main

import (
	"encoding/json"
	"errors"
	"fmt"
	"io/ioutil"
	"os"

	"github.com/goccy/go-yaml"
)

var configYAML Config

// common parts consist of the anchors that are reused for the services
func createCommonParts() {
	configYAML.Version = "3.8"

	configYAML.CommonEnvs = make(map[string]string, 1)

	configYAML.CommonEnvs["IPv6_ENABLED"] = "${IPv6_ENABLED}"
	configYAML.CommonEnvs["SSH_CONNECTIONS"] = "${SSH_CONNECTIONS}"
	configYAML.CommonEnvs["TLS_CONNECTIONS"] = "${TLS_CONNECTIONS}"
	configYAML.CommonEnvs["NTS_NF_MOUNT_POINT_ADDRESSING_METHOD"] = "${NTS_NF_MOUNT_POINT_ADDRESSING_METHOD}"
	configYAML.CommonEnvs["NTS_HOST_IP"] = "${NTS_HOST_IP}"
	configYAML.CommonEnvs["NTS_HOST_BASE_PORT"] = "${NTS_HOST_BASE_PORT}"
	configYAML.CommonEnvs["NTS_HOST_NETCONF_SSH_BASE_PORT"] = "${NTS_HOST_NETCONF_SSH_BASE_PORT}"
	configYAML.CommonEnvs["NTS_HOST_NETCONF_TLS_BASE_PORT"] = "${NTS_HOST_NETCONF_TLS_BASE_PORT}"
	configYAML.CommonEnvs["NTS_HOST_TRANSFER_FTP_BASE_PORT"] = "${NTS_HOST_TRANSFER_FTP_BASE_PORT}"
	configYAML.CommonEnvs["NTS_HOST_TRANSFER_SFTP_BASE_PORT"] = "${NTS_HOST_TRANSFER_SFTP_BASE_PORT}"
	configYAML.CommonEnvs["SDN_CONTROLLER_PROTOCOL"] = "${SDN_CONTROLLER_PROTOCOL}"
	configYAML.CommonEnvs["SDN_CONTROLLER_IP"] = "${SDNC_OAM_IPv6}"
	configYAML.CommonEnvs["SDN_CONTROLLER_PORT"] = "${SDNC_REST_PORT}"
	configYAML.CommonEnvs["SDN_CONTROLLER_CALLHOME_IP"] = "${SDNC_OAM_IPv6}"
	configYAML.CommonEnvs["SDN_CONTROLLER_CALLHOME_PORT"] = "${SDN_CONTROLLER_CALLHOME_PORT}"
	configYAML.CommonEnvs["SDN_CONTROLLER_USERNAME"] = "${ADMIN_USERNAME}"
	configYAML.CommonEnvs["SDN_CONTROLLER_PASSWORD"] = "${ADMIN_PASSWORD}"
	configYAML.CommonEnvs["VES_COMMON_HEADER_VERSION"] = "${VES_COMMON_HEADER_VERSION}"
	configYAML.CommonEnvs["VES_ENDPOINT_PROTOCOL"] = "${VES_ENDPOINT_PROTOCOL}"
	configYAML.CommonEnvs["VES_ENDPOINT_IP"] = "${VES_COLLECTOR_OAM_IPv6}"
	configYAML.CommonEnvs["VES_ENDPOINT_PORT"] = "${VES_ENDPOINT_PORT}"
	configYAML.CommonEnvs["VES_ENDPOINT_AUTH_METHOD"] = "${VES_ENDPOINT_AUTH_METHOD}"
	configYAML.CommonEnvs["VES_ENDPOINT_USERNAME"] = "${VES_ENDPOINT_USERNAME}"
	configYAML.CommonEnvs["VES_ENDPOINT_PASSWORD"] = "${VES_ENDPOINT_PASSWORD}"

	configYAML.DuEnv = make(map[string]string, 1)
	configYAML.DuEnv["NTS_NF_STANDALONE_START_FEATURES"] = "datastore-populate ves-heartbeat ves-file-ready ves-pnf-registration web-cut-through"

	configYAML.RuEnv = make(map[string]string, 1)
	configYAML.RuEnv["NTS_NF_STANDALONE_START_FEATURES"] = "datastore-populate netconf-call-home web-cut-through"

	configYAML.TopoEnv = make(map[string]string, 1)
	configYAML.TopoEnv["NTS_NF_STANDALONE_START_FEATURES"] = "datastore-populate netconf-call-home web-cut-through"

	var commonNf CommonNf
	commonNf.StopGracePeriod = "5m"
	commonNf.CapAdd = append(commonNf.CapAdd, "SYS_ADMIN")
	commonNf.CapAdd = append(commonNf.CapAdd, "SYS_PTRACE")
	configYAML.CommonNfs = commonNf
}

// creates the network information to be used by the services
func createNetwork() {
	configYAML.Networks = make(map[string]Network, 1)
	defaultNetwork := configYAML.Networks["default"]

	defaultNetwork.External = make(map[string]string, 1)
	defaultNetwork.External["name"] = "oam"

	configYAML.Networks["default"] = defaultNetwork
}

// creates an O-RU simulator instance as a service
func addORUasService(name string) {
	service := configYAML.Services[name]

	service.Image = "${NEXUS3_DOCKER_REPO}nts-ng-o-ran-ru-fh:${NTS_BUILD_VERSION}"
	service.ContainerName = "ntsim-ng-" + name
	service.Hostname = name

	commonEnv := &CommonEnv{}
	ruEnv := &RuEnv{}
	env := &Env{commonEnv, nil, ruEnv, nil}
	service.Environment = *env

	configYAML.Services[name] = service
}

// creates an O-DU simulator instance as a service
func addODUasService(name string) {
	service := configYAML.Services[name]

	service.Image = "${NEXUS3_DOCKER_REPO}nts-ng-o-ran-du:${NTS_BUILD_VERSION}"
	service.ContainerName = "ntsim-ng-" + name
	service.Hostname = name

	commonEnv := &CommonEnv{}
	duEnv := &DuEnv{}
	env := &Env{commonEnv, duEnv, nil, nil}
	service.Environment = *env

	configYAML.Services[name] = service
}

// iterates through the topology and creates associated services
func createServices(topologyJSON *TapiContext) {
	topology := topologyJSON.TapiCommonContext.TapiTopologyTopologyContext.Topology[0]

	configYAML.Services = make(map[string]Service, 1)

	for _, node := range topology.Node {
		if node.ORanScTopologyFunction == "o-ran-sc-topology-common:o-ru" {
			name := getNodeNameFromUUID(node.UUID, topologyJSON)
			addORUasService(name)
		} else if node.ORanScTopologyFunction == "o-ran-sc-topology-common:o-du" {
			name := getNodeNameFromUUID(node.UUID, topologyJSON)
			addODUasService(name)
		}
	}
}

// returns the type of O-RAN-SC Topology Function of the input TAPI Node
func getTypeOfNodeUUID(nodeUUID string, topologyJSON *TapiContext) string {
	topology := topologyJSON.TapiCommonContext.TapiTopologyTopologyContext.Topology[0]

	for _, node := range topology.Node {
		if node.UUID == nodeUUID {
			return node.ORanScTopologyFunction
		}
	}

	return ""
}

// returns the Node Name of the TAPI Node with the input UUID
func getNodeNameFromUUID(searchedUUID string, topologyJSON *TapiContext) string {
	topology := topologyJSON.TapiCommonContext.TapiTopologyTopologyContext.Topology[0]

	for _, node := range topology.Node {
		if node.UUID == searchedUUID {
			for _, name := range node.Name {
				if name.ValueName == "topology-node-name" {
					return name.Value
				}
			}
		}
	}

	return ""
}

func main() {
	if len(os.Args) > 1 {
		fmt.Printf("Parsing file %v...\n", os.Args[1])
	} else {
		fmt.Printf("Usage: %v <input>\nwhere input is the topology filename in JSON format.\n", os.Args[0])
		os.Exit(0)
	}

	if _, err := os.Stat(os.Args[1]); errors.Is(err, os.ErrNotExist) {
		fmt.Printf("File %v does not exist!\n", os.Args[1])
		os.Exit(1)
	}

	topoJSONFile, err := os.Open(os.Args[1])
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
	defer topoJSONFile.Close()

	byteValue, _ := ioutil.ReadAll(topoJSONFile)

	var topologyObject TapiContext
	err = json.Unmarshal(byteValue, &topologyObject)
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}

	if len(topologyObject.TapiCommonContext.TapiTopologyTopologyContext.Topology) < 1 {
		fmt.Println("Could not find TAPI Topology object in the loaded JSON!")
		os.Exit(1)
	}

	createCommonParts()
	createNetwork()
	createServices(&topologyObject)

	yamlData, err := yaml.Marshal(&configYAML)
	if err != nil {
		fmt.Println(err)
	}

	fileName := "docker-compose.yaml"
	err = ioutil.WriteFile(fileName, yamlData, 0644)
	if err != nil {
		fmt.Println(err)
	}

	fmt.Println("File docker-compose.yaml created successfully!")
}
