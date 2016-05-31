#!/usr/bin/env python
""" 
Service for logging gps coordinates

Store the GPS coordinates in Redis under the hkey GPS for retreival later. 

"""

import logging
import time
from os import sys, path, mkdir
import datetime
from gps import *
from time import *
import time
import threading
import json


cwd = path.dirname(path.abspath(__file__))
sys.path.append('{}/lib/'.format(cwd))
sys.path.append('{}/../lib/'.format(cwd))

from piricohmotoConfig import Data
from piricohmotoNotifier import Notifier

data = Data()

class GpsPoller(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    self.gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
    self.current_value = None
    self.running = True #setting the thread running to true

  def run(self):
    while self.running:
      self.gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer

gpsp = GpsPoller() # create the thread
n = Notifier()
try:
  gpsp.start() # start it up
  while True:

    if gpsp.gpsd.fix.latitude:
      n.status_payload(0005)
      localtime = datetime.datetime.now().strftime('%s')
      data.create_new_gpsrecord(localtime, gpsp.gpsd.fix.__dict__):
    else:
      n.status_payload(1005)
    time.sleep(5)

except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
  print ("\nKilling Thread...")
  gpsp.running = False
  gpsp.join() # wait for the thread to finish what it's doing
print ("Done.\nExiting.")

