# -*- coding: utf-8 -*-
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import json
from ansible.module_utils.urls import Request, basic_auth_header
from ansible.errors import AnsibleParserError
from ansible.errors import AnsibleError

# 3rd party imports
try:
    import requests
    from requests.auth import HTTPBasicAuth
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

class Client:
  def __init__(self):
    self.url = None
    self.headers = None
    self.cis = None
    self.tql = None

    if not HAS_REQUESTS:
        raise AnsibleError('This script requires python-requests 1.1 as a minimum version')
  
  def _session(self, **kwargs):
    if not self.headers:
      headers = {
        "Content-Type": "application/json"
      }
      auth_params = {
        'username': self.get_option('user'),
        'password': self.get_option('password'),
        'clientContext': 1
      }
      auth_call = requests.post(self.url + "/authenticate", json=auth_params, headers=headers, verify=self.get_option('validate_certs'))
      auth_call.raise_for_status()
      self.token = auth_call.json()["token"]
      self.headers = {
        "Authorization": "Bearer " + self.token,
        "Content-Type": "application/json"
      }
    return self.headers

  def _exec_tql(self, **kwargs):
    try:
      execute_tql = requests.post(self.url + "/topology", data=self.tql, headers=self.headers, verify=self.get_option('validate_certs'))
    except Exception as e:
      raise AnsibleError(e)
    j_out_dict = json.loads(execute_tql.text)
    self.cis = j_out_dict["cis"]
    self.relations = j_out_dict["relations"]
    return j_out_dict

  def get_relations(self, ucmdbId):
    for r in self.relations:
      return r['end2Id'] if r['end1Id'] == ucmdbId else r['end2Id']

  def get_ip_address(self, ucmdbId):
    for c in self.cis:
      if c['ucmdbId'] == ucmdbId:
        return c['properties']['display_label']
