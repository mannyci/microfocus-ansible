# Ansible Collection for Microfocus CMDB

The Ansible Collection for Microfocus CMDB includes a dynamic inventory to be used by Ansible.

# Ansible version

This collection has been tested against following Ansible versions: >=2.9.10.

# Python version

This collection requires `Python 3.x` or greater.

# Included Content

## Inventory plugins

| Name | Description |
|---|---|
|microfocus.itsm.ucmdb|Microfocus CMDB as Inventory source |

## Example inventory plugin



## Modules

| Name | Description |
|---|---|
|NA|NA

# Installing this collection

## Install from source

With Ansible >= 2.10, you can install from a Github repository (such as this one or your fork):

```
ansible-galaxy collection install git+https://github.com/mannyci/microfocus-ansible.git
```

You can also include it in a `requirements.yml` file and install it with `ansible-galaxy collection install -r requirements.yml`, using the format:

```
---
collections:
  - name: https://github.com/mannyci/microfocus-ansible.git
    type: git
    version: main
```

# Dependencies

These dependencies are required for the Ansible controller, not the Microfocus instance.

- requests

