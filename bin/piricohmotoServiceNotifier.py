#!/usr/bin/env python
import sys
import threading
import json
import piglow
import random
from time import sleep

from flask import Flask, request
app = Flask(__name__)

class Notifier(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    self.running = True
    self.new_map=[[[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]], [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]]

  def set_colour(self, item):
    for p, i in enumerate(self.new_map[item]):
      if i[1] < 1:
        i[0] = 0
      else:
        i[1] -= 1
      piglow.led(p, i[0])
    piglow.show()

  def run(self):
    while self.running:
      for i in [0,1]:
        self.set_colour(i)
        sleep(0.2)



@app.route('/', methods=["POST"])
def change_colour():
  r = json.loads(request.get_json(silent=True))
  n.new_map[0][r[1]] = [r[2], r[3]]
  if r[0]:
    n.new_map[1][r[1]] = [0, 0]
  else:
    n.new_map[1][r[1]] = [r[2], r[3]]
  return "GOOD"

if __name__ == '__main__':
  n = Notifier()
  n.start()

  try:
    app.run()
    n.running = False
    n.join()
  except (KeyboardInterrupt, SystemExit):
    n.running = False
    n.join()