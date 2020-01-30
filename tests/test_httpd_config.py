
from mock import MagicMock, patch
import pytest

import tests.helper
from tests.helper import create_ansible_module

from lib.httpd_config import extract_virtualhosts
from lib.httpd_config import main

CONF = './tests/data/httpd.conf'

EXPECTED_HOSTS = [
  {'root': '/var/www/html/odo', 'name': 'odo.example.com'},
  {'alias': 'www.vvv.example.com', 'root': '/var/www/html/odo', 'name': 'vvv.example.com'},
  {'alias': 'www.yyy.example.com', 'root': '/var/www/html/odo', 'name': 'yyy.example.com'},
  {'alias': 'www.sss.example.com', 'name': 'sss.example.com'},
  {'alias': 'www.abc.example.com', 'root': '/var/www/html/abc', 'name': 'abc.example.com'},
  {'alias': 'www.bbb.example.com', 'root': '/var/www/html/bbb', 'name': 'bbb.example.com'},
  {'alias': 'www.eeee.example.com', 'root': '/var/www/html/eeee', 'name': 'eeee.example.com'},
  {'alias': 'www.tag.example.com', 'root': '/var/www/html/tag', 'name': 'tag.example.com'},
  {'alias': 'www.hhh.example.com', 'root': '/var/www/html/hhh', 'name': 'hhh.example.com'},
  {'alias': 'www.iii.example.com', 'root': '/var/www/html/iii', 'name': 'iii.example.com'},
  {'alias': 'www.hhh.example.com', 'root': '/var/www/html/hhh', 'name': 'hhh.example.com'},
  {'alias': 'www.ppp.example.com', 'root': '/var/www/html/ppp', 'name': 'ppp.example.com'}]

def test_extract_virtualhosts():
  """
  Returns extracted document roots and server names
  """
  hosts = extract_virtualhosts(CONF)
  assert hosts == EXPECTED_HOSTS

@patch('lib.httpd_config.AnsibleModule', autospec=True)
def test_main_with_conf(mocked_class):
  """
  Returns extracted document roots and server names
  """
  module = create_ansible_module({ 'conf': CONF })
  mocked_class.return_value = module
  main()
  module.exit_json.assert_called_with(**{ 'servers': EXPECTED_HOSTS })
  module.fail_json.assert_not_called()

@patch('lib.httpd_config.AnsibleModule', autospec=True)
def test_main_with_nonexistent_conf(mocked_class):
  """
  Returns error message
  """
  module = create_ansible_module({ 'conf': 'NONEXISTENT' })
  mocked_class.return_value = module
  main()
  module.exit_json.assert_not_called()
  module.fail_json.assert_called_with(**{ 'msg': 'File Not Found: NONEXISTENT' })

@patch('lib.httpd_config.AnsibleModule', autospec=True)
@patch('lib.httpd_config.os.path.exists', autospec=True)
def test_main_without_conf(os_path_exists, mocked_class):
  """
  Returns error message
  """
  module = create_ansible_module()
  mocked_class.return_value = module
  os_path_exists.return_value = False
  main()
  os_path_exists.assert_called_with('/etc/httpd/conf/httpd.conf')
  module.exit_json.assert_not_called()
  module.fail_json.assert_called_with(**{ 'msg': 'File Not Found: /etc/httpd/conf/httpd.conf' })
