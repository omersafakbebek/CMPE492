from flask import Flask, jsonify
from kubernetes import client, config, watch
import threading
import os

app = Flask(__name__)

pod_creation_latencies = {}

def watch_pod_scheduling_events():
    print("Watching for pod scheduling events...")
    w = watch.Watch()
    for event in w.stream(v1.list_event_for_all_namespaces):
        if event['type'] == "ADDED" and event['object'].reason == 'Scheduled':
            pod_name = event['object'].involved_object.name
            namespace = event['object'].involved_object.namespace
            try:
                pod = v1.read_namespaced_pod(name=pod_name, namespace=namespace)
                creation_timestamp = pod.metadata.creation_timestamp
                scheduled_timestamp = event['object'].first_timestamp
                if creation_timestamp and scheduled_timestamp:
                    latency = (scheduled_timestamp - creation_timestamp).total_seconds()
                    pod_creation_latencies[pod_name] = latency
                    print(f"Pod {pod_name} scheduled in {latency:.2f} seconds")
            except client.exceptions.ApiException as e:
                continue
        elif event['type'] == 'DELETED':
            pod_name = event['object'].metadata.name
            pod_creation_latencies.pop(pod_name, None)
            print(f"Pod {pod_name} deleted")

@app.route('/pod-creation-latencies', methods=['GET'])
def get_pod_creation_latencies():
    return jsonify(pod_creation_latencies)

if __name__ == '__main__':
    in_cluster = os.environ.get('IN_CLUSTER')
    if in_cluster == "true":
      config.load_incluster_config()
    else:
        config.load_kube_config()
    v1 = client.CoreV1Api()

    threading.Thread(target=watch_pod_scheduling_events, daemon=True).start()
    
    app.run(debug=True, host='0.0.0.0', port=3000)
