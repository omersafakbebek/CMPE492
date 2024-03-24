## Create the vpc network, subnet and firewall rules
``` 
gcloud compute networks create example-k8s --subnet-mode custom
gcloud compute networks subnets create k8s-nodes --network example-k8s --range 10.240.0.0/24 --region europe-west3 
gcloud compute firewall-rules create example-k8s-allow-internal \                                                                                 
--allow tcp,udp,icmp,ipip \
--network example-k8s \
--source-ranges 10.240.0.0/24
gcloud compute firewall-rules create example-k8s-allow-external \                                                                                 
--allow tcp:22,tcp:6443,tcp:30000-32767,icmp \
--network example-k8s \
--source-ranges 0.0.0.0/0  
```
## Create the controller node
```
gcloud compute instances create controller \                     
  --async \
  --boot-disk-size 10GB \
  --can-ip-forward \
  --image-family ubuntu-2004-lts \
  --image-project ubuntu-os-cloud \
  --machine-type e2-medium \
  --private-network-ip 10.240.0.11 \
  --scopes compute-rw,storage-ro,service-management,service-control,logging-write,monitoring \
  --subnet k8s-nodes \
  --zone europe-west3-c \
  --tags example-k8s,controller  
```
## Create the worker nodes
```
for i in 0 1; do
  gcloud compute instances create worker-${i} \
  --async \
  --boot-disk-size 10GB \
  --can-ip-forward \
  --image-family ubuntu-2004-lts \
  --image-project ubuntu-os-cloud \
  --machine-type e2-medium \
  --private-network-ip 10.240.0.2${i} \
  --scopes compute-rw,storage-ro,service-management,service-control,logging-write,monitoring \
  --subnet k8s-nodes \
  --zone europe-west3-c \
  --tags example-k8s,worker
done
```
## Install Docker
```
sudo apt update
sudo apt install -y docker.io
sudo systemctl enable docker.service
sudo apt install -y apt-transport-https curl
```
## Install kubelet, kubeadm and kubectl
```
sudo apt-get update
# apt-transport-https may be a dummy package; if so, you can skip that package
sudo apt-get install -y apt-transport-https ca-certificates curl gpg
sudo mkdir -p -m 755 /etc/apt/keyrings
curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.25/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg
echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.25/deb/ /' | sudo tee /etc/apt/sources.list.d/kubernetes.list
sudo apt-get update
sudo apt-get install -y kubelet kubeadm kubectl
sudo apt-mark hold kubelet kubeadm kubectl
```
## Create the cluster
```
# In the controller node
sudo kubeadm init --config config.yaml
```
## Set up kubectl for the user
```
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```
## Join the worker nodes to the controller node
```
# This command is shown in the output of kubeadm init command
sudo kubeadm join --config join.yaml
```
## Install CNI Plugin
```
# In the controller
kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v3.27.2/manifests/tigera-operator.yaml
curl https://raw.githubusercontent.com/projectcalico/calico/v3.27.2/manifests/custom-resources.yaml -O
kubectl create -f custom-resources.yaml
```
## Use Kubectl commands from local terminal
* Copy the related sections from ~/.kube/config to local ~/.kube/config
## Install the gcp csi driver
* [Follow the instructions](https://github.com/kubernetes-sigs/gcp-compute-persistent-disk-csi-driver/blob/master/docs/kubernetes/user-guides/driver-install.md)
## Create the storage class
```kubectl apply -f storageclass.yaml```
## Install metrics server
```kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/high-availability-1.21+.yaml```
## Approve kubelet certificate requests
```
for kubeletcsr in `kubectl -n kube-system get csr | grep kubernetes.io/kubelet-serving | awk '{ print $1 }'`; do kubectl certificate approve $kubeletcsr; done
```
