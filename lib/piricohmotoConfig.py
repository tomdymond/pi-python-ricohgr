#!/usr/bin/env python
# piricohmotoConfig.py

import yaml
import os
import sys
import json
from piricohmotoNotifier import Notifier
import redis

class Data(object):
  def __init__(self):
    self.r = redis.StrictRedis(host='localhost')

  def image_exists(self, key):
    return self.r.hexists('IMAGES', key)

  def gpskey_exits(self, key):
    return self.r.hexists('GPSKEYS', key)

  def get_key(self, key):
    return self.r.get(key)

  def set_key(self, key, value):
    return self.r.set(key, value)

  def unpack(self, key, filename):
    return json.loads(self.r.hget(key, filename))

  def repack(self, key, filename, data):
    return self.r.hmset(key, {filename: json.dumps(data)})

  def remove_image(self, filename):
    return self.r.hdel('IMAGES', filename)

  def create_new_image(self, filename):
    return self.r.hmset('IMAGES', {filename: json.dumps({'UPLOAD': False, 'GPS': {}})})

  def create_new_gpskey(self, gpskey, data):
    return self.r.hmset('GPSKEYS', {gpskey: json.dumps(data) })

  def create_new_gpsrecord(self, key, data):
    return self.r.hmset('GPS', {key: json.dumps(data) })

  def get_hkeys(self, key):
    return self.r.hkeys('GPS')
    self.redis_connection.hgetall('IMAGES').keys()

class Config(object):
  def __init__(self, **kwargs):
    self.config = self.load_config(kwargs['config_file'])
    self.config_file = kwargs['config_file']
    self.notify = Notifier()
    self.data = Data()

  def load_config(self, config_file):
    """ Load config """
    if os.path.exists(config_file):
      with open(config_file) as config:
        config = yaml.load(config)
      return config
    else:
      print ("Cannot find config file. Create one and copy it to /etc/piricohmoto.yml")
      sys.exit(1)

