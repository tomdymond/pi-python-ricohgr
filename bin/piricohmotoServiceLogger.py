#!/usr/bin/env python
""" 
Service for logging gps coordinates

"""

import logging
import time
from daemon import runner
from os import sys, path
import datetime
from gps import *
from time import *
import time
import threading
import redis
import json
import piglow

cwd = path.dirname(path.abspath(__file__))
sys.path.append('{}/lib/'.format(cwd))
sys.path.append('{}/../lib/'.format(cwd))

class Notifier(threading.Thread):
  def __init__(self, colour):
    threading.Thread.__init__(self)
    self.colour = colour
    self.piglow = piglow
    self.running = True

  def run(self):
    while self.running:
      if self.colour == 'green':
        self.piglow.green(100)
      if self.colour == 'red':
        self.piglow.red(100)
      if self.colour == 'orange':
        self.piglow.orange(100)
      if self.colour == 'blue':
        self.piglow.blue(100)
      self.piglow.show()
      time.sleep(0.5)
      self.piglow.clear()
      self.piglow.show()
      time.sleep(0.5)

class GpsPoller(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    self.gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
    self.current_value = None
    self.running = True #setting the thread running to true

  def run(self):
    while self.running:
      self.gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer

class App():
  def __init__(self, sleep_time=5):
    self.stdin_path = '/dev/null'
    self.stdout_path = '/dev/stdout'
    self.stderr_path = '/dev/stderr'
    self.pidfile_path =  '/var/run/piricohmoto/piricohmotoGpslogger.pid'
    self.pidfile_timeout = 5
    self.sleep_time = sleep_time
            
  def run(self):
    gpsp = GpsPoller() # create the thread
    r = redis.StrictRedis(host='localhost')
    try:
      gpsp.start() # start it up
      while True:
        if gpsp.gpsd.fix.latitude:
          notifier = Notifier('green')
          localtime = datetime.datetime.now().strftime('%s')
          r.hmset('GPS', {localtime: json.dumps(gpsp.gpsd.fix.__dict__)})

        logger.debug("Debug message")
        logger.info("Info message")
        logger.warn("Warning message")
        logger.error("Error message")
        time.sleep(self.sleep_time)

    except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
      print "\nKilling Thread..."
      notifier.running = False
      gpsp.running = False
      gpsp.join() # wait for the thread to finish what it's doing
    print "Done.\nExiting."

if __name__ == "__main__":
  if len(sys.argv) > 2:
    sleep_time = int(sys.argv[2])
  else:
    sleep_time = 5
  app = App(sleep_time=sleep_time)
  logger = logging.getLogger("DaemonLog")
  logger.setLevel(logging.INFO)
  formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
  handler = logging.FileHandler("/var/log/piricohmoto.log")
  handler.setFormatter(formatter)
  logger.addHandler(handler)

  daemon_runner = runner.DaemonRunner(app)

  #This ensures that the logger file handle does not get closed during daemonization
  daemon_runner.daemon_context.files_preserve=[handler.stream]
  daemon_runner.do_action()
