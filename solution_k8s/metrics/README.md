
# install telegraf influxdb grafana

## add repos
```
helm repo add influxdata https://helm.influxdata.com/
helm search repo influxdata
helm repo add grafana https://grafana.github.io/helm-charts
helm search repo grafana
```

## Install 

```
export METRIC_NAMESPACE=metric
export APP=onap
sudo apt install jq
kubectl apply -f metrics-pv.yaml -n $METRIC_NAMESPACE

helm install $APP-influxdb2 influxdata/influxdb2 -n $METRIC_NAMESPACE --create-namespace -f influxdb-override.yaml
echo $(kubectl get secret onap-influxdb2-auth -o "jsonpath={.data['admin-password']}" --namespace $METRIC_NAMESPACE | base64 --decode)
kubectl exec -t -n metric onap-influxdb2-0 -- sh -c 'influx auth create --token $DOCKER_INFLUXDB_INIT_ADMIN_TOKEN --org $DOCKER_INFLUXDB_INIT_ORG --json --all-access'

kubectl create secret generic -n $METRIC_NAMESPACE influxdb-grafana-token --from-env-file <(kubectl exec -t -n $METRIC_NAMESPACE $APP-influxdb2-0 -- sh -c 'influx auth create --token $DOCKER_INFLUXDB_INIT_ADMIN_TOKEN --org $DOCKER_INFLUXDB_INIT_ORG --json --all-access'|jq -r "to_entries|map(\"\(.key)=\(.value|tostring)\")|.[]" )
# get the token
kubectl get secret -n metric influxdb-grafana-token -o jsonpath='{.data.token}' |base64 -d; echo

kubectl create configmap -n metric grafana-dashboards --from-file dashboards/  #pm-dashboard-oai.json
```
# and adjust grafana-override.yaml

helm install $APP-grafana grafana/grafana  -n $METRIC_NAMESPACE --create-namespace -f grafana-override.yaml 

kubectl get secret --namespace $METRIC_NAMESPACE onap-grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo
```
## update grafana Dashboard

any modifification in the dashboard cannot be saved in the deployment.
Export dashboard as json file and recreate configmap

```
kubectl delete configmap -n metric grafana-dashboards
kubectl create configmap -n metric grafana-dashboards --from-file dashboards/
kubectl label  configmap -n metric grafana-dashboards grafana_dashboard=1
```
Refresh browser and after a certain time the updated dashboard will be available.

## Uninstall grafana
```
export METRIC_NAMESPACE=metric
export APP=onap
helm uninstall $APP-grafana  -n $METRIC_NAMESPACE

# patch pv to resuse persisistent volume and data
kubectl patch pv grafana-storage-local-pv -p '{"spec":{"claimRef": null}}'
# or delete pv and directory
kubectl delete pv  grafana-storage-local-pv
sudo rm -rf /dockerdata-nfs/grafana/

```
## Install pm microservice

```
./deploy-pm-ms.sh
```
## uninstall influxdb

```
export METRIC_NAMESPACE=metric
export APP=onap
helm uninstall $APP-influxdb2  -n $METRIC_NAMESPACE
kubectl delete secret -n $METRIC_NAMESPACE influxdb-grafana-token
kubectl delete pvc onap-influxdb2 -n $METRIC_NAMESPACE
kubectl delete pv  influxdb-storage-local-pv
sudo rm -rf /dockerdata-nfs/influxdb/

```