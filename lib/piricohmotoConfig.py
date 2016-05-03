#!/usr/bin/env python
# piricohmotoConfig.py

import yaml
import os
import sys

class Config(object):
  def __init__(self, **kwargs):
    self.config = self.load_config(kwargs['config_file'])
    self.config_file = kwargs['config_file']

  def notify(self, colour, duration=5, flashing=False):
    """ Send a request to the notificatin daemon """
    if flashing:
      c = 'flashing'
    else
      c = 'fixed'
    try:
      response = requests.get('http://127.0.0.1/piglow/{}/{}/{}'.format(colour, c, duration))
      if response.status_code == 200:
        return True
      return False
    except Exception as e:
      return False

  def load_config(self, config_file):
    """ Load config """
    if os.path.exists(config_file):
      with open(config_file) as config:
        config = yaml.load(config)
      return config
    else:
      print ("Cannot find config file. Create one and copy it to /etc/piricohmoto.yml")
      sys.exit(1)

