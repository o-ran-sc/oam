# Application Deployment


## Baremetal kubernetes

Assuming all steps for kubernetes setup on baremetal are done [see: infrastructure-kubernetes-baremetal](../infrastructure/README.md)

```
cd application

```
## SMO deployment

### Customize SMO deplyoment

Modify `override/onap-override-o-ran-sc-<version>.yaml` parameters according your need

| Parameter | Value | Description |
| --------- | ------- | ---------|
| global.masterPassword | secretpassword | password used for craeting all subsequent secrets |
| global.ingress.virtualhost.baseurl | o-ran-sc.org | DNS entry for SMO cluster |

# pull policy

### Deploy SMO
```
# prepare local persistent volume for mariaDB
sudo mkdir -p /dockerdata-nfs/onap/mariadb/
sudo chmod 777 /dockerdata-nfs/onap/mariadb/ 
kubectl apply -f maria-db-pv.yaml
# deploy SMO
./deploy_smo_from_repo.sh
```
### Deploymant Verification

Verify helm deployment status:
```
helm ls -n onap
NAME                    NAMESPACE       REVISION        UPDATED                                 STATUS          CHART                           APP VERSION
onap                    onap            1               2024-09-26 17:16:33.902042754 +0000 UTC deployed        onap-14.0.0                     NewDelhi
onap-dcaegen2-services  onap            1               2024-09-26 17:17:46.03142037 +0000 UTC  deployed        dcaegen2-services-13.1.0        NewDelhi
onap-dmaap              onap            1               2024-09-26 17:17:58.075993391 +0000 UTC deployed        dmaap-13.0.0
onap-mariadb-galera     onap            1               2024-09-26 17:17:42.264588891 +0000 UTC deployed        mariadb-galera-13.2.0
onap-platform           onap            1               2024-09-26 17:18:06.099689176 +0000 UTC deployed        platform-13.0.1
onap-repository-wrapper onap            1               2024-09-26 17:18:07.469923814 +0000 UTC deployed        repository-wrapper-13.0.0
onap-robot              onap            1               2024-09-26 17:18:08.121495948 +0000 UTC deployed        robot-13.0.0
onap-roles-wrapper      onap            1               2024-09-26 17:18:09.500333995 +0000 UTC deployed        roles-wrapper-13.0.0
onap-sdnc               onap            1               2024-09-26 17:18:10.447261484 +0000 UTC deployed        sdnc-14.0.0
onap-strimzi            onap            2               2024-09-26 17:17:41.072480835 +0000 UTC deployed        strimzi-13.0.1


```
Verify status of all pods
```
kubectl get pods -n onap
NAME                                            READY   STATUS      RESTARTS   AGE
mariadb-galera-0                                1/1     Running     0          13h
onap-chartmuseum-7bc565d46-xkj9q                1/1     Running     0          13h
onap-dcae-datafile-collector-54fb56f757-2p2dg   1/1     Running     0          13h
onap-dcae-ms-healthcheck-d7cf866bb-6cfjg        1/1     Running     0          13h
onap-dcae-pm-mapper-9f5b6fc74-b6gm2             1/1     Running     0          13h
onap-dcae-ves-collector-5f57dcb588-2dbjr        1/1     Running     0          13h
onap-dcae-ves-mapper-5dcc6dd778-2g8gp           1/1     Running     0          13h
onap-dmaap-dr-mariadb-init-config-job-knkt9     0/1     Completed   0          13h
onap-dmaap-dr-node-0                            1/1     Running     0          13h
onap-dmaap-dr-prov-66bf788f8-f4snl              1/1     Running     0          13h
onap-message-router-0                           2/2     Running     0          13h
onap-robot-5c748c57d9-xsngd                     1/1     Running     0          13h
onap-sdnc-0                                     1/1     Running     0          13h
onap-sdnc-sdnrdb-init-job-m8jx6                 0/1     Completed   0          13h
onap-sdnc-web-6cf9547dbd-8ns45                  1/1     Running     0          13h
onap-strimzi-entity-operator-5b46c475d4-f57sv   2/2     Running     0          13h
onap-strimzi-kafka-0                            1/1     Running     0          13h
onap-strimzi-zookeeper-0                        1/1     Running     0          13h

```

### Apply Deployment Patches

```
# runs pm bulk use case once, if this fails try again
./patch-pmbulk.sh
```

### Deploy Performance Management Components

This step deploys
- influxdb
- grafana with datasource to influxdb and dashboard
- pm microservice to get pm data from kafka message bus and push pm data to influxdb

Follow the [metrics instruction](../metrics/README.md)

## Undeploy SMO

```
helm undeploy onap -n onap
for topic in $$(kubectl get kafkatopic -n onap -o name); do   kubectl patch $$topic -n onap -type=json -p '[{"op": "remove", "path": "/metadata/finalizers"}]'; done
kubectl delete ns onap
sudo rm -rf /dockerdata-nfs/onap
```

# Troubleshooting

## k9s
https://k9scli.io/ is a nice tool to manage your k8s ressources

```
sudo apt update 
sudo apt install k9s
```

if docker is install on the install server or on the vm k9s is a helpful tool to investigate further all kubernetes ressources
```
sudo docker run --rm -it -v ~/.kube/config:/root/.kube/config quay.io/derailed/k9s
```




