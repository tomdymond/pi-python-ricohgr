#!/usr/bin/env python


from os import sys, path, mkdir
import requests
from time import sleep

cwd = path.dirname(path.abspath(__file__))
sys.path.append('{}/lib/'.format(cwd))
sys.path.append('{}/../lib/'.format(cwd))

from piricohmotoNotifier import Notifier


def check_internet():
    n = Notifier()

    try:
        response = requests.head('http://www.google.com')
        if int(response.status_code) in (200, 302):
            return n.notify.status_payload(0001)
        else:
            return n.notify.status_payload(1001)
    except Exception as e:
        return n.notify.status_payload(1001)

while True:
    check_internet()
    sleep(30)
