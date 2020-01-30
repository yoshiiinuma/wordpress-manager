#!/usr/bin/python

"""
Returns DocumentRoot and ServerName apache configuration
"""

import sys
import os
import shutil
import datetime
import json
import re

from ansible.module_utils.basic import AnsibleModule

ANSIBLE_METADATA = {
  'metadata_version': '1.1',
  'status': ['preview'],
  'supported_by': 'community'
}

DOCUMENTATION = '''
---
moudle: wp_config_update

short_description: replace global variables in Wordpress configuration file

description:
  - replace global variables in Wordpress configuration file with specified values; create a new variable if not exists

options:
  root:
    description:
      - The Wordpress installed directory
    required: true
  replacement:
    description:
      - pairs of variable name and new value to replace configurations
    required: true

author:
  - Yoshiaki Iinuma
'''

STOPEDITING = re.compile(r"/\*.+stop editing!.+\*/")
OPTION = re.compile(r"^define\( *'([^']+)' *,  *(.+) *\);(.*)", re.IGNORECASE)
TBL_PREFIX = re.compile(r"^\$table_prefix *= *'(.+)' *;(.*)", re.IGNORECASE)
BASE = re.compile(r"^\$base *= *'(.+)' *;(.*)", re.IGNORECASE)
INTEGER = re.compile(r"^\d+$")
BOOLEAN = re.compile(r"^(true|false)$", re.IGNORECASE)

def setup_module():
  module_args = dict(
    root=dict(type='str', required=True),
    replacement=dict(type='dict', required=True)
  )
  module = AnsibleModule(
    argument_spec=module_args,
    supports_check_mode=False
  )
  return module

def create_backup(conf):
  dirname = os.path.dirname(conf)
  time = datetime.datetime.now(tz=None).strftime('%Y%m%d%H%M%S')
  dst = os.path.join(dirname, 'wp-config.php.' + time + '.bkup')
  shutil.copyfile(conf, dst)
  return dst

def create_define_statement(key, value, rest=''):
  if key == 'table_prefix':
    return "$table_prefix = '{}';{}\n".format(value, rest) 
  if key == 'base':
    return "$base = '{}';{}\n".format(value, rest) 
  if type(value) is str:
    if BOOLEAN.match(value):
      value = value.lower()
    elif not INTEGER.match(value):
      value = "'" + value + "'"
  if type(value) is bool:
      value = str(value).lower()
  return "define('{}', {});{}\n".format(key, value, rest)

def update_line(line, replacement, rslt):
  matched = OPTION.match(line)
  if matched:
    key = matched.group(1)  
    rest = matched.group(3)  
    if key in replacement:
      val = replacement.pop(key)
      line = create_define_statement(key, val, rest)  
      rslt['updated'].append(line)
      return line
  else:
    if 'table_prefix' in replacement:
      matched = TBL_PREFIX.match(line)
      if matched:
        key = 'table_prefix'
        rest = matched.group(2)  
        val = replacement.pop(key)
        line = create_define_statement(key, val, rest)  
        rslt['updated'].append(line)
        return line
    if 'base' in replacement:
      matched = BASE.match(line)
      if matched:
        key = 'base'
        rest = matched.group(2)  
        val = replacement.pop(key)
        line = create_define_statement(key, val, rest)  
        rslt['updated'].append(line)
        return line
  return line

def update_conf(conf, replacement):
  newlines = []
  targets = replacement.keys()
  stop_editing = False;
  rslt = { 'updated': [], 'inserted': [] }
  with open(conf) as rp:
    for line in rp:
      if stop_editing:
        newlines.append(line)
        continue
      if STOPEDITING.match(line):
        stop_editing = True;
        for key in replacement:
          line = create_define_statement(key, replacement[key])
          newlines.append(line)
          rslt['inserted'].append(line)
      else:
        line = update_line(line, replacement, rslt)
      newlines.append(line)
  with open(conf, 'w') as wp:
    for line in newlines:
        wp.write(line)
  return rslt

def main():
  module = setup_module()
  root = module.params['root']
  replacement = module.params['replacement']
  if not os.path.exists(root):
     msg = 'Directory Not Found: ' + root
     module.fail_json(msg=msg) 
  conf = os.path.join(root, 'wp-config.php')
  if not os.path.exists(conf):
     msg = 'WP-CONFIG.PHP Not Found: ' + conf
     module.fail_json(msg=msg) 
  create_backup(conf)
  update_conf(conf, replacement)
  module.exit_json(msg='Completed', **{ 'replaced': replacement })

if __name__ == '__main__':
  main()
