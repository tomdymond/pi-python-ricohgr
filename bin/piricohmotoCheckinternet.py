#!/usr/bin/env python

from os import sys, path
from time import sleep

cwd = path.dirname(path.abspath(__file__))
sys.path.append('{}/lib/'.format(cwd))
sys.path.append('{}/../lib/'.format(cwd))

from piricohmotoNotifier import Notifier
from piricohmotoChecks import Checks

n = Notifier()
c = Checks()

while True:
    n.status_payload(c.check_internet()[1])
    n.status_payload(c.check_internet()[1])
    n.status_payload(c.check_cpu_temp()[1])
    n.status_payload(c.check_disk_space()[1])
    n.status_payload(c.check_usb_storage()[1])
    sleep(30)
