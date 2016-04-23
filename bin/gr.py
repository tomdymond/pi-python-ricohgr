#!/usr/bin/env python

import os

cwd = os.path.dirname(os.path.abspath(__file__))
os.sys.path.append('{}/lib/'.format(cwd))
os.sys.path.append('{}/../lib/'.format(cwd))
from piricohmotoWifi import Wifishit
from piricohmoto import Grimage

a = Wifishit(camera_ssid=os.environ["RICOH_SSID"])

if a.is_camera_on():
  if a.connect_to_camera_ssid():
    b = Grimage()
    dirs = b.listdirs()
    for d in b.listdirs():
      for i in b.listimages(d):
        for j in i:
          print j['n']


