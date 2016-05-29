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
  
  conn = flow.connection()
  try:
    if conn.is_camera_on():
      conn.notify.green()
      if conn.connect_to_camera_ssid():
        flow.download_all()
    else:
      if conn.get_current_ssid():
        print "Connected to a SSID at least : {}".format(conn.get_current_ssid())
        conn.notify.orange()
        conn.restart_connection()
      else:
        print "Not connected to ANY ssid. So restart wpa_supplicant"
        conn.restart_wpasupplicant()
        
  except Exception as e:
    print e.message

flow = Ricoh(config_file='/config/piricohmoto.yml')
while True:
  do_everything()
  sleep(30)