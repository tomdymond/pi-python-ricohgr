#!/usr/bin/env python
""" 
Thumbnail script 
"""

from os import sys, path, mkdir
from time import sleep

cwd = path.dirname(path.abspath(__file__))
sys.path.append('{}/lib/'.format(cwd))
sys.path.append('{}/../lib/'.format(cwd))

from piricohmotoCamera import Camera

flow = Camera(config_file='/config/piricohmoto.yml')
while True:
  flow.thumbnail_all()
  sleep(120)
  