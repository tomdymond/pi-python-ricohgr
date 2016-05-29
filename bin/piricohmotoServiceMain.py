#!/usr/bin/env python
""" 
Main service 
"""

import logging
import time
from time import sleep
from os import sys, path, mkdir
import datetime
import os

cwd = path.dirname(path.abspath(__file__))
sys.path.append('{}/lib/'.format(cwd))
sys.path.append('{}/../lib/'.format(cwd))

from piricohmotoRicoh import Ricoh

def do_everything():
  """ foo """
  flow = Ricoh(config_file='/config/piricohmoto.yml')
  conn = flow.connection()
  try:
    if conn.is_camera_on():
      conn.notify.green()
      if conn.connect_to_camera_ssid():
        flow.download_all()
    else:
      conn.notify.blue()
      ssid = conn.get_current_ssid()
      if ssid:
        print "Connected to a SSID at least : {}".format(ssid)
        conn.notify.orange()
      else:
        print "Currently not connected to any SSID. restart_connection"
        conn.restart_connection()
  except Exception as e:
    print e.message

while True:
  do_everything()
  sleep(30)