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
import re


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

def normalise_time(timestamp):
  if timestamp:
    if re.findall('\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z', str(timestamp)):
      dt = datetime.datetime.strptime(timestamp.split('.')[0], "%Y-%m-%dT%H:%M:%S")
      dt = int(dt.strftime('%s'))
    else:
      dt = int(float(timestamp))
  return dt


gpsp = GpsPoller() # create the thread
n = Notifier()

try:
  gpsp.start() # start it up

  initial_payload = {
    'altitude': 0,
    'climb': 0,
    'epc': 0,
    'epd': 0,
    'eps': 0,
    'ept': 0,
    'epv': 0,
    'epx': 0,
    'epy': 0,
    'latitude': 0,
    'longitude': 0,
    'mode': 3,
    'speed': 0.0,
    'time': str(datetime.datetime.now().strftime('%s')),
    'track': 0
    }

  data.create_new_gpsrecord(localtime, initial_payload)

  while True:
    if gpsp.gpsd.fix.latitude:

      epochs_time_system = int(datetime.datetime.now().strftime('%s'))
      epochs_time_gps = normalise_time(gpsp.gpsd.fix.time)

      if abs(epochs_time_system - epochs_time_gps) < 5:
        n.status_payload(0005)
        data.create_new_gpsrecord(localtime, gpsp.gpsd.fix.__dict__)
      else:
        n.status_payload(1005)
    else:
      n.status_payload(1005)
    time.sleep(5)

except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
  print ("\nKilling Thread...")
  gpsp.running = False
  gpsp.join() # wait for the thread to finish what it's doing
print ("Done.\nExiting.")

