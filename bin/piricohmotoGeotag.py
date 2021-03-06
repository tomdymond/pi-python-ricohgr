#!/usr/bin/env python
"""
Geotag script
"""

from os import sys, path, mkdir
from time import sleep

cwd = path.dirname(path.abspath(__file__))
sys.path.append('{}/lib/'.format(cwd))
sys.path.append('{}/../lib/'.format(cwd))

from piricohmotoCamera import Camera
from piricohmotoChecks import Check


c = Check()
flow = Camera(config_file='/config/piricohmoto.yml')
while True:
  if c.check_cpu_temp()[0]:
    flow.geotag_all()
  sleep(60)

