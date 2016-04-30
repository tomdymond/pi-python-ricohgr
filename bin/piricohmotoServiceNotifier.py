#!/usr/bin/env python
"""
For now, a simple endpoint to display visual status of my Pi. It's a start...
"""

import piglow
import time
import threading

from flask import Flask
app = Flask(__name__)

class Notifier(threading.Thread):
  def __init__(self, colour='green', flashing=True, power=100):
    threading.Thread.__init__(self)
    self.colour = colour
    self.running = True
    self.piglow = piglow
    self.flashing = flashing
    self.power = power
    self.event= True

  def stop(self):
    self.running=False
    self.piglow.clear()
    self.piglow.show()

  def run(self):
    """ Make it start """
    print "run"
    while self.running:
      if self.flashing:
        self.piglow.clear()
        self.piglow.show()
        time.sleep(0.5)

      if self.event or self.flashing:
        if self.colour not in ['red', 'green', 'blue', 'yellow', 'orange']:
          self.colour = 'red'
        self.piglow.clear()
        self.piglow.colour(self.colour, self.power)
        self.piglow.show()
        self.event = False
      time.sleep(0.5)


@app.route('/piglow/<colour>/<colourstate>')
def change_colour(colour, colourstate):
  if colourstate == 'flashing':
    a.flashing = True
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
    print "\nKilling Thread..."
    a.running = False
    a.join() # wait for the thread to finish what it's doing
  print "Done.\nExiting."