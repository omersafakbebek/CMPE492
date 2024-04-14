# ADDON EXAMPLE
* You should have a cluster.
* `cd manifests`
* `kubectl apply -f role.yaml`
* `kubectl apply -f deployment.yaml`
* `kubectl apply -f service.yaml`
* `kubectl port-forward svc/pod-creation-latency-watcher 3000:3000`
* Access the api through `http://localhost:3000/pod-creation-latencies`
