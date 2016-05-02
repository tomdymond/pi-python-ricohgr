#!/usr/bin/env python

import os
import threading

cwd = os.path.dirname(os.path.abspath(__file__))
os.sys.path.append('{}/lib/'.format(cwd))
os.sys.path.append('{}/../lib/'.format(cwd))

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

flow = Ricoh(config_file='/etc/piricohmoto.yml')

conn = flow.connection()

try:
  b = Tag_all(flow)
  b.start()

  if conn.is_camera_on():
    if conn.connect_to_camera_ssid():
      a = Download_all(flow)
      a.start()

except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
  print ("\nKilling Threads...")
  a.running = False
  b.running = False
  a.join() # wait for the thread to finish what it's doing
  b.join() # wait for the thread to finish what it's doing
print ("Done.\nExiting.")


#  flow.upload_all()