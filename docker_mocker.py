#!/usr/bin/python

import logging
from ansible.module_utils.basic import AnsibleModule
import subprocess
import yaml

def instantiate_docker_containers(hosts_count, hosts_file_path, group_name, logs_folder):

    # Configure logging
    logging.basicConfig(filename=logs_folder + "/docker_mocker.log", level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Instantiate Docker containers
    for i in range(1, hosts_count + 1):
        container_name = f"ubuntu_container{i}"
        logging.info(f"Creating container: {container_name}")
        subprocess.run(["docker", "run", "-d", "--name", container_name, "ubuntu:latest", "tail", "-f", "/dev/null"])

    # Gather Docker container info
    container_info = []
    for i in range(1, hosts_count + 1):
        container_name = f"ubuntu_container{i}"
        logging.info(f"Inspecting container: {container_name}")
        output = subprocess.run(["docker", "inspect", container_name], capture_output=True, text=True)
        logging.info(output)
        container_info.append(yaml.safe_load(output.stdout))

    # Write IP addresses to the inventory file
    # Load existing data from YAML file
    with open(hosts_file_path, 'r') as f:
        try:
            existing_data = yaml.safe_load(f)
        except yaml.YAMLError as exc:
            print(exc)
            return

    if not existing_data:
        existing_data = {}

    # Check if the group already exists
    if group_name in existing_data:
        print(f"Group {group_name} already exists. Skipping...")
        return

    # Add the group and IP addresses to the data
    group_data = {}
    for info in container_info:
        ip_address = info[0]['NetworkSettings']['IPAddress']
        group_data[ip_address] = None  # You can add more data associated with each IP address if needed
        logging.info(f"Added IP address {ip_address} to group {group_name} in inventory file")

    existing_data[group_name] = group_data

    # Write updated data back to YAML file
    with open(hosts_file_path, 'w') as f:
        yaml.dump(existing_data, f, default_flow_style=False)

def main():
    module = AnsibleModule(
        argument_spec=dict(
            hosts_count=dict(type='int', required=True),
            hosts_file_path=dict(type='str', required=True),
            group_name=dict(type='str', required=True),
            logs_folder=dict(type='str', required=True)
        )
    )

    hosts_count = module.params['hosts_count']
    hosts_file_path = module.params['hosts_file_path']
    group_name = module.params['group_name']
    logs_folder = module.params['logs_folder']

    try:
        instantiate_docker_containers(hosts_count, hosts_file_path, group_name, logs_folder)
        module.exit_json(changed=True, msg="Docker containers instantiated and added to inventory file")
    except Exception as e:
        logging.error(f"Failed to instantiate Docker containers: {str(e)}")
        module.fail_json(msg=f"Failed to instantiate Docker containers: {str(e)}")

if __name__ == '__main__':
    main()
