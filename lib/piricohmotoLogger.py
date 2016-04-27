#!/usr/bin/env python
""" 
Service for logging gps coordinates

"""

import logging
import time
from daemon import runner
from os import sys, path
import datetime

cwd = path.dirname(path.abspath(__file__))
sys.path.append('{}/lib/'.format(cwd))
sys.path.append('{}/../lib/'.format(cwd))
from piricohmotoGpslogger import GpsPoller

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
    try:
      gpsp.start() # start it up
      while True:
        if gpsd.fix.latitude:
          d = gpsd.fix.__dict__
          d['localtime'] = datetime.datetime.now().strftime('%s')
          if not path.exists(LOGGER_FILE):
            with open(LOGGER_FILE, 'wb') as f:
              w = csv.DictWriter(f, gpsd.fix.__dict__.keys())
              w.writeheader()
              w.writerow(gpsd.fix.__dict__)
          else:
            with open(LOGGER_FILE, 'ab') as f:
              w = csv.DictWriter(f, gpsd.fix.__dict__.keys())
              w.writerow(gpsd.fix.__dict__)

        logger.debug("Debug message")
        logger.info("Info message")
        logger.warn("Warning message")
        logger.error("Error message")
        time.sleep(self.sleep_time)

    except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
      print "\nKilling Thread..."
      gpsp.running = False
      gpsp.join() # wait for the thread to finish what it's doing
    print "Done.\nExiting."

if __name__ == "__main__":
  if len(sys.argv) > 2:
    sleep_time = int(sys.argv[2])
  else:
    sleep_time = 60
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
