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

// TapiContext is a view of the TAPI Context, augmented with TAPI Topology
// https://mholt.github.io/json-to-go/ used to transform the JSON into Go struct
type TapiContext struct {
	TapiCommonContext struct {
		UUID string `json:"uuid"`
		Name []struct {
			ValueName string `json:"value-name"`
			Value     string `json:"value"`
		} `json:"name"`
		TapiTopologyTopologyContext struct {
			Topology []struct {
				UUID string `json:"uuid"`
				Name []struct {
					ValueName string `json:"value-name"`
					Value     string `json:"value"`
				} `json:"name"`
				LayerProtocolName []string `json:"layer-protocol-name"`
				Node              []struct {
					UUID string `json:"uuid"`
					Name []struct {
						ValueName string `json:"value-name"`
						Value     string `json:"value"`
					} `json:"name"`
					OwnedNodeEdgePoint []struct {
						UUID string `json:"uuid"`
						Name []struct {
							ValueName string `json:"value-name"`
							Value     string `json:"value"`
						} `json:"name"`
						AdministrativeState                string   `json:"administrative-state"`
						OperationalState                   string   `json:"operational-state"`
						LifecycleState                     string   `json:"lifecycle-state"`
						LinkPortRole                       string   `json:"link-port-role"`
						LayerProtocolName                  string   `json:"layer-protocol-name"`
						SupportedCepLayerProtocolQualifier []string `json:"supported-cep-layer-protocol-qualifier"`
						LinkPortDirection                  string   `json:"link-port-direction"`
						TerminationState                   string   `json:"termination-state"`
						TerminationDirection               string   `json:"termination-direction"`
					} `json:"owned-node-edge-point"`
					AdministrativeState string   `json:"administrative-state"`
					OperationalState    string   `json:"operational-state"`
					LifecycleState      string   `json:"lifecycle-state"`
					LayerProtocolName   []string `json:"layer-protocol-name"`
					CostCharacteristic  []struct {
						CostName      string `json:"cost-name"`
						CostAlgorithm string `json:"cost-algorithm"`
						CostValue     string `json:"cost-value"`
					} `json:"cost-characteristic"`
					LatencyCharacteristic []struct {
						TrafficPropertyName         string `json:"traffic-property-name"`
						QueingLatencyCharacteristic string `json:"queing-latency-characteristic"`
						FixedLatencyCharacteristic  string `json:"fixed-latency-characteristic"`
						JitterCharacteristic        string `json:"jitter-characteristic"`
						WanderCharacteristic        string `json:"wander-characteristic"`
					} `json:"latency-characteristic"`
					ORanScTopologyFunction    string `json:"o-ran-sc-topology:function"`
					ORanScTopologyGeolocation struct {
						Longitude string `json:"longitude"`
						Latitude  string `json:"latitude"`
						Altitude  string `json:"altitude"`
					} `json:"o-ran-sc-topology:geolocation"`
				} `json:"node"`
				Link []struct {
					UUID string `json:"uuid"`
					Name []struct {
						ValueName string `json:"value-name"`
						Value     string `json:"value"`
					} `json:"name"`
					TransitionedLayerProtocolName []string `json:"transitioned-layer-protocol-name"`
					AdministrativeState           string   `json:"administrative-state"`
					OperationalState              string   `json:"operational-state"`
					Direction                     string   `json:"direction"`
					LifecycleState                string   `json:"lifecycle-state"`
					NodeEdgePoint                 []struct {
						TopologyUUID      string `json:"topology-uuid"`
						NodeUUID          string `json:"node-uuid"`
						NodeEdgePointUUID string `json:"node-edge-point-uuid"`
					} `json:"node-edge-point"`
					LatencyCharacteristic []struct {
						TrafficPropertyName         string `json:"traffic-property-name"`
						QueingLatencyCharacteristic string `json:"queing-latency-characteristic"`
						FixedLatencyCharacteristic  string `json:"fixed-latency-characteristic"`
						JitterCharacteristic        string `json:"jitter-characteristic"`
						WanderCharacteristic        string `json:"wander-characteristic"`
					} `json:"latency-characteristic"`
					LayerProtocolName  []string `json:"layer-protocol-name"`
					RiskCharacteristic []struct {
						RiskCharacteristicName string   `json:"risk-characteristic-name"`
						RiskIdentifierList     []string `json:"risk-identifier-list"`
					} `json:"risk-characteristic"`
					ValidationMechanism []struct {
						ValidationMechanism             string `json:"validation-mechanism"`
						ValidationRobustness            string `json:"validation-robustness"`
						LayerProtocolAdjacencyValidated string `json:"layer-protocol-adjacency-validated"`
					} `json:"validation-mechanism"`
					CostCharacteristic []struct {
						CostName      string `json:"cost-name"`
						CostAlgorithm string `json:"cost-algorithm"`
						CostValue     string `json:"cost-value"`
					} `json:"cost-characteristic"`
				} `json:"link"`
			} `json:"topology"`
		} `json:"tapi-topology:topology-context"`
	} `json:"tapi-common:context"`
}
