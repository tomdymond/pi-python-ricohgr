#!/usr/bin/env python

import yaml
import os
import sys

class Config(object):
  def __init__(self, config_file='/etc/piricohmoto.yml'):
    self.config = self.load_config(config_file)

  def load_config(self, config_file):
    """ Load config """
    if os.path.exists(config_file):
      with open(config_file) as config:
        config = yaml.load(config)
      return config
    else:
      print "Cannot find config file. Create one and copy it to /etc/piricohmoto.yml"
      sys.exit(1)

