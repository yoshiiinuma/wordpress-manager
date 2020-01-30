
import os
from mock import patch
import pytest

import tests.helper
from tests.helper import create_ansible_module, restore_file

from lib.file_contents_update import create_backup, \
                                     search_contents, \
                                     update_contents, \
                                     check_replacements_format, \
                                     main

DATADIR = './tests/data'
SAVE = DATADIR + '/orig.wp-config.php'
CONF = DATADIR + '/wp-config.php'

def test_create_backup():
  bkup = create_backup(CONF)
  assert os.path.exists(bkup)
  os.remove(bkup)

def test_search_contents():
  search = [
    {'from':"define('DB_USER', 'wordpress_user')", 'to':"define('DB_USER', 'wpusr_xxx')"},
    {'from':"define('DB_PASSWORD', 'wordpress_pass')", 'to':"define('DB_PASSWORD', 'wpass_xxx')"},
    {'from':"define('NOTEXIST', 'xxxxxx')", 'to':"define('EXIST', 'yyyyyy'"}
  ]
  rslt = search_contents(CONF, search)
  assert rslt == [
    {'from':"define('DB_USER', 'wordpress_user')", 'to':"define('DB_USER', 'wpusr_xxx')"},
    {'from':"define('DB_PASSWORD', 'wordpress_pass')", 'to':"define('DB_PASSWORD', 'wpass_xxx')"},
    {'from':"define('NOTEXIST', 'xxxxxx')", 'to': None}
  ]

def test_update_contents():
  replace = [
    {'from':"define('DB_USER', 'wordpress_user')", 'to':"define('DB_USER', 'wpusr_xxx')"},
    {'from':"define('DB_PASSWORD', 'wordpress_pass')", 'to':"define('DB_PASSWORD', 'wpass_xxx')"},
    {'from':"define('NOTEXIST', 'xxxxxx')", 'to':"define('EXIST', 'yyyyyy'"}
  ]
  rslt = update_contents(CONF, replace)
  assert rslt == [
    {'from':"define('DB_USER', 'wordpress_user')", 'to':"define('DB_USER', 'wpusr_xxx')"},
    {'from':"define('DB_PASSWORD', 'wordpress_pass')", 'to':"define('DB_PASSWORD', 'wpass_xxx')"},
    {'from':"define('NOTEXIST', 'xxxxxx')", 'to': None}
  ]
  search = [
    {'from':"define('DB_USER', 'wpusr_xxx')", 'to':"define('DB_USER', 'wpusr_xxx')"},
    {'from':"define('DB_PASSWORD', 'wpass_xxx')", 'to':"define('DB_PASSWORD', 'wpass_xxx')"},
  ]
  rslt = search_contents(CONF, search)
  assert rslt == search
  restore_file(SAVE, CONF)

def test_check_replacements_format():
  """
  Returns None if inputs is list of { 'from', 'to' }
  """
  inputs = ({'from':'a', 'to':'A'}, {'from':'b', 'to':'B'}, {'from':'c', 'to':'C'})
  assert check_replacements_format(inputs)

def test_check_replacements_format_with_empty_list():
  """
  Returns None if inputs is list of { 'from', 'to' }
  """
  inputs = ()
  assert check_replacements_format(inputs)

def test_check_replacements_format_with_invalid_list_entry():
  """
  Returns err message if any input is not { 'from', 'to' }
  """
  exp = "Replacements must be list of dict({ 'from', 'to' })"
  inputs = ["{'from':'a', 'to':'A'}", "{'from':'b', 'to':'B'}"]
  assert check_replacements_format(inputs) == exp
  inputs = [{'from':'a', 'to':'A'}, {'from':'b', 'XXX':'B'}]
  assert check_replacements_format(inputs) == exp

def test_check_replacements_format_with_none_list():
  """
  Returns err message if any input is not list
  """
  exp = "Replacements must be list"
  inputs = "{'from':'a', 'to':'A'}, {'from':'b', 'XXX':'B'}"
  assert check_replacements_format(inputs) == exp

