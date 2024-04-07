## Execute the playbook
* Create a file named gcp-key.json for service account key. Change the variables according to your gcp configuration.
* ```ssh-keygen -t rsa -b 2048 -f ~/.ssh/gcp_ansible -C ansible_user -t ed25519```
* ```export ANSIBLE_SSH_COMMON_ARGS="-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null"```
* ```export ANSIBLE_HOST_KEY_CHECKING=False```
* ```ansible-galaxy collection install google.cloud```
## To Create the Cluster
* ```ansible-playbook play-create-cluster.yaml -e "worker_node_count=3"``
## To Deploy the Application
* ```ansible-playbook play-deploy-and-generate-load.yaml``
## To Delete All Resources
* ```ansible-playbook play-delete-all.yaml -e "worker_node_count=3"``
