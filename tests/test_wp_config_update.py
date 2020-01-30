
import os
from mock import patch
import pytest

import tests.helper
from tests.helper import create_ansible_module, restore_file

from lib.file_contents_update import search_contents
from lib.wp_config_update import create_backup, \
                                 create_define_statement, \
                                 update_line, \
                                 update_conf, \
                                 main

DATADIR = './tests/data'
SAVE = DATADIR + '/orig.wp-config.php'
CONF = DATADIR + '/wp-config.php'

def test_create_backup():
  """
  Creates a backup file
  """
  bkup = create_backup(CONF)
  print(bkup)
  assert os.path.exists(bkup)
  os.remove(bkup)

def test_create_define_statement():
  """
  Create a define statement
  """
  assert create_define_statement('DB_USER', 'user') == "define('DB_USER', 'user');\n"
  assert create_define_statement('DB_COLLATE', '') == "define('DB_COLLATE', '');\n"
  assert create_define_statement('WP_DEBUG', 'true') == "define('WP_DEBUG', true);\n"
  assert create_define_statement('SITE_ID_CURRENT_SITE', 25) == "define('SITE_ID_CURRENT_SITE', 25);\n"
  assert create_define_statement('table_prefix', 'wordpress_') == "$table_prefix = 'wordpress_';\n"
  assert create_define_statement('DB_USER', 'user', ' # comments') == "define('DB_USER', 'user'); # comments\n"

def test_update_line_with_exisiting_options():
  """
  Returns updated line
  """
  rslt = { 'updated': [] }
  line = update_line("define('DB_USER', 'xxx');", {'DB_USER': 'yyy'}, rslt)
  assert line == "define('DB_USER', 'yyy');\n"
  line = update_line("$table_prefix = 'xxx_'; # zzz", {'table_prefix': 'yyy_'}, rslt)
  assert line == "$table_prefix = 'yyy_'; # zzz\n"
  line = update_line("$base = '/'; # zzz", {'base': '/yyy'}, rslt)
  assert line == "$base = '/yyy'; # zzz\n"
  assert rslt['updated'] == [
           "define('DB_USER', 'yyy');\n",
           "$table_prefix = 'yyy_'; # zzz\n",
           "$base = '/yyy'; # zzz\n"
         ]

def test_update_line_with_nonexistent_options():
  """
  Returns the original line
  """
  rslt = { 'updated': [] }
  line = update_line("define('DB_USER', 'xxx');", {'DB_PASS': 'yyy'}, rslt)
  assert line == "define('DB_USER', 'xxx');"
  assert rslt == { 'updated': [] }

def test_update_conf():
  replacement = {
    'DB_USER': 'wpusr_xxx',
    'DB_PASSWORD': 'wpass_xxx',
    'table_prefix': 'wp_xxx_',
    'base': '/xxx',
    'ZZZZ': 'zzzz'
  }

  search = [
    {'from':"define('DB_USER', 'wpusr_xxx')", 'to':"define('DB_USER', 'wpusr_xxx')"},
    {'from':"define('DB_PASSWORD', 'wpass_xxx')", 'to':"define('DB_PASSWORD', 'wpass_xxx')"},
    {'from':"$table_prefix = 'wp_xxx_';", 'to':"$table_prefix_= 'wp_xxx_';"},
    {'from':"$base = '/xxx';", 'to':"$base = '/xxx';"},
    {'from':"define('ZZZZ', 'zzzz')", 'to':"define('ZZZZ', 'zzzz')"},
  ]
  rslt = search_contents(CONF, search)
  assert rslt == [
    {'from':"define('DB_USER', 'wpusr_xxx')", 'to':None},
    {'from':"define('DB_PASSWORD', 'wpass_xxx')", 'to':None},
    {'from':"$table_prefix = 'wp_xxx_';", 'to':None},
    {'from':"$base = '/xxx';", 'to':None},
    {'from':"define('ZZZZ', 'zzzz')", 'to':None},
  ]

  rslt = update_conf(CONF, replacement)
  assert rslt['updated'] == [
    "define('DB_USER', 'wpusr_xxx');\n",
    "define('DB_PASSWORD', 'wpass_xxx');\n",
    "$table_prefix = 'wp_xxx_';\n",
    "$base = '/xxx';\n"
  ]
  assert rslt['inserted'] == [
    "define('ZZZZ', 'zzzz');\n",
  ]

  rslt = search_contents(CONF, search)
  restore_file(SAVE, CONF)
  assert rslt == search

