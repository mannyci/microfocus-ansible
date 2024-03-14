# Ansible Collection for Microfocus CMDB

The Ansible Collection for Microfocus CMDB includes a dynamic inventory to be used by Ansible.

# Ansible version

This collection has been tested against following Ansible versions: >=2.9.10.

# Python version

This collection requires Python 3.x or greater.

# Included Content

## Inventory plugins

| Name | Description |
|---|---|
|microfocus.itsm.ucmdb|Microfocus CMDB as Inventory source |

## Modules

# Installing this collection
You can install the Microfocus collection with the Ansible Galaxy CLI:

```
ansible-galaxy collection install git+https://github.com/mannyci/microfocus-ansible.git
```

You can also include it in a `requirements.yml` file and install it with `ansible-galaxy collection install -r requirements.yml`, using the format:

```
---
collections:
  - name: microfocus.itsm
```

