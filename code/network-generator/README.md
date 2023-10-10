# Network Generator

This projects generates a view of a telecommunication network composed of RAN,
Transport, 5G-Core, O-Cloud and SMO functions associated with the O-RAN 
Alliance architecture. 

Please note that a single 5G frequency represents a single sector, represents
a single NRCellDU, represents a single O-RU, represents a single O-DU.

Each sector/cell covers an angel of 120° where the tower is represented by the
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

## Usage 

```
python3 network_generator.py config.json
```

## Output

By default the generated files can be found in the 'output' folder:

- [network.json](output/network.json)
- [network.svg](output/network.svg)
- [network.kml](output/network.kml)
