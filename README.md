# ansible-docker-mocker

An Ansible module that automates Docker image building, container provisioning, and Ansible inventory updates with the IP addresses of the running containers.

## Overview

`docker_mocker` is a custom Ansible module written in Python. It builds a Docker image from a specified Dockerfile, spins up a given number of containers from that image, inspects each container to retrieve its IP address, and appends the group and IPs to an existing Ansible inventory YAML file.

## Parameters

| Parameter         | Type   | Required | Description                                                      |
|-------------------|--------|----------|------------------------------------------------------------------|
| `hosts_count`     | int    | yes      | Number of Docker containers to create.                           |
| `hosts_file_path` | str    | yes      | Path to the Ansible inventory YAML file to update.               |
| `group_name`      | str    | yes      | Inventory group name under which container IPs will be listed.   |
| `image_name`      | str    | yes      | Name to assign to the built Docker image.                        |
| `dockerfile_path` | str    | yes      | Path to the directory containing the Dockerfile to build.        |

## Usage

Copy `docker_mocker.py` to your Ansible `library/` directory and reference the module in a playbook:

```yaml
- name: Instantiate Docker containers and add to inventory
  hosts: localhost
  tasks:
    - name: Instantiate Docker containers and add to inventory
      docker_mocker:
        hosts_count: 10
        hosts_file_path: ../inventory.yml
        group_name: docker_containers
        image_name: ubuntu
        dockerfile_path: ../docker_images/ubuntu
      become: yes
```

## How It Works

1. **Build** – Runs `docker build -t <image_name> <dockerfile_path>` to create the image.
2. **Run** – Starts `hosts_count` detached containers named `<image_name>_1`, `<image_name>_2`, …
3. **Inspect** – Runs `docker inspect` on each container and extracts its `NetworkSettings.IPAddress`.
4. **Update inventory** – Reads the existing inventory YAML file, adds a new group entry with the collected IPs, and writes it back. If the group already exists, the update is skipped.

## Features

- **Automated image builds** – No manual `docker build` step required; just point to the Dockerfile.
- **Bulk container provisioning** – Spin up any number of containers in a single task.
- **Inventory integration** – Container IPs are written directly into the Ansible inventory, making the containers immediately available for subsequent plays.
- **Idempotent group handling** – If the specified inventory group already exists, the module skips the update to avoid duplication.

## Use Cases

- **Automated testing** – Quickly provision short-lived test environments and tear them down after a test run.
- **Load testing** – Scale out containers to simulate concurrent users and measure application performance under stress.
- **Integration testing** – Deploy multiple interconnected services as containers and validate that they work together before a production release.

## Requirements

- Python 3
- `ansible` (module utilities)
- `docker` CLI available on the host
- `PyYAML`
