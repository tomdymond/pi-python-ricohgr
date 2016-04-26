#! /usr/bin/python
# THIS IS NOT THE ORIGINAL DAN MANDLE SCRIPT. I'M CHANGING IT TO SUIT MY NEEDS
# ORIGINAL SCRIPT HERE: http://www.danmandle.com/blog/getting-gpsd-to-work-with-python/
# License: GPL 2.0

import os
from gps import *
from time import *
import time
import threading
import csv

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


if __name__ == '__main__':
  gpsp = GpsPoller() # create the thread
  try:
    gpsp.start() # start it up
    while True:
      if gpsd.fix.latitude:
        d = {}
        d['time'] = gpsd.fix.time
        d['latitude'] = gpsd.fix.latitude
        d['longitude'] = gpsd.fix.longitude
        d['altitude'] = gpsd.fix.altitude
        d['eps'] = gpsd.fix.eps
        d['epx'] = gpsd.fix.epx
        d['epv'] = gpsd.fix.epv
        d['ept'] = gpsd.fix.ept
        d['speed'] = gpsd.fix.speed
        d['climb'] = gpsd.fix.climb
        d['track'] = gpsd.fix.track
        d['mode'] = gpsd.fix.mode
        d['sats'] = gpsd.satellites
        d['utc'] = gpsd.utc

        with open(LOGGER_FILE, 'ab') as f:
          w = csv.DictWriter(f, d.keys())
          w.writeheader()
          w.writerow(d)

      time.sleep(REFRESH_TIME) 

  except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
    print "\nKilling Thread..."
    gpsp.running = False
    gpsp.join() # wait for the thread to finish what it's doing
  print "Done.\nExiting."