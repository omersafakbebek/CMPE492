# DEPLOYMENT OF AN EXAMPLE STATELESS APPLICATION
Source: https://kubernetes.io/docs/tutorials/stateful-application/mysql-wordpress-persistent-volume/ <br/>
Note: A kubernetes cluster is required.
## Steps:
* Run ```kubectl apply -k ./```. This command will create resources and secrets specified in the kustomization.yaml file. secretGenerator in this file
creates a secret object named mysql-pass which includes a key-value pair for password. Also, the specified files in the resources section creates necessary resources for mysql and wordpress.
* In the mysql-deployment.yaml, a Deployment, a PersistentVolumeClaim and a Service objects are created. The PersistentVolumeClaim is a request for storage. The storage is used for storing the mysql database data permanently. The claimed volume can be mounted as read-write by a single node.
* In the wordpress-deployment.yaml, a Deployment, a PersistentVolumeClaim and a Service objects are created. The PersistentVolumeClaim is a request for storage. The claimed volume can be mounted as read-write by a single node.
## Current State After the Steps
<img width="511" alt="Screenshot 2024-02-24 at 17 26 15" src="https://github.com/omersafakbebek/CMPE492/assets/75090441/0477dad3-30c5-4d6c-8a14-459bca86b043">
<img width="550" alt="Screenshot 2024-02-24 at 17 27 22" src="https://github.com/omersafakbebek/CMPE492/assets/75090441/c1125d62-037c-4216-ae5f-6fda0eb4f999">
<img width="550" alt="Screenshot 2024-02-24 at 17 28 02" src="https://github.com/omersafakbebek/CMPE492/assets/75090441/44c54c7a-3f98-4c80-a141-2d86f046d5ef">
<img width="762" alt="Screenshot 2024-02-24 at 17 28 28" src="https://github.com/omersafakbebek/CMPE492/assets/75090441/28646ad5-c454-4c95-8b20-c9ce3be9e9d1">


Note that the status of external ip for the wordpress service is pending since a cloud provider which supports load balancers is not used.

## Accessing to the app
* If your cluster is in a cloud provider which supports load balancers, you can get the external ip address for the frontend service by running the following command. <br/>
```kubectl get service wordpress```
* If you are using minikube, run ```minikube tunnel```. This command will create a tunnel for the application. After that, get the external ip address by running ```kubectl get service wordpress```. You can access to the application with ```EXTERNAL-IP:80```.
<img width="762" alt="Screenshot 2024-02-24 at 17 31 01" src="https://github.com/omersafakbebek/CMPE492/assets/75090441/d9f6214a-5b09-4f6c-9df9-b94e86ca7234">

* In killercoda, click on the menu and choose Traffic / Ports, then access to the application via NodePort of the service.
<img width="762" alt="Screenshot 2024-02-24 at 17 39 37" src="https://github.com/omersafakbebek/CMPE492/assets/75090441/17fd060e-a71d-4993-9dc6-7bd1c82ca770">

In my case the node port is 31525.
* In Play With Kubernetes, run ```kubectl port-forward svc/wordpress 80:80```. Then the app is accessible via http://127.0.0.1:80.
## Scale the Wordpress Deployment
* Run ```kubectl scale deployment wordpress --replicas=3```. The number of pods of the deployment wordpress will be increased to 3.
<img width="762" alt="Screenshot 2024-02-24 at 17 35 00" src="https://github.com/omersafakbebek/CMPE492/assets/75090441/9e6cfb03-557a-463e-9cf9-fa3c2ce35ecb">

## Cleaning Up
* Run the following command: 
```kubectl delete -k ./```
<img width="762" alt="Screenshot 2024-02-24 at 17 37 37" src="https://github.com/omersafakbebek/CMPE492/assets/75090441/7da1f3db-653f-4705-be3d-8da817425af2">

## The Application
<img width="762" alt="Screenshot 2024-02-24 at 17 31 57" src="https://github.com/omersafakbebek/CMPE492/assets/75090441/a6ea1335-148d-42e9-8ff2-86a793d4ce66">

