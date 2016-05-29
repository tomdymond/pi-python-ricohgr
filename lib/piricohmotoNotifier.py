#!/usr/bin/env python

import requests
import json

class Notifier(object):
    def __init__(self, power=100, duration=100, flashing=0):
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
        self.status_codes = {
            # description, colour, led position, flashing, power, duration
            0001: ['Internet connected',      'white',    0, 0, 100, 999],
            0002: ['Camera connected',        'green',    0, 0, 100, 999],
            0003: ['SSID connected',          'blue',     0, 0, 100, 100],
            0004: ['UNASSIGNED',              'red',      0, 0, 100, 100],
            0005: ['GPS satellites found',    'yellow',   0, 0, 100, 100],
            0006: ['Downloading photos',      'orange',   0, 0, 100, 100],

            0101: ['UNASSIGNED',              'white',    1, 0,  50, 100],
            0102: ['Tagging photos',          'green',    1, 0,  50,  50],
            0103: ['Uploading photos',        'blue',     1, 0,  50,  50],
            0104: ['UNASSIGNED',              'red',      1, 0,  50,  50],
            0105: ['Geotagging',              'yellow',   1, 0,  50,  50],
            0106: ['UNASSIGNED',              'orange',   1, 0, 100,  50],

            0201: ['UNASSIGNED',              'white',    2, 0, 100, 100],
            0202: ['UNASSIGNED',              'green',    2, 0, 100, 100],
            0203: ['UNASSIGNED',              'blue',     2, 0, 100, 100],
            0204: ['UNASSIGNED',              'red',      2, 0, 100, 100],
            0205: ['UNASSIGNED',              'yellow',   2, 0, 100, 100],
            0206: ['UNASSIGNED',              'orange',   2, 0, 100, 100],

            1001: ['No internet connection',  'white',    0, 1,  50, 999], 
            1002: ['Camera not connected',    'green',    0, 1,   0, 999],
            1003: ['No SSID',                 'blue',     0, 1,  50, 100],
            1004: ['UNASSIGNED',              'red',      0, 1,  50, 100],
            1005: ['No GPS',                  'yellow',   0, 1,  50, 100],
            1006: ['Failed downloading photo','orange',   0, 1,  50, 100],

            1101: ['UNASSIGNED',              'white',    1, 1, 100, 100],
            1102: ['Failed tagging',          'green',    1, 1, 100, 100],
            1103: ['Failed uploading',        'blue',     1, 1, 100, 100],
            1104: ['UNASSIGNED',              'red',      1, 1, 100, 100],
            1105: ['UNASSIGNED',              'yellow',   1, 1, 100, 100],
            1106: ['UNASSIGNED',              'orange',   1, 1, 100, 100],

            1201: ['UNASSIGNED',              'white',    2, 1, 100, 100],
            1202: ['UNASSIGNED',              'green',    2, 1, 100, 100],
            1203: ['UNASSIGNED',              'blue',     2, 1, 100, 100],
            1204: ['UNASSIGNED',              'red',      2, 1, 100, 100],
            1205: ['UNASSIGNED',              'yellow',   2, 1, 100, 100],
            1206: ['UNASSIGNED',              'orange',   2, 1, 100, 100],

            3001: ['UNASSIGNED',              'white',    [0,1,2], 0, 100, 100], 
            3002: ['UNASSIGNED',              'green',    [0,1,2], 0, 100, 100],
            3003: ['UNASSIGNED',              'blue',     [0,1,2], 0, 100, 100],
            3004: ['CPU OK',                  'red',      [0,1,2], 0, 20,  999],
            3005: ['UNASSIGNED',              'yellow',   [0,1,2], 0, 100, 100],
            3006: ['UNASSIGNED',              'orange',   [0,1,2], 0, 100, 100],

            4001: ['UNASSIGNED',              'white',    [0,1,2], 1, 100, 100], 
            4002: ['UNASSIGNED',              'green',    [0,1,2], 1, 100, 100],
            4003: ['UNASSIGNED',              'blue',     [0,1,2], 1, 100, 100],
            4004: ['CPU OVERHEAD',            'red',      [0,1,2], 1, 200, 999],
            4005: ['UNASSIGNED',              'yellow',   [0,1,2], 1, 100, 100],
            4006: ['UNASSIGNED',              'orange',   [0,1,2], 1, 100, 100],
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

    def status_payload(self, code):
        """ Prepare a standard status code payload """
        payload = []
        description, colour, position, flashing, power, duration = self.status_codes[code]

        if type(position) == list:
            for p in position:
                led = self.led_codes[colour][p]
                payload.append(
                    [flashing, led, power, duration]
                    )
        else:
            led = self.led_codes[colour][p]
            payload.append(
                [flashing, i, power, duration]
                )
        print description
        self.payload=payload
        self.send()


    def red(self):
        self.make_payload('red')
        self.send()

    def orange(self):
        self.make_payload('orange')
        self.send()

    def yellow(self):
        self.make_payload('yellow')
        self.send()

    def green(self):
        self.make_payload('green')
        self.send()

    def blue(self):
        self.make_payload('blue')
        self.send()

    def white(self):
        self.make_payload('white')
        self.send()

    def send(self):
        for p in self.payload:
            requests.post('http://127.0.0.1:5000', json=json.dumps(p))

