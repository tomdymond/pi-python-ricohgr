#!/usr/bin/env python
# piricohmotoGeo.py

import requests
import os
import sys
import datetime
import redis
import json
from piricohmotoConfig import Config
import base64



class Geo(Config):
  def __init__(self, **kwargs):
    Config.__init__(self, **kwargs)
    self.timestamp = kwargs['image_timestamp']




  def _get_nearest_number(self, image_timestamp, numberlist):
    """ From list of numbers, return the closest number """
    best = 999999999
    best_time = None
    #print "numberlist={}".format(numberlist)
    for gps_timestamp in numberlist:
      time_diff = (int(gps_timestamp) - int(image_timestamp))
      #print "time_diff={}".format(time_diff)
      if time_diff < 0:
        time_diff = time_diff * -1
      if time_diff < best:
        best = time_diff
        best_time = gps_timestamp
    return best_time

  def get_current_location(self):
    """ Return timestamp and current location """
    print "get_current_location()"
    r = redis.StrictRedis(host='localhost')
    time_keys = r.hkeys('GPS')
    
    print "self_timestamp={}".format(self.timestamp)
    timestamp = self._get_nearest_number(self.timestamp, time_keys)
    print "closest timestamp is {}".format(timestamp)
    #print r.hget('GPS', timestamp)
    location = json.loads(r.hget('GPS', timestamp))
    try:
      int(location['latitude'])
      int(location['longitude'])
    except Exception as e:
      location['latitude'] = float(0)
      location['longitude'] = float(0)
      print "Invalid GPS data. Replacing with 0 values"
    return location


