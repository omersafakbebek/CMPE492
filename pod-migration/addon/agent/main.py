from flask import Flask, request, jsonify
import requests
import os
import paramiko
import subprocess
from time import time
app = Flask(__name__)
controller_ip = "controller"
test = False
kubelet_api = None
cert_path = '/etc/kubernetes/pki/apiserver-kubelet-client.crt'
key_path = '/etc/kubernetes/pki/apiserver-kubelet-client.key'
pem_file_path = '/etc/kubernetes/pki/sftp.pem'
@app.route('/checkpoint-transfer', methods=['POST'])
def handle_checkpoint_transfer():
    data = request.json
    namespace = data['namespace']
    pod = data['pod']
    containers = data['containers']
    target_node_ip = data['target_node_ip']
    print(f"Checkpoint request received for {pod} in {namespace}", flush=True)
    checkpoints = {}
    for container in containers:
        print(f"Creating checkpoint for {container} in {pod}", flush=True)
        response = requests.post(f'{kubelet_api}/{namespace}/{pod}/{container}', cert=(cert_path, key_path), verify=False)
        print(response.text, flush=True)
        checkpoints[container] = response.json()["items"][0]
    print(f"Checkpoints: {checkpoints}", flush=True)
    transfer_successful = transfer_checkpoint_files(checkpoints, target_node_ip)
    if transfer_successful:
        return jsonify({"message": "Checkpoint-Transfer handled successfully"}), 200
    else:
        return jsonify({"error": "Failed to transfer checkpoint files"}), 500
@app.route('/create-images', methods=['POST'])
def handle_image_creation():
    data = request.json
    containers = data
    for container in containers:
        checkpoint_file = f"/tmp/checkpoints/{container}.tar"
        image_name = f"{container}-checkpoint"
        container_name = f"{container}-checkpoint-{int(time())}"
        try:
            subprocess.run(["buildah", "from", "--name", container_name, "scratch"], check=True)
            subprocess.run(["buildah", "add", container_name, checkpoint_file, "/"], check=True)
            subprocess.run(["buildah", "config", f"--annotation=io.kubernetes.cri-o.annotations.checkpoint.name={container}", container_name], check=True)
            subprocess.run(["buildah", "commit", container_name, f"{image_name}:latest"], check=True)
            print(f"Successfully created image {image_name} from checkpoint {checkpoint_file}", flush=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed to create image for {container}: {str(e)}", flush=True)
            return jsonify({"error": f"Failed to create image for {container}"}), 500
    print("Image creation handled successfully", flush=True)
    return jsonify({"message": "Image creation handled successfully"}), 200
def transfer_checkpoint_files(checkpoints, target_node_ip):
    try:
        key = paramiko.Ed25519Key.from_private_key_file(pem_file_path)
        transport = paramiko.Transport((target_node_ip, 22))
        transport.connect(username='ansible_user', pkey=key) 
        sftp = paramiko.SFTPClient.from_transport(transport)
        remote_dir = "/tmp/checkpoints"
        try:
            sftp.mkdir(remote_dir, mode=777)
        except IOError:
            pass  
        for container, checkpoint in checkpoints.items():
            remote_file = os.path.join(remote_dir, f"{container}.tar")
            sftp.put(checkpoint, remote_file)        
        sftp.close()
        transport.close()
        print(f"Successfully transferred checkpoint files to {target_node_ip}", flush=True)
        return True
    except Exception as e:
        print(f"Failed to transfer checkpoint files to {target_node_ip}: {str(e)}", flush=True)
        return False
def register_with_controller(node_name, node_ip, pod_ip):
    agent_data = {"node": node_name, "ip": pod_ip, "node_ip": node_ip}

    response = requests.post(f'http://{controller_ip}:8000/register', json=agent_data)
    print(response.json(), flush=True)

if __name__ == '__main__':
    test = os.environ.get('TEST')
    if test:
        controller_ip = "localhost"
    pod_name = os.environ.get('POD_NAME')
    node_name = os.environ.get('NODE_NAME')
    node_ip = os.environ.get('NODE_IP')
    pod_ip = os.environ.get('POD_IP')
    kubelet_api = f'https://{node_ip}:10250/checkpoint'
    print(kubelet_api)
    register_with_controller(node_name=node_name, node_ip=node_ip, pod_ip=pod_ip)
    app.run(host='0.0.0.0', port=8001)