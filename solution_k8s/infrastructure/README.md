# Overview

# Setup
## install kubeone

```
sudo apt install unzip -y
sudo yum install unzip  #RockyLinux
# changed k8s repo prevents apt update
export K8S_VERSION=v1.24
curl -fsSL https://pkgs.k8s.io/core:/stable:/$K8S_VERSION/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg
echo "deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/$K8S_VERSION/deb/ /" | sudo tee /etc/apt/sources.list.d/kubernetes.list


# if dedicated version is required
./scripts/install-kubeone.sh

# if latest kubeone version is required:
curl -sfL https://get.kubeone.io | sh 

rm -r kubeone_1.*_linux_amd64

 kubeone version
{
  "kubeone": {
    "major": "1",
    "minor": "7",
    "gitVersion": "1.7.3",
    "gitCommit": "b86d23e5178761dd8534fda6c3cb52d92e286c37",
    "gitTreeState": "",
    "buildDate": "2024-03-01T18:55:33Z",
    "goVersion": "go1.21.6",
    "compiler": "gc",
    "platform": "linux/amd64"
  },
  "machine_controller": {
    "major": "1",
    "minor": "57",
    "gitVersion": "v1.57.5",
    "gitCommit": "",
    "gitTreeState": "",
    "buildDate": "",
    "goVersion": "",
    "compiler": "",
    "platform": "linux/amd64"
  }
}

```

## Prepare kubeone config files

### kubeone.yaml

Adjust IP addresses of your baremetal or VM server.

```
vi infrastructure/baremetal/kubeone.yaml
...
   - publicAddress: '<yourPublicIP>'  
      privateAddress: '<yourprivateIP>'
      sshUsername: <youruser>
...

```
### addons

Kubeone will apply all addons listed in addons sub-directory.
Ingress deployment is configured to open port 80 and 443 directly on the host machine.
Change hostPort in the deplyoment if a different port is required.
Basic certificate handling will be applied wit cert-manager. In case of own CA instance please adapt 

## Prerequisites
Please verify if sudo can be executed passwordless.
otherwise add this file and replace <youruser> with your username:
```
sudo vi /etc/sudoers.d/20-kubeone-user
# Created for kubeone passwordless sudo

# User rules for <youruser>
<youruser> ALL=(ALL) NOPASSWD:ALL

```

## Deploy kubernetes cluster

Execute the following commands and confirm settings:
```
ssh-keygen -q -t rsa -N '' -f ~/.ssh/id_rsa_kubeone <<<y >/dev/null 2>&1
cat ~/.ssh/id_rsa_kubeone.pub >> ~/.ssh/authorized_keys
eval `ssh-agent`
ssh-add ~/.ssh/id_rsa_kubeone
cd infrastructure
kubeone apply -m kubeone.yaml
mkdir ~/.kube
cp campusos-test-cluster-kubeconfig ~/.kube/config
```

Verify access to kubernetes cluster

```
kubectl get nodes
#NAME                                 STATUS   ROLES           AGE     VERSION
#o-ran-sc-smo-3.t3.lab.osn-lab.com   Ready    control-plane   2m56s   v1.24.5

```



## cert-manager

Kubernetes cluster provides cert-manager with a self-signed cluster-issuer.

```
kubectl apply -f certs/selfsigned-cluster-issuer.yaml
kubectl get clusterissuers -o wide selfsigned-cluster-issuer

# NAME                        READY   STATUS   AGE
# selfsigned-cluster-issuer   True             42s

```


## Additional pre-requisites

- helm
```
scripts/install_helm.sh
```
- kafka-strimzi operator
```
scripts/install-kafka-strimzi.sh

```
Stop with ctrl+c if `READY 1/1 STATUS: Running`
- mariadb operator
```
scripts/install-mariadb-operator.sh

# NAME                                                READY   STATUS              RESTARTS   AGE
# mariadb-operator-7bf57fd855-ckgnj                   0/1     ContainerCreating   0          115s
# mariadb-operator-cert-controller-54dd9575f6-zx9kw   0/1     ContainerCreating   0          115s
# mariadb-operator-webhook-74c87c5b8-rhkkr            0/1     ContainerCreating   0          115s
# mariadb-operator-webhook-74c87c5b8-rhkkr            0/1     Running             0          5m2s
# mariadb-operator-cert-controller-54dd9575f6-zx9kw   0/1     Running             0          5m2s
# mariadb-operator-7bf57fd855-ckgnj                   1/1     Running             0          5m3s
# mariadb-operator-webhook-74c87c5b8-rhkkr            1/1     Running             0          5m25s
# mariadb-operator-cert-controller-54dd9575f6-zx9kw   1/1     Running             0          5m25s

```

## Application

If all steps are done, cluster should started pods as follows

```
kubectl get pods --all-namespaces
NAMESPACE          NAME                                                         READY   STATUS      RESTARTS   AGE
cert-manager       cert-manager-77d99d86f9-lc4wx                                1/1     Running     0          15m
cert-manager       cert-manager-cainjector-bdd866bd4-s27hn                      1/1     Running     0          17m
cert-manager       cert-manager-webhook-5655dcfb4b-g9prn                        1/1     Running     0          17m
ingress-nginx      ingress-nginx-admission-create-rjdt5                         0/1     Completed   0          17m
ingress-nginx      ingress-nginx-admission-patch-5mqrg                          0/1     Completed   0          17m
ingress-nginx      ingress-nginx-controller-64c44fcf4d-hc6mf                    1/1     Running     0          17m
kube-system        calico-kube-controllers-9c48d8ff9-89p66                      1/1     Running     0          17m
kube-system        canal-hs5nj                                                  2/2     Running     0          17m
kube-system        coredns-77d547497-pjf6s                                      1/1     Running     0          17m
kube-system        coredns-77d547497-xc8db                                      1/1     Running     0          17m
kube-system        etcd-o-ran-sc-smo-2.t3.lab.osn-lab.com                      1/1     Running     0          18m
kube-system        kube-apiserver-o-ran-sc-smo-2.t3.lab.osn-lab.com            1/1     Running     0          18m
kube-system        kube-controller-manager-o-ran-sc-smo-2.t3.lab.osn-lab.com   1/1     Running     0          17m
kube-system        kube-proxy-ffqcx                                             1/1     Running     0          17m
kube-system        kube-scheduler-o-ran-sc-smo-2.t3.lab.osn-lab.com            1/1     Running     0          18m
kube-system        metrics-server-5dd584cfb8-9pmxs                              1/1     Running     0          17m
kube-system        node-local-dns-g7vgk                                         1/1     Running     0          17m
mariadb-operator   mariadb-operator-7bf57fd855-ckgnj                            1/1     Running     0          8m6s
mariadb-operator   mariadb-operator-cert-controller-54dd9575f6-zx9kw            1/1     Running     0          8m6s
mariadb-operator   mariadb-operator-webhook-74c87c5b8-rhkkr                     1/1     Running     0          8m6s
strimzi-system     strimzi-cluster-operator-677cc89c49-25m47                    1/1     Running     0          13m


```

If kubernetes baremetal cluster is ready, please continue with application deployment
[see: SMO Deployment](../../application/README.md)

## Troubleshooting

TODO

# deploy/undeploy sdnc

```
# Uninstall using below command
helm uninstall onap-sdnc -n onap

# Remove the directory from nfs server
sudo rm -rf /dockerdata-nfs/dev/sdnc
# Secret deletion
# kubectl delete secret dev-sdnc-secret-0 -n onap

# dev-sdnc deploy again

helm install dev-sdnc local/sdnc --debug --namespace onap --create-namespace -f 

```

