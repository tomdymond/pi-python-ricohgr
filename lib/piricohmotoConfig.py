#!/usr/bin/env python
# piricohmotoConfig.py

import yaml
import os
import sys
import requests
import json

class Config(object):
  def __init__(self, **kwargs):
    self.config = self.load_config(kwargs['config_file'])
    self.config_file = kwargs['config_file']

  def notify(self, led, duration=5, flashing=0, power=100):
    """ Send a request to the notificatin daemon """
    try:
      a=[flashing, led, power, duration]
      response = requests.post('http://127.0.0.1:5000', json=json.dumps(a))
      if response.status_code == 200:
        return True
      print response.status_code
      return False
    except Exception as e:
      print e.message
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

