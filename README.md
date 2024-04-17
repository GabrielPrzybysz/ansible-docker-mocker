![_4e42ea76-ace3-431b-ac96-56529fda93e5](https://github.com/GabrielPrzybysz/ansible-docker-mocker/assets/45472156/9467ce97-4f4e-41a4-bbad-aebee47d5957)

# Automating Docker Image Building, Container Provisioning, and Ansible Inventory Update

This Python script provides a robust solution for automating Docker image building, container instantiation, and Ansible inventory update with container IP addresses.
```yml
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

## Features

- **Effortless Docker Image Building**: Simply specify the Dockerfile path and the desired image name, and the script will handle the rest, automating the Docker image building process.

- **Seamless Container Provisioning**: Define the number of containers you need, and the script will effortlessly instantiate them based on the provided image, streamlining container provisioning.

- **Ansible Inventory Automation**: The script automatically updates the Ansible inventory file with the IP addresses of the provisioned containers, ensuring seamless integration with Ansible for configuration management.

## Benefits

- **Time Saving**: Automates tedious manual tasks, such as building Docker images, provisioning containers, and updating Ansible inventory, saving valuable time and effort.

- **Consistency**: Ensures consistency across environments by automating the deployment process, reducing the risk of human error in manual deployments.

## Use Cases

- **Automated Testing Environments**: Quickly provision disposable test environments with Docker containers for automated testing, enabling faster feedback loops and improved software quality. Integrate with testing frameworks such as Selenium or pytest to automate testing workflows.

- **Load Testing**: Scale up the number of containers to simulate heavy loads on your application and measure its performance under stress. Automate the provisioning and teardown of containers to streamline the load testing process.

- **Integration Testing**: Automate the deployment of multiple interconnected services in Docker containers to facilitate integration testing. Ensure that different components of your application work seamlessly together in a controlled environment.
