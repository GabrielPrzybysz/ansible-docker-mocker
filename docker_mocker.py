#!/usr/bin/python
from ansible.module_utils.basic import AnsibleModule
import subprocess
import yaml

def build_docker_image(image_name, dockerfile_path):
    subprocess.run(["docker", "build", "-t", image_name, dockerfile_path])

def instantiate_docker_containers(hosts_count, hosts_file_path, group_name, image_name):
    # Instantiate Docker containers
    for i in range(1, hosts_count + 1):
        container_name = f"host{i}"
        subprocess.run(["docker", "run", "-d", "--name", container_name, image_name])

    # Gather Docker container info
    container_info = []
    for i in range(1, hosts_count + 1):
        container_name = f"host{i}"
        output = subprocess.run(["docker", "inspect", container_name], capture_output=True, text=True)
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
            image_name=dict(type='str', required=True),
            dockerfile_path=dict(type='str', required=True)
        )
    )

    hosts_count = module.params['hosts_count']
    hosts_file_path = module.params['hosts_file_path']
    group_name = module.params['group_name']
    image_name = module.params['image_name']
    dockerfile_path = module.params['dockerfile_path']

    try:
        build_docker_image(image_name, dockerfile_path)
        instantiate_docker_containers(hosts_count, hosts_file_path, group_name, image_name)
        module.exit_json(changed=True, msg="Docker containers instantiated and added to inventory file")
    except Exception as e:
        module.fail_json(msg=f"Failed to instantiate Docker containers: {str(e)}")

if __name__ == '__main__':
    main()
