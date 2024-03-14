# -*- coding: utf-8 -*-
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r"""
name: ucmdb
author:
  - Manas Maiti
short_description: Microfocus CMDB as Ansible inventory source
description:
  - Builds inventory from Microfocus CMDB
  - Requires a configuration file ending/named in C(ucmdb.yml) or C(ucmdb.yaml).
version_added: 1.0.0
extends_documentation_fragment:
  - ansible.builtin.constructed
options:
  plugin:
    description:
      - The name of the inventory plugin
    required: true
    type: str
    choices: [ 'microfocus.itsm.ucmdb' ]
  url:
    description:
      - URL of the Microfocus CMDB instance.
    required: true
    type: str
    env:
        - name: UCMDB_SERVER
  user:
    description:
      - Username accessing the Microfocus CMDB instance.
    required: true
    type: str
    env:
        - name: UCMDB_USER
  password:
    description:
      - Password of the user accessing the Microfocus CMDB instance.
    required: true
    type: str
    env:
        - name: UCMDB_PASSWORD
  validate_certs:
    description:
      - Whether or not to verify the TLS certificates of the Microfocus CMDB instance.
    type: boolean
    default: true
    env:
        - name: VALIDATE_CERTS
  tql:
    description:
      - Name of the TQL to query from the Microfocus CMDB instance.
    required: true
    type: str
"""

EXAMPLES = r"""
# An example that retrieves a host from Microfocus CMDB instance.
plugin: microfocus.itsm.ucmdb

# `ansible-inventory -i inventory.ucmdb.yml --graph` output:
# @all:
#  |--@ungrouped:
#  |  |--DatabaseServer1
#  |  |--DatabaseServer2
#  |  |--INSIGHT-NY-03
#  |  |--MailServerUS
#  |  |--VMWARE-SD-04

"""

import json
import os

from ansible.module_utils.six import PY2
from ansible.module_utils.urls import Request, basic_auth_header
from ansible.plugins.inventory import BaseInventoryPlugin, Cacheable, Constructable, to_safe_group_name
from ansible.errors import AnsibleParserError
from ansible.errors import AnsibleError

from ..module_utils.client import Client

# 3rd party imports
try:
    import requests
    from requests.auth import HTTPBasicAuth
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

class InventoryModule(BaseInventoryPlugin, Cacheable, Constructable):
  ''' Host inventory parser for ansible using Microfocus CMDB as source. '''

  NAME = 'microfocus.itsm.ucmdb'

  def __init__(self):

    super(InventoryModule, self).__init__()
    # from config
    self.url = None
    self.headers = None
    self.cis = None

    if not HAS_REQUESTS:
        raise AnsibleError('This script requires python-requests 1.1 as a minimum version')

  def verify_file(self, path):
    ''' return true/false if this is possibly a valid file for this plugin to consume '''
    valid = False
    if super(InventoryModule, self).verify_file(path):
      # base class verifies that file exists and is readable by current user
      if path.endswith(('ucmdb.yaml', 'ucmdb.yml')):
        valid = True
      else:
        self.display.vvv('Skipping due to inventory source not ending in "ucmdb.yaml" nor "ucmdb.yml"')
    return valid

  def _populate(self):

    self.headers = Client._session(self)
    self.response = Client._exec_tql(self)

    for ci in self.response['cis']:
      if ci['type'] == "fx_server":
        
        name = ci['properties']['name']
        self.inventory.add_host(name)
        for k,v in ci.items():
          if v != 'null':
            self.inventory.set_variable(name, k, v)

  def _fetch_params(self):

    params = dict()


  def parse(self, inventory, loader, path, cache=True):

    super(InventoryModule, self).parse(inventory, loader, path)

    # read config from file, this sets 'options'
    self._read_config_data(path)
    self.url = self.get_option('url')
    self.tql = self.get_option('tql')
    self.username = self.get_option('user')
    self.password = self.get_option('password')

    self._populate()
