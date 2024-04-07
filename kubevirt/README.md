## Deploy KubeVirt Operator
```
export VERSION=$(curl -s https://storage.googleapis.com/kubevirt-prow/release/kubevirt/kubevirt/stable.txt)
echo $VERSION
kubectl create -f https://github.com/kubevirt/kubevirt/releases/download/$VERSION/kubevirt-operator.yaml
```
## Deploy Kubevirt Custom Resource Definitions
```
kubectl create -f https://github.com/kubevirt/kubevirt/releases/download/$VERSION/kubevirt-cr.yaml 
```
## Check the Components
```
kubectl get all -n kubevirt
```
## Install virtctl
```
VERSION=$(kubectl get kubevirt.kubevirt.io/kubevirt -n kubevirt -o=jsonpath="{.status.observedKubeVirtVersion}")
ARCH=$(uname -s | tr A-Z a-z)-$(uname -m | sed 's/x86_64/amd64/') || windows-amd64.exe
echo ${ARCH}
curl -L -o virtctl https://github.com/kubevirt/kubevirt/releases/download/$VERSION/virtctl-$VERSION-$ARCH
chmod +x virtctl
sudo install virtctl /usr/local/bin
```
## Download the VM manifest
```
wget https://kubevirt.io/labs/manifests/vm.yaml
```
## Apply the manifest
```
kubectl apply -f https://kubevirt.io/labs/manifests/vm.yaml
```
## Start the VM
```
virtctl start testvm
```
## Accessing VMs
```
virtctl console testvm
```
## Shut Down the VM
```
virtctl stop testvm
```
## Delete the VM
```
kubectl delete vm testvm
```