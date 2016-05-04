#!/usr/bin/env python
""" 
Service for logging gps coordinates

Store the GPS coordinates in Redis under the hkey GPS for retreival later. 

"""

import logging
import time
from daemon import runner
from os import sys, path, mkdir
import datetime
from gps import *
from time import *
import time
import threading
import redis
import json

cwd = path.dirname(path.abspath(__file__))
sys.path.append('{}/lib/'.format(cwd))
sys.path.append('{}/../lib/'.format(cwd))


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
    self.stdout_path = '/dev/null'
    self.stderr_path = '/dev/null'
    if not path.exists('/var/run/piricohmoto/'):
      mkdir('/var/run/piricohmoto/')
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
          localtime = datetime.datetime.now().strftime('%s')
          r.hmset('GPS', {localtime: json.dumps(gpsp.gpsd.fix.__dict__)})

        logger.debug("Debug message")
        logger.info("Info message")
        logger.warn("Warning message")
        logger.error("Error message")
        time.sleep(self.sleep_time)

    except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
      print ("\nKilling Thread...")
      gpsp.running = False
      gpsp.join() # wait for the thread to finish what it's doing
    print ("Done.\nExiting.")

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
