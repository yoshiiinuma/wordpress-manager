#!/usr/bin/python

"""
Extracts DocumentRoot and ServerName from Apache configuration
"""

import sys
import json
import re
import os

from ansible.module_utils.basic import AnsibleModule

ANSIBLE_METADATA = {
  'metadata_version': '1.1',
  'status': ['preview'],
  'supported_by': 'community'
}

DOCUMENTATION = '''
---
moudle: httpd_config

short_description: extract information from apache configuration file

description:
  - extract ServerName, ServerAlias and DoucmentRoot from each VirtualHost definition in /etc/httpd/conf/httpd.conf

options:
  conf:
    description:
      - The pass to the apache configuration file
    required: false
    default: /etc/httpd/conf/httpd.conf

author:
  - Yoshiaki Iinuma
'''

CONF = '/etc/httpd/conf/httpd.conf'
VirtualHostStart = re.compile(r'<VirtualHost', re.IGNORECASE)
VirtualHostEnd = re.compile(r'</VirtualHost>', re.IGNORECASE)
ServerName = re.compile(r'^ServerName +(.+)$', re.IGNORECASE)
ServerAlias = re.compile(r'^ServerAlias +(.+)$', re.IGNORECASE)
DocRoot = re.compile(r'^DocumentRoot +(.+)$', re.IGNORECASE)

def setup_module():
  module_args = dict(
    conf=dict(type='str', required=False),
  )
  module = AnsibleModule(
    argument_spec=module_args,
    supports_check_mode=False
  )
  return module

def extract_virtualhosts(conf):
  servers = []
  with open(conf) as fp:
    cur = {}
    for line in fp:
      line = line.strip()
      if VirtualHostStart.match(line):
        cur = {}
      elif VirtualHostEnd.match(line):
        if 'mainrootdir' not in cur.get('root', ''):
          servers.append(cur)
        cur = {}
      elif DocRoot.match(line):
        r = DocRoot.match(line)
        cur['root'] = r.group(1)
      elif ServerName.match(line):
        r = ServerName.match(line)
        cur['name'] = r.group(1)
      elif ServerAlias.match(line):
        r = ServerAlias.match(line)
        cur['alias'] = r.group(1)
  return servers

def main():
  module = setup_module()
  conf = module.params.get('conf')
  if not conf:
    conf = CONF
  if not os.path.exists(conf):
    msg = 'File Not Found: ' + str(conf)
    module.fail_json(msg=msg)
    return
  servers = extract_virtualhosts(conf)
  module.exit_json(**{'servers': servers})

if __name__ == '__main__':
  main()
