from kubernetes import client, config, utils, watch
from time import time
from tabulate import tabulate
def print_data_as_table(data):
    table_data = []
    for key, value in data.items():
        row = [
            key, 
            value.get('phase'), 
            value.get('created_at'), 
            value.get('completed_at', 'N/A'), 
            value.get('duration', 'N/A'),
            value.get('node', 'N/A')
        ]
        table_data.append(row)

    headers = ["ID", "Phase", "Created At", "Completed At", "Duration", "Node"]
    table = tabulate(table_data, headers, tablefmt="grid")
    print(table)
def is_completed(pods):
    for pod in pods:
        if (pod["phase"] == "Pending"):
            return False
    return True
def watch_pod_creation():
    pods = dict()
    v1 = client.CoreV1Api()
    w = watch.Watch()
    start = time()
    ret = v1.list_namespaced_pod("default")
    for pod in ret.items:
        pods[pod.metadata.name] = {"phase": pod.status.phase}
    print(pods[0])
    # for event in w.stream(v1.list_namespaced_pod,namespace= "default",timeout_seconds=200):
    #     event_type = event['type']
    #     pod_name = event['object'].metadata.name
    #     pod_phase = event['object'].status.phase
    #     if (pod_name in pods.keys() and pods[pod_name]["phase"] == "Running"):
    #         continue
    #     if event_type == "ADDED":
    #         t= time() - start
    #         print("%s added at %s" % (pod_name, t))
    #         pods[pod_name]={"phase": pod_phase, "created_at":t}
    #     elif (pod_phase == "Running"): 
    #         t = time() - start
    #         duration = t - pods[pod_name]["created_at"]
    #         pods[pod_name]["phase"] = pod_phase
    #         pods[pod_name]["completed_at"] = t
    #         pods[pod_name]["duration"] = duration
    #         pods[pod_name]["node"] = event['object'].spec.node_name
    #         print("%s completed at %s in %s seconds" % (pod_name, t, duration))
    #     else:
    #         pods[pod_name]["phase"] = pod_phase
    #     if (is_completed(pods.values())):
    #         w.stop()     
    print("Pod creation stage is completed")
    print(print_data_as_table(pods))
def main():
    config.load_kube_config()
    watch_pod_creation()
if __name__ == "__main__":
    main()