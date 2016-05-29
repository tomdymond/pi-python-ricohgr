#!/usr/bin/env python
""" 
Main service 
"""

import logging
import time
from time import sleep
from os import sys, path, mkdir
import datetime
from time import *
import os
import threading

cwd = path.dirname(path.abspath(__file__))
sys.path.append('{}/lib/'.format(cwd))
sys.path.append('{}/../lib/'.format(cwd))

from piricohmotoRicoh import Ricoh

class Download_all(threading.Thread):
  def __init__(self, flow):
    print "download all "
    threading.Thread.__init__(self)
    self.flow = flow
    self.running = True

  def run(self):
    """ Make it start """
    print "make it start"
    self.flow.download_all()

class Tag_all(threading.Thread):
  def __init__(self, flow):
    threading.Thread.__init__(self)
    self.flow = flow
    self.running = True

  def run(self):
    """ Make it start """
    self.flow.geotag_all()

class Upload_all(threading.Thread):
  def __init__(self, flow):
    threading.Thread.__init__(self)
    self.flow = flow
    self.running = True

  def run(self):
    """ Make it start """
    self.flow.upload_all()


def do_everything():
  conn = flow.connection()

  try:
    #b = Tag_all(flow)
    #b.start()


    if conn.is_camera_on():
      conn.notify.green()
      if conn.connect_to_camera_ssid():
        a = Download_all(flow)
        a.start()
    else:
      conn.notify.blue()
      if conn.get_current_ssid:
        conn.notify.red()
      else:
        conn.restart_connection()
        # c = Upload_all(flow)
        # c.start()

  except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
    print ("\nKilling Threads...")
    a.running = False
    b.running = False
    c.running = False
    a.join() # wait for the thread to finish what it's doing
    b.join() # wait for the thread to finish what it's doing
    c.join()
  print ("Done.\nExiting.") 


flow = Ricoh(config_file='/config/piricohmoto.yml')
while True:
  do_everything()
  sleep(30)


