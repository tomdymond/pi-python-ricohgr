#!/usr/bin/env python
""" 
Geotag script 
"""

from os import sys, path, mkdir

cwd = path.dirname(path.abspath(__file__))
sys.path.append('{}/lib/'.format(cwd))
sys.path.append('{}/../lib/'.format(cwd))

from piricohmotoCamera import Camera

flow = Camera(config_file='/config/piricohmoto.yml')
while True:
  flow.geotag_all()
  sleep(30)
  