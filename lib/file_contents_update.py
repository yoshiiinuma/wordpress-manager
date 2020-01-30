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
moudle: file_contents_update

short_description: change file contents

description:
  - search a file for given words and replace them with a different one

options:
  filepath:
    description:
      - The path to the file to be replaced
    required: true
  replacements:
    description:
      - list of dict({ from, to })
    required: true
  backup:
    description:
      - boolean value; create a backup file if true

author:
  - Yoshiaki Iinuma
'''

def setup_module():
  module_args = dict(
    filepath=dict(type='str', required=True),
    replacements=dict(type='list', required=True, elements='dict'),
    backup=dict(type='bool', required=False, default=True)
  )
  module = AnsibleModule(
    argument_spec=module_args,
    supports_check_mode=True
  )
  return module

def create_backup(filepath):
  dirname = os.path.dirname(filepath)
  filename = os.path.basename(filepath)
  time = datetime.datetime.now(tz=None).strftime('%Y%m%d%H%M%S')
  dst = os.path.join(dirname, filename + '.' + time + '.bkup')
  shutil.copyfile(filepath, dst)
  return dst

def search_contents(filepath, replacements):
  rslt = [] 
  with open(filepath, 'r') as fp:
    text = fp.read()
    for word in replacements:
      if re.search(re.escape(word['from']), text):
        rslt.append({ 'from': word['from'], 'to': word['to'] })
      else:
        rslt.append({ 'from': word['from'], 'to': None })
  return rslt

def update_contents(filepath, replacements):
  rslt = [] 
  with open(filepath, 'r+') as fp:
    text = fp.read()
    for word in replacements:
      if re.search(re.escape(word['from']), text):
        text = re.sub(re.escape(word['from']), word['to'], text)
        rslt.append({ 'from': word['from'], 'to': word['to'] })
      else:
        rslt.append({ 'from': word['from'], 'to': None })
    fp.seek(0)
    fp.write(text)
    fp.truncate()
  return rslt

def check_replacements_format(replacements):
  if type(replacements) is not list:
    return "Replacements must be list"
  for word in replacements:
    if type(word) is not dict:
      return "Replacements must be list of dict({ 'from', 'to' })"
    if 'from' not in word or 'to' not in word:
      return "Replacements must be list of dict({ 'from', 'to' })"
  return None

def main():
  module = setup_module()
  filepath = module.params['filepath']
  replacements = module.params['replacements']
  should_change = not module.check_mode
  msg = 'Not Changed'
  bkup = None
  rslt = None
  if not os.path.exists(filepath):
    msg = 'File Not Found: ' + filepath
    module.fail_json(msg=msg) 
  err = check_replacements_format(replacements)
  if err:
    module.fail_json(msg=err) 
  if module.params['backup']:
    bkup = create_backup(filepath)
  if should_change:
    rslt = update_contents(filepath, replacements)
    msg = 'Completed'
  else:
    rslt = search_contents(filepath, replacements)
  module.exit_json(changed=should_change, msg=msg, **{ 'bkup': bkup, 'replaced': rslt })

if __name__ == '__main__':
  main()
