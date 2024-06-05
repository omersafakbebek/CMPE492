from flask import Flask, request, jsonify
from kubernetes import client, config
import os
import requests
from time import time
app = Flask(__name__)
agents = {}
v1 = None
test = False
migrations = {}
migration_id = 0
@app.route('/register', methods=['POST'])
def register_agent():
    data = request.json
    agents[data['node']] = {"ip": data['ip'], "node_ip": data['node_ip']}

    print(f"Agent registered: {data['node']} - {data['ip']}", flush=True)
    return jsonify({"message": "Agent registered"}), 200

@app.route('/migrate/<namespace>/<pod>/<target>', methods=['POST'])
def handle_migration(namespace, pod, target):
    global migration_id
    start = time()
    cur_mig_id = migration_id
    migration_id += 1
    migrations[cur_mig_id] = {
        "namespace": namespace,
        "pod": pod,
        "containers": [],
        "target_node_ip": agents.get(target)["node_ip"],
        "start_time": start,
        "status": "started"
    }
    pod_info = v1.read_namespaced_pod(name=pod, namespace=namespace)
    containers = [container.name for container in pod_info.spec.containers]
    node_name = pod_info.spec.node_name
    migration_data = {
        "namespace": namespace,
        "pod": pod,
        "containers": containers,
        "target_node_ip": agents.get(target)["node_ip"],
    }
    migrations[cur_mig_id] = migration_data
    print(f"Migration data: {migrations[cur_mig_id]}", flush=True)
    source_agent_ip = agents.get(node_name)["ip"]
    target_agent_ip = agents.get(target)["ip"]
    if source_agent_ip and target_agent_ip:
        migrations[cur_mig_id]["status"] = "checkpoint-transfer-initiated"
        print(f"Checkpoint-Transfer initiated for {pod}", flush=True)
        response = requests.post(f'http://{source_agent_ip}:8001/checkpoint-transfer', json=migration_data)
        v1.delete_namespaced_pod(name=pod, namespace=namespace)
        print("Checkpoint-Transfer completed", flush=True)
        migrations[cur_mig_id]["status"] = "checkpoint-transfer-completed"
        # Send image creation request to target node
        print(f"Image creation initiated for {pod}", flush=True)
        migrations[cur_mig_id]["status"] = "image-creation-initiated"
        response = requests.post(f'http://{target_agent_ip}:8001/create-images', json=containers)
        migrations[cur_mig_id]["status"] = "image-creation-completed"
        print("Image creation completed", flush=True)
        # Change the pod spec to use the new image
        print("Pod Creation initiated", flush=True)
        migrations[cur_mig_id]["status"] = "pod-creation-initiated"
        modify_and_recreate_pod(namespace, pod_info, target)
        print(f"Migration completed for {pod}", flush=True)
        end = time()
        migrations[cur_mig_id]["status"] = "completed"
        migrations[cur_mig_id]["end_time"] = end
        migrations[cur_mig_id]["duration"] = end - start
        return jsonify({"message": f"Migration completed in {end - start}"}), 200
    else:
        return jsonify({"error": "Source Agent or Target Agent not found"}), 404

def modify_and_recreate_pod(namespace, pod, target_node):
    pod.spec.node_name = target_node  # Change the node name
    for container in pod.spec.containers:
        container.image = f"localhost/{container.name}-checkpoint:latest"  # Change the image to the new image    
    new_pod_name = f"{pod.metadata.name}-migrated"
    pod.metadata.name = new_pod_name
    pod.metadata.resource_version = None  # Clear the resource version
    v1.create_namespaced_pod(namespace=namespace, body=pod)
    # Wait until pod is running
    while True:
        new_pod = v1.read_namespaced_pod(name=new_pod_name, namespace=namespace)
        if new_pod.status.phase == "Running":
            break
    print(f"New pod {new_pod_name} created on node {target_node}", flush=True)


if __name__ == '__main__':
    test = os.environ.get('TEST')
    if test:
      config.load_kube_config()
    else:
      config.load_incluster_config()

    v1 = client.CoreV1Api()
    app.run(host='0.0.0.0', port=8000)