#!/usr/bin/python

"""
Returns DocumentRoot and ServerName apache configuration
"""

import sys
import os
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
moudle: wp_config

short_description: extract global variables from Wordpress configuration file

description:
  - extract global variables from Wordpress configuration file

options:
  root:
    description:
      - The Wordpress installed directory
    required: true
  category:
    description:
      - filter the results by this: {all|db|security|debug|others}
    default: all
    required: false

author:
  - Yoshiaki Iinuma
'''

OPTION = re.compile(r"^define\( *'([^']+)' *,  *(\S.+\S|\S*) *\);", re.IGNORECASE)
TBL_PREFIX = re.compile(r"^\$table_prefix *= *'(.+)' *;", re.IGNORECASE)
QUOTED = re.compile(r"^'(.*)'$")

CATEGORIES = {
  'security': [
    'AUTH_KEY', 'SECURE_AUTH_KEY', 'LOGGED_IN_KEY', 'NONCE_KEY',
    'AUTH_SALT', 'SECURE_AUTH_SALT', 'LOGGED_IN_SALT', 'NONCE_SALT'],
  'db': [
    'DB_HOST', 'DB_USER', 'DB_PASSWORD', 'DB_NAME',
    'DB_CHARSET', 'DB_COLLATE', 'table_prefix'],
  #'sites': [
  #  'WP_SITEURL', 'WP_HOME', 'WP_ALLOW_MULTISITE', 'WPLANG', 'WP_CACHE',
  #  'WP_CONTENT_DIR', 'WP_CONTENT_URL', 'WP_PLUGIN_DIR', 'WP_PLUGIN_URL',
  #  'PLUGIN_DIR', 'UPLOADS'],
  'debug': [
    'WP_DEBUG', 'WP_DEBUG_LOG', 'WP_DEBUG_DISPLAY', 'WP_DISABLE_FATAL_ERROR_HANDLER', 'SCRIPT_DEBUG']
}

def strip_quotes(str):
  matched = QUOTED.match(str)
  if matched:
    return matched.group(1)
  return str

def extract_options(conf):
  options = {}
  with open(conf) as fp:
    for line in fp:
      line = line.strip()
      matched = OPTION.match(line)
      if matched:
        options[matched.group(1)] = strip_quotes(matched.group(2))
      matched = TBL_PREFIX.match(line)
      if matched:
        options['table_prefix'] = strip_quotes(matched.group(1))
      
  return options

def setup_module():
  module_args = dict(
    root=dict(type='str', required=True),
    category=dict(type='str', required=False, default='all', choices=['all', 'db', 'security', 'debug', 'others'])
  )
  module = AnsibleModule(
    argument_spec=module_args,
    supports_check_mode=False
  )
  return module

def filter_options(category, options):
  if category == 'all':
      return options
  keys = CATEGORIES.get(category)
  filtered = {}
  if keys:
    for k in keys:
      if k in options:
          filtered[k] = options[k]
    return filtered
  for key in options:
    if key in CATEGORIES['db']:
      continue
    elif key in CATEGORIES['security']:
      continue
    elif key in CATEGORIES['debug']:
      continue
    filtered[key] = options[key] 
  return filtered

def main():
  module = setup_module()
  docroot = module.params.get('root')
  category = module.params.get('category')
  if not docroot:
     msg = 'DocumentRoot Not Specified'
     module.fail_json(msg=msg) 
     return
  if not os.path.exists(docroot):
     msg = 'Directory Not Found: ' + str(docroot)
     module.fail_json(msg=msg) 
     return
  conf = os.path.join(docroot, 'wp-config.php')
  if not os.path.exists(conf):
     msg = 'WP-CONFIG.PHP Not Found: ' + str(conf)
     module.fail_json(msg=msg) 
     return
  options = extract_options(conf)
  options = filter_options(category, options)
  module.exit_json(**{'options': options})

if __name__ == '__main__':
  main()
