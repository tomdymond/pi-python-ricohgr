#!/usr/bin/env python
""" 
Upload script 
"""

from os import sys, path, mkdir

cwd = path.dirname(path.abspath(__file__))
sys.path.append('{}/lib/'.format(cwd))
sys.path.append('{}/../lib/'.format(cwd))

from piricohmotoCamera import Camera
from piricohmotoChecks import Checks

c = Checks()

flow = Camera(config_file='/config/piricohmoto.yml')
while True:
  if c.check_internet()[0]
    flow.upload_all()
  sleep(30)
  