#!/usr/bin/env python

import os
import threading

cwd = os.path.dirname(os.path.abspath(__file__))
os.sys.path.append('{}/lib/'.format(cwd))
os.sys.path.append('{}/../lib/'.format(cwd))

from piricohmotoRicoh import Ricoh

class Download_all(threading.Thread)
  def __init__(self, flow):
    threading.Thread.__init__(self)

  def run(self):
    """ Make it start """
    flow.download_all()

class Tag_all(threading.Thread)
  def __init__(self, flow):
    threading.Thread.__init__(self)

  def run(self):
    """ Make it start """
    flow.geotag_all()

flow = Ricoh(config_file='/etc/piricohmoto.yml')

if flow.connection().is_camera_on():
  if flow.connection().connect_to_camera_ssid():
    Download_all(flow)
    Tag_all(flow)


#  flow.upload_all()