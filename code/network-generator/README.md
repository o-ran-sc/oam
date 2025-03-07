# Network Generator

This projects generates a view of a telecommunication network composed of RAN,
Transport, 5G-Core, O-Cloud and SMO functions associated with the O-RAN 
Alliance architecture. 

Please note that a single 5G frequency represents a single sector, represents
a single NRCellDU, represents a single O-RU, represents a single O-DU.

Each sector/cell covers an angle of 120° where the tower is represented by the
center of a hexagon. 3 sectors/cells cover with azimuths [0°,120°,240°] cover
an area around the tower. O-RUs are mounted add the tower. O-DUs are located in
data center (o-cloud resource pool). 

## Prerequisites

```
$ cat /etc/os-release | grep -oP 'PRETTY_NAME="\K[^"]+'
Ubuntu 22.04.3 LTS

$ python3 --version
Python 3.10.12
```

For validation purposes libyang is recommended.
Please follow the libyang [installation instructions](https://github.com/CESNET/libyang).

## Installation

```
make virtual_env_4_oam
source .oam/bin/activate

pip install -r requirements.txt 
pip install -r requirements-test.txt 
```


## Usage 

```
make virtual_env_4_oam
source .oam/bin/activate

python3 -m network_generation config.json
```

## Output

By default the generated files can be found in the 'output' folder:

- [o-ran-network-operational.json](output/o-ran-network-operational.json)
- [o-ran-network.svg](output/o-ran-network.svg)
- [o-ran-network.kml](output/o-ran-network.kml)

## yang validation

```
pyang --lint \
-p network_generation/model/yang \
network_generation/model/yang/o-ran-sc-*.yang
```

```
yanglint \
-p network_generation/model/yang \
network_generation/model/yang/o-ran-sc-*.yang
```

## Output validation

```
yanglint \
network_generation/model/yang/ietf-network.yang \
network_generation/model/yang/ietf-network-topology.yang \
network_generation/model/yang/o-ran-common-identity-refs.yang \
network_generation/model/yang/o-ran-sc-network.yang \
\
output/o-ran-network-operational.json 
```

## Development

Read the [CONTRIBUTING.md](CONTRIBUTING.md) file.
