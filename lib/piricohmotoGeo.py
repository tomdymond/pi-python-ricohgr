#!/usr/bin/env python
# piricohmotoGeo.py

import requests
import os
import sys
import datetime
import redis
import json
from piricohmotoConfig import Config

class Geo(Config):
  def __init__(self, **kwargs):
    Config.__init__(self, **kwargs)
    self.timestamp = kwargs['image_timestamp']

  def get_geo_payload_from_google(self, latitude, longitude):
    """ Retrive information on the location from google """
    a = requests.get('http://maps.googleapis.com/maps/api/geocode/json?latlng={},{}&sensor=true'.format(latitude, longitude)).json()

  def _get_nearest_number(self, image_timestamp, numberlist):
    """ From list of numbers, return the closest number """
    best = 999999999
    best_time = None
    print "numberlist={}".format(numberlist)
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
    return json.loads(r.hget('GPS', timestamp))
