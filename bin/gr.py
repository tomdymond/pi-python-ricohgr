#!/usr/bin/env python

import os

cwd = os.path.dirname(os.path.abspath(__file__))
os.sys.path.append('{}/lib/'.format(cwd))
os.sys.path.append('{}/../lib/'.format(cwd))

from piricohmotoRicoh import Ricoh

flow = Ricoh()
connection = flow.connection()

if connection.is_camera_on():
  if connection.connect_to_camera_ssid():
    flow.download_all()

  flow.geotag_all()
  flow.upload_all()