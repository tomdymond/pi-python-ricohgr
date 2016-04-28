#!/usr/bin/env python

import os

cwd = os.path.dirname(os.path.abspath(__file__))
os.sys.path.append('{}/lib/'.format(cwd))
os.sys.path.append('{}/../lib/'.format(cwd))
from piricohmotoWifi import Wifi
from piricohmoto import Image
from piricohmotoExif import Exif
from piricohmotoCamera import Ricoh

a = Wifi()

if a.is_camera_on():
  if a.connect_to_camera_ssid():
    b = Ricoh()
    b.download_all()

b = Image()
b.geotag_all()
b.upload_all()