#! /usr/bin/python
# THIS IS NOT THE ORIGINAL DAN MANDLE SCRIPT. I'M CHANGING IT TO SUIT MY NEEDS
# ORIGINAL SCRIPT HERE: http://www.danmandle.com/blog/getting-gpsd-to-work-with-python/
# License: GPL 2.0

from gps import *
from time import *
import time
import threading

gpsd = None #seting the global variable

REFRESH_TIME=5
LOGGER_FILE='/tmp/gpslog'

class GpsPoller(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    global gpsd #bring it in scope
    gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
    self.current_value = None
    self.running = True #setting the thread running to true

  def run(self):
    global gpsd
    while gpsp.running:
      gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer

