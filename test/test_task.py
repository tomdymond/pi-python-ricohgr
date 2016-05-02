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
from piricohmotoWifi import Wifi

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

  def test_listimages(self):
    """ test_listdirs """
    a = Ricoh(config_file=CONFIG_FILE)
    a.objs = self.mock_camera_objs()
    print (a.listimages('875RICOH'))
    self.assertTrue(a.listimages('875RICOH'))

  def test_listimages(self):
    """ test_listdirs """
    a = Ricoh(config_file=CONFIG_FILE)
    a.objs = self.mock_camera_objs()
    print (a.listimages('875RICOH'))
    self.assertTrue(a.listimages('875RICOH'))

  def test_is_camera_off(self):
    """ Test if camera is off """
    a = Wifi(config_file=CONFIG_FILE)
    a.get_ssids = Mock(return_value=['A', 'B'])
    a.get_current_ssid = Mock(return_value='A')
    print "---"
    print (a.is_camera_on())

  def test_is_camera_on(self):
    """ Test if camera is on """
    a = Wifi(config_file=CONFIG_FILE)
    a.get_ssids = Mock(return_value=['A', 'B', 'RICOH_000000'])
    a.get_current_ssid = Mock(return_value='RICOH_000000')
    print (a.is_camera_on())

  def test_connect_to_camera_ssid(self):
    """ Test connecting to camera. SSID is good already """
    a = Wifi(config_file=CONFIG_FILE)
    a.get_ssids = Mock(return_value=['A', 'B', 'RICOH_000000'])
    a.get_current_ssid = Mock(return_value='RICOH_000000')
    print (a.connect_to_camera_ssid())

  def test_connect_to_camera_ssid_2(self):
    """ Try connecting to the camera but the current SSID is not the camera """
    def side_effect(a, ssid):
      a.get_current_ssid = Mock(return_value=ssid)

    a = Wifi(config_file=CONFIG_FILE)
    a.get_ssids = Mock(return_value=['A', 'B', 'RICOH_000000'])
    a.get_current_ssid = Mock(return_value=['A'])
    a.restart_interface = Mock(return_value=True, side_effect=side_effect(a, 'RICOH_000000'))
    print (a.connect_to_camera_ssid())




