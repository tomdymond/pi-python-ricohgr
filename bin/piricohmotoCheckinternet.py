#!/usr/bin/env python


from os import sys, path, mkdir
import requests
from time import sleep

cwd = path.dirname(path.abspath(__file__))
sys.path.append('{}/lib/'.format(cwd))
sys.path.append('{}/../lib/'.format(cwd))

from piricohmotoNotifier import Notifier

response = requests.head('http://www.google.com')
n = Notifier()
n.power=50
n.flashing=1
n.duration=2

if int(response.status_code) == 200:
    n.flashing=0

else:
    n.flashing=1

n.led([n.led_codes['white'][0]])
n.duration=20
 

n.send()

sleep(30)