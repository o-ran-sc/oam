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

// Config is the entire docker-compose YAML object
type Config struct {
    Version  string
    CommonEnvs map[string]string `yaml:"x-common_env,anchor=common_env"`
    DuEnv map[string]string `yaml:"x-du_env,anchor=du_env"`
    RuEnv map[string]string `yaml:"x-ru_env,anchor=ru_env"`
    TopoEnv map[string]string `yaml:"x-topo_env,anchor=topo_env"`
    CommonNfs CommonNf `yaml:"x-nf,anchor=common_nf"`
    Networks map[string]Network
    Volumes  map[string]Volume `yaml:",omitempty"`
    Services map[string]Service
}

// CommonNf is the common network function alias
type CommonNf struct {
    StopGracePeriod     string `yaml:"stop_grace_period"`
    CapAdd              []string `yaml:"cap_add"`
}

// Network is the network YAML object
type Network struct {
    Driver          string `yaml:",omitempty"`
    DriverOpts      map[string]string `yaml:"driver_opts,omitempty"`
    External        map[string]string `yaml:",omitempty"`
}

// Volume is the volume YAML object
type Volume struct {
    Driver, External string
    DriverOpts       map[string]string `yaml:"driver_opts"`
}

// Service is the service YAML object
type Service struct {
    *Service `yaml:",inline,alias=common_nf"`
    ContainerName                     string `yaml:"container_name"`
    Image                             string
    Networks, Ports, Volumes, Command, Links []string `yaml:",omitempty"`
    VolumesFrom                       []string `yaml:"volumes_from,omitempty"`
    DependsOn                         []string `yaml:"depends_on,omitempty"`
    CapAdd                            []string `yaml:"cap_add,omitempty"`
    Build                             struct{ Context, Dockerfile string } `yaml:",omitempty"`
    Environment                       Env `yaml:"environment"`
    Hostname                          string
}

// Env is the environment YAML object
type Env struct {
    *CommonEnv `yaml:",omitempty,inline,alias=common_env"`
    *DuEnv `yaml:",omitempty,inline,alias=du_env"`
    *RuEnv `yaml:",omitempty,inline,alias=ru_env"`
    *TopoEnv `yaml:",omitempty,inline,alias=topo_env"`
}

// CommonEnv is the common_env anchor
type CommonEnv struct {
    *CommonEnv `yaml:",omitempty,inline,alias=common_env"`
}

// DuEnv is the du_env anchor
type DuEnv struct {
    *DuEnv `yaml:",omitempty,inline,alias=du_env"`
}

// RuEnv is the ru_env anchor
type RuEnv struct {
    *RuEnv `yaml:",omitempty,inline,alias=ru_env"`
}

// TopoEnv is the topo_env anchor
type TopoEnv struct {
    *TopoEnv `yaml:",omitempty,inline,alias=topo_env"`
}
