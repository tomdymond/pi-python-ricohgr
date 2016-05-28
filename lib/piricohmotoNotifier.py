#!/usr/bin/env python

import requests
import json

class Notifier(object):
    def __init__(self, power=100, duration=100, flashing=False):
        self.power = power
        self.payload = None
        self.duration = duration
        self.flashing = flashing
        self.led_codes = {
            'red': [1, 7, 13],
            'orange': [2, 8, 14],
            'yellow': [3, 9, 15],
            'green': [4, 10, 16],
            'blue': [5, 11, 17],
            'white': [6, 12, 18]
        }

    def make_payload(self, colour):
        payload = []
        for i in self.led_codes[colour]:
            payload.append(
                [self.flashing, i, self.power, self.duration]
                )
        self.payload=payload

    def led(self, leds):
        payload = []
        for i in leds:
            payload.append(
                [self.flashing, i, self.power, self.duration]
                )
        self.payload=payload

    def red(self):
        self.make_payload('red')

    def orange(self):
        self.make_payload('orange')

    def yellow(self):
        self.make_payload('yellow')

    def green(self):
        self.make_payload('green')

    def blue(self):
        self.make_payload('blue')

    def white(self):
        self.make_payload('white')

    def send(self):
        for p in self.payload:
            if p[0] == True:
                p[0] == 1
            else:
                p[0] == 0
            requests.post('http://127.0.0.1:5000', json=json.dumps(p))

a = Notifier()
a.led([1,2,3,4])
a.flashing=True
a.send()