#!/usr/bin/env python


from os import sys, path, mkdir
import requests
from time import sleep

cwd = path.dirname(path.abspath(__file__))
sys.path.append('{}/lib/'.format(cwd))
sys.path.append('{}/../lib/'.format(cwd))

from piricohmotoNotifier import Notifier


def check_cpu_temp():
    n = Notifier()
    os.environ['PATH'] += ':/opt/vc/bin'
    result = sh.vcgencmd('measure_temp')
    temp = float(result.stdout.rstrip().split('=')[1].split("'")[0])
    if temp > 60:
        return n.status_payload(4004)
    return n.status_payload(3004)

def check_internet():
    n = Notifier()

    try:
        response = requests.head('http://www.google.com')
        if int(response.status_code) in (200, 302):
            return n.status_payload(0001)
        else:
            return n.status_payload(1001)
    except Exception as e:
        return n.status_payload(1001)

while True:
    check_internet()
    sleep(30)
