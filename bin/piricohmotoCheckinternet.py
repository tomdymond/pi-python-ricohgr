#!/usr/bin/env python


from os import sys, path, mkdir
import requests
from time import sleep

cwd = path.dirname(path.abspath(__file__))
sys.path.append('{}/lib/'.format(cwd))
sys.path.append('{}/../lib/'.format(cwd))

from piricohmotoNotifier import Notifier


def check_internet():
    response = requests.head('http://www.google.com')
    n = Notifier()
    n.power=50

    if int(response.status_code) in (200, 302):
        n.flashing=0
    else:
        n.flashing=1

    print response.status_code
    n.duration=40
    n.led([n.led_codes['white'][0]])
    print n.payload
    n.send()

while True:
    check_internet()
    sleep(30)
