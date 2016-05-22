#!/usr/bin/env python
"""
Service for displaying certain alert conditions

colour/flashing/duration

For example http://127.0.0.1/red/flashing/1

"""

import piglow
import time
import threading
from datetime import datetime

from flask import Flask
app = Flask(__name__)

class Notifier(threading.Thread):
  def __init__(self, colour='green', flashing=True, power=100, duration=5):
    threading.Thread.__init__(self)
    self.duration = duration
    self.colour = colour
    self.running = True
    self.piglow = piglow
    self.flashing = flashing
    self.power = power
    self.event= True

  def stop(self):
    self.piglow.clear()
    self.piglow.show()
    self.running=False

  def run(self):
    """ Make it start """
    print ("run")
    time_start=int(datetime.now().strftime('%s'))
    time_actual=int(datetime.now().strftime('%s'))
    while self.running:
      time_actual=int(datetime.now().strftime('%s'))
      print "LOOP"
      if self.flashing:
        print "FLASH"
        self.piglow.clear()
        self.piglow.show()
        time.sleep(self.duration)

      if self.event or self.flashing:
        print "BEEP: EVENT IS TRUE."
        if self.colour not in ['red', 'green', 'blue', 'yellow', 'orange']:
          self.colour = 'red'
        self.piglow.clear()
        self.piglow.colour(self.colour, self.power)
        self.piglow.show()
        self.event = False
      time.sleep(self.duration)


@app.route('/piglow/<colour>/<colourstate>/<duration>')
def change_colour(colour, colourstate, duration=10):
  if colourstate == 'flashing':
    a.flashing = True
    a.duration = duration
  else:
    a.flashing = False
  a.colour=colour
  a.event=True
  return colour


if __name__ == '__main__':
  a = Notifier(flashing=False)
  try:
    a.start()
    while True:
      app.run()
  except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
    print ("\nKilling Thread...")
    a.running = False
    a.join() # wait for the thread to finish what it's doing
  print ("Done.\nExiting.")