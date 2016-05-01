#!/usr/bin/env python
""" Test suite for pi ricoh motorbike project """

import unittest
from mock import Mock
from os import sys, path
import yaml
import json

cwd = path.dirname(path.dirname(path.abspath(__file__)))
sys.path.append('{}/lib/'.format(cwd))

from piricohmotoRicoh import Ricoh

CONFIG_FILE = '{}/test/test-data/piricohmoto.yml'.format(cwd)

class Test(unittest.TestCase):
  """ Test stuff """

  def mock_camera_objs(self):
    """ Mock mock_stats_output """
    with open('{}/test/test-data/objs.json'.format(cwd), 'r') as f:
      return json.loads(f.read())

  def test_listdirs(self):
    """ test_listdirs """
    a = Ricoh(config_file=CONFIG_FILE)
    a.objs = self.mock_camera_objs()
    print (a.listdirs())
    self.assertTrue(a.listdirs)





