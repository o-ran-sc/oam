# Network Topology Parser

This golang project generates a docker-compose.yaml file to be used for simulating the network topology, by parsing the topology JSON file created by the [Network Topology Instance Generator](../network-topology-instance-generator/README.md) tool.

## Prerequisites

The GO runtime should be installed on the machine. Instructions [here](https://go.dev/doc/install).

## Usage

These commands should be run from the folder where this README is located.

``` bash
go build
```

This creates the executable *topology-parser*.

``` bash
./topology-parser <network-topology.json>
```

## Output

The result of running this tool is a **docker-compose.yaml** file that can be then used in the *solution/integration/network* folder, **along with the .env file defined there**, for starting a simulated topology as described in the network-topology.json input file.
