# docker_mocker — Ansible Module for Docker Automation

An Ansible custom module that automates Docker image building, container provisioning, and Ansible inventory population — all in a single task.

---

## Overview

`docker_mocker` is a Python-based Ansible module that performs three sequential operations:

1. **Builds a Docker image** from a specified Dockerfile path.
2. **Provisions N containers** from that image, naming them `<image_name>_1` through `<image_name>_N`.
3. **Inspects each container** to retrieve its IP address and appends them as a named group to an existing Ansible inventory YAML file.

---

## Requirements

- Python 3.x
- `docker` CLI available on the host
- `ansible` with `AnsibleModule` (`ansible.module_utils.basic`)
- `PyYAML` (`pyyaml`)
- The inventory file specified in `hosts_file_path` must already exist (even if empty)

---

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `hosts_count` | int | Yes | Number of Docker containers to instantiate |
| `hosts_file_path` | str | Yes | Path to the Ansible inventory YAML file to update |
| `group_name` | str | Yes | Inventory group name to create for the containers |
| `image_name` | str | Yes | Name to assign to the built Docker image (also used as container name prefix) |
| `dockerfile_path` | str | Yes | Path to the directory containing the `Dockerfile` |

---

## How It Works

### 1. Image Build

Calls `docker build -t <image_name> <dockerfile_path>` via subprocess.

### 2. Container Provisioning

Runs `docker run -d --name <image_name>_<i> <image_name>` for each container index from `1` to `hosts_count`.

### 3. Inventory Update

- Calls `docker inspect <container_name>` for each container.
- Parses the JSON output to extract `NetworkSettings.IPAddress`.
- Loads the existing inventory YAML file.
- **Skips silently** if `group_name` already exists in the inventory (idempotency guard).
- Appends the group with a list of IP addresses and writes the file back.

**Resulting inventory structure:**

```yaml
docker_containers:
  - 172.17.0.2
  - 172.17.0.3
  - 172.17.0.4
  # ...
```

---

## Usage Example

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

### What happens when this task runs:

1. Builds a Docker image named `ubuntu` from `../docker_images/ubuntu/Dockerfile`.
2. Starts 10 detached containers: `ubuntu_1`, `ubuntu_2`, ..., `ubuntu_10`.
3. Inspects each container and collects their IP addresses.
4. Appends the group `docker_containers` with those IPs to `../inventory.yml`.

---

## Module Placement

Place the module file inside a `library/` directory relative to your playbook, or in a path defined by `ANSIBLE_LIBRARY`:

```
project/
├── library/
│   └── docker_mocker.py
├── inventory.yml
├── docker_images/
│   └── ubuntu/
│       └── Dockerfile
└── playbook.yml
```

---

## Return Values

| Key | Type | Description |
|---|---|---|
| `changed` | bool | Always `True` on success |
| `msg` | str | Human-readable status message |

On failure, the module calls `fail_json` with the exception message.

---

## Limitations & Notes

- **Idempotency**: If the specified `group_name` already exists in the inventory file, the module prints a warning and exits without making changes. Existing containers are not checked — re-running the playbook will attempt to create containers with already-existing names, which will cause `docker run` to fail.
- **IP assignment**: IPs are read from `NetworkSettings.IPAddress` (bridge network default). Containers on custom networks may return an empty string here; use `NetworkSettings.Networks.<network>.IPAddress` in that case.
- **Error handling**: Subprocess calls (`docker build`, `docker run`, `docker inspect`) do not explicitly check for non-zero return codes. Failures in Docker commands will silently pass unless they raise a Python exception.
- **`become: yes`** is required to run Docker commands with elevated privileges on most Linux systems.

---

## Use Cases

- **Automated test environments**: Spin up isolated containers for integration or end-to-end tests, then pass inventory to subsequent Ansible roles that configure the test targets.
- **Load testing**: Rapidly provision a fleet of containers and feed their IPs to load testing tools via the generated inventory.
- **Multi-service integration testing**: Provision multiple containers representing different application tiers and manage them uniformly through Ansible.
