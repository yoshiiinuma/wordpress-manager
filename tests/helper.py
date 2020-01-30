
import sys
from shutil import copyfile

if sys.version_info >= (3, 3):
  from unittest.mock import MagicMock
else:
  from mock import MagicMock


#class MockAnsibleModule(object):
#  def __init__(self, **kwargs):
#    self.params = kwardgs
#
#  def exit_json(self, *args, **kwargs):
#    self.exit_args = args
#    self.exit_kwargs = kwargs
#
#  def fail_json(self, *args, **kwargs):
#    self.exit_args = args
#    self.exit_kwargs = kwargs
#    raise Exception(kwargs["XXXXX MSG XXXXX"])

def create_ansible_module(params = {}):
  #module = MockAnsibleModule(**params)
  module = MagicMock()
  module.params = params
  return module

sys.modules['ansible'] = MagicMock()
sys.modules['ansible.module_utils'] = MagicMock()
sys.modules['ansible.module_utils.basic'] = MagicMock()
#sys.modules['ansible.module_utils.basic.AnsibleModule'] = MagicMock()

def restore_file(original, target):
  copyfile(original, target)
