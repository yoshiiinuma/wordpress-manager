
import mock
from mock import patch
import pytest

import tests.helper
from tests.helper import create_ansible_module

from lib.wp_config import strip_quotes, \
                              extract_options, \
                              filter_options, \
                              main

DATADIR = './tests/data'
SAVE = DATADIR + '/orig.wp-config.php'
CONF = DATADIR + '/wp-config.php'

OPTIONS = {
  'WP_CACHE': 'true',
  'WPCACHEHOME': '/var/www/html/wp-content/plugins/wp-super-cache/',
  'DB_NAME': 'wordpress_database',
  'DB_USER': 'wordpress_user',
  'DB_PASSWORD': 'wordpress_pass',
  'DB_HOST': '127.0.0.1',
  'DB_CHARSET': 'utf8',
  'DB_COLLATE': '',
  'AUTH_KEY': 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
  'SECURE_AUTH_KEY': 'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
  'LOGGED_IN_KEY': 'CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC',
  'NONCE_KEY': 'DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD',
  'AUTH_SALT': 'EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE',
  'SECURE_AUTH_SALT': 'FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF',
  'LOGGED_IN_SALT': 'GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG',
  'NONCE_SALT': 'HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH',
  'table_prefix': 'wp_prefix_',
  'WPLANG': '',
  'WP_DEBUG': 'true',
  'WP_DEBUG_DISPLAY': 'false',
  'WP_DEBUG_LOG': 'true',
  'WP_AUTO_UPDATE_CORE': 'false',
  'FORCE_SSL_ADMIN': 'false',
  'WP_ALLOW_MULTISITE': 'true',
  'MULTISITE': 'true',
  'SUBDOMAIN_INSTALL': 'false',
  'DOMAIN_CURRENT_SITE': 'odo.example.com',
  'PATH_CURRENT_SITE': '/',
  'SITE_ID_CURRENT_SITE': '1',
  'BLOG_ID_CURRENT_SITE': '1',
  'ABSPATH': "dirname(__FILE__) . '/'",
}

def test_extract_options():
  """
  Extracts options from wp-config.php
  """
  options = extract_options(CONF)
  assert options == OPTIONS

def test_strip_quotes():
  """
  Strips the single quoates around the given string 
  """
  assert strip_quotes('') == ''
  assert strip_quotes("''") == ''
  assert strip_quotes("abc") == 'abc'
  assert strip_quotes("abc def ghij") == 'abc def ghij'
  assert strip_quotes("'abc'") == 'abc'
  assert strip_quotes("'abc def ghij'") == 'abc def ghij'
  assert strip_quotes("dirname(__FILE__) . '/'") == "dirname(__FILE__) . '/'"

def test_filter_options_with_all():
  """
  Returns all options 
  """
  assert filter_options('all', OPTIONS) == OPTIONS

def test_filter_options_with_db():
  """
  Returns filtered options 
  """
  assert filter_options('db', OPTIONS) == {
          'DB_NAME': 'wordpress_database',
          'DB_USER': 'wordpress_user',
          'DB_PASSWORD': 'wordpress_pass',
          'DB_HOST': '127.0.0.1',
          'DB_CHARSET': 'utf8',
          'DB_COLLATE': '',
          'table_prefix': 'wp_prefix_',
        }

def test_filter_options_with_security():
  """
  Returns filtered options 
  """
  assert filter_options('security', OPTIONS) == {
          'AUTH_KEY': 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
          'SECURE_AUTH_KEY': 'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
          'LOGGED_IN_KEY': 'CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC',
          'NONCE_KEY': 'DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD',
          'AUTH_SALT': 'EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE',
          'SECURE_AUTH_SALT': 'FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF',
          'LOGGED_IN_SALT': 'GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG',
          'NONCE_SALT': 'HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH',
        }

def test_filter_options_with_debug():
  """
  Returns filtered options 
  """
  assert filter_options('debug', OPTIONS) == {
          'WP_DEBUG': 'true',
          'WP_DEBUG_DISPLAY': 'false',
          'WP_DEBUG_LOG': 'true',
        }

def test_filter_options_with_others():
  """
  Returns filtered options 
  """
  assert filter_options('others', OPTIONS) == {
          'WP_CACHE': 'true',
          'WPCACHEHOME': '/var/www/html/wp-content/plugins/wp-super-cache/',
          'WPLANG': '',
          'WP_AUTO_UPDATE_CORE': 'false',
          'FORCE_SSL_ADMIN': 'false',
          'WP_ALLOW_MULTISITE': 'true',
          'MULTISITE': 'true',
          'SUBDOMAIN_INSTALL': 'false',
          'DOMAIN_CURRENT_SITE': 'odo.example.com',
          'PATH_CURRENT_SITE': '/',
          'SITE_ID_CURRENT_SITE': '1',
          'BLOG_ID_CURRENT_SITE': '1',
          'ABSPATH': "dirname(__FILE__) . '/'",
        }

@patch('lib.wp_config.AnsibleModule', autospec=True)
@patch('lib.wp_config.os.path.exists', autospec=True)
def test_main(os_path_exists, mocked_class):
  """
  Returns extracted wordpress options 
  """
  module = create_ansible_module({ 'root': DATADIR, 'category': 'all' })
  mocked_class.return_value = module
  os_path_exists.return_value = True
  main()
  os_path_exists.assert_has_calls([mock.call(DATADIR), mock.call(CONF)])
  module.exit_json.assert_called_with(**{ 'options': OPTIONS })
  module.fail_json.assert_not_called()

@patch('lib.wp_config.AnsibleModule', autospec=True)
@patch('lib.wp_config.os.path.exists', autospec=True)
def test_main_no_root(os_path_exists, mocked_class):
  """
  Returns DocumentRoot Not Specified
  """
  module = create_ansible_module({ 'category': 'all' })
  mocked_class.return_value = module
  os_path_exists.return_value = False
  main()
  os_path_exists.assert_not_called()
  module.exit_json.assert_not_called()
  module.fail_json.assert_called_with(**{ 'msg': 'DocumentRoot Not Specified' })

@patch('lib.wp_config.AnsibleModule', autospec=True)
@patch('lib.wp_config.os.path.exists', autospec=True)
def test_main_without_root(os_path_exists, mocked_class):
  """
  Returns Directory Not Found
  """
  module = create_ansible_module({ 'root': 'notexist', 'category': 'all' })
  mocked_class.return_value = module
  os_path_exists.return_value = False
  main()
  os_path_exists.assert_called_with('notexist')
  module.exit_json.assert_not_called()
  module.fail_json.assert_called_with(**{ 'msg': 'Directory Not Found: notexist' })

@patch('lib.wp_config.AnsibleModule', autospec=True)
@patch('lib.wp_config.os.path.exists', autospec=True)
def test_main_with_category(os_path_exists, mocked_class):
  """
  Returns extracted wordpress DB options 
  """
  module = create_ansible_module({ 'root': DATADIR, 'category': 'db' })
  mocked_class.return_value = module
  os_path_exists.return_value = True
  main()
  os_path_exists.assert_has_calls([mock.call(DATADIR), mock.call(CONF)])
  module.exit_json.assert_called_with(**{ 'options': {
      'DB_NAME': 'wordpress_database',
      'DB_USER': 'wordpress_user',
      'DB_PASSWORD': 'wordpress_pass',
      'DB_HOST': '127.0.0.1',
      'DB_CHARSET': 'utf8',
      'DB_COLLATE': '',
      'table_prefix': 'wp_prefix_'}})
  module.fail_json.assert_not_called()

