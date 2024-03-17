## Run with web UI
```locust -f locustfile.py --host <LoadBalancerIp>```
## Run without web UI
```locust -f locustfile.py --headless -u <#ofUsers> -r <spawnRate> --host <LoadBalancerIp```
