# Service Management and Orchestration (SMO) on single node k8s 

## Introduction

A tailored ONAP application is deployed on a single node kubernetes cluster.
A metric stack contains influxdb and grafana dashboard to visualize performance data provided by 3GPP ftp files from network devices.
A test network function deployment ensures function of netconf call-home and O1 interface.

## Documentation

### Directory Structure

```
.
├── README.md       This README.md
├── application     Deployment directory for SMO
├── infrastructure  Deployment directory for kubernetes infrastructure
├── makefile        file to deploy or undeploy components
├── metrics         Deployment directory for metric stack
├── tests           Deployment directory for simulated network functions
└── .env            Common environment variables for deployments
```

### Installation

#### Prerquiesites
This setup requires (and is verified with) ubuntu 22.04.
VM or baremetal server should fullfill (less ressources could work as well)
- 4 (better 8) vCPU
- 20 (better 32) GB RAM
- 50GB HDD

Passwordless sudo access is required

Please verify if sudo can be executed passwordless.
otherwise add this file and replace <youruser> with your username:
```
sudo vi /etc/sudoers.d/20-kubeone-user
# Created for kubeone passwordless sudo

# User rules for <youruser>
<youruser> ALL=(ALL) NOPASSWD:ALL

```

Install make tool
```
sudo apt install make
```
Install other prerequisites
```
make install-prereqisites
```

Modify variables in .env file
Apply templates for kubernetes and Application deployment
```
# internal IP is the IP, which is assigned to the network interface.
# external IP is the IP, which is used from outside the VM, e.g. floating IP in openstack
# in common cases this is equal to internal IP
# FQDN is the DNS resolvable adress of the VM
make prepare-templates
```
This creates infrastructure/kubeone.yaml and override files for helm deployments


#### Kubernetes
This step creates a single node kubernetes cluster with kubeone.
If a different kubernetes setup is used, please ensure kubectl is working without any additional parameters

- Create kubernetes cluster
```
make create-infrastructure
```

- verify if cluster is accessable
```
kubectl get nodes
NAME                                 STATUS   ROLES           AGE    VERSION
o-ran-sc-oam-cluster   Ready    control-plane   3m6s   v1.28.6
```


- To remove the cluster from the machine use

```
make destroy-infrastructure
```

In case of issues please check more details in infastructure/README.md

#### SMO

- Deploy SMO application stack

```
make deploy-smo
```

- Un-deploy SMO application stack

```
make undeploy-smo
```

#### Metric Stack

Deploy metric stack to visualize PM data provided by networkfunctions via O1 fileready notification.
- pm-microservice to consume 3GPP pm data from kafka and fill into influxdb
- influxdb
- grafana

```
make deploy-metric
```

undeploy

```
make undeploy-metric
```

#### Network Simulation

For verification purposes two networkfunctions can be deployed
- O-DU    connected via pnf registration request to ves-collector
- O-RU    connectect via call home to controller

```
make deploy-test-nfs
```

remove simulation

```
make undeploy-test-nfs
```

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.
