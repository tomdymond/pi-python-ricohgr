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
    best = 999999
    for gps_timestamp in numberlist:
      time_diff = (gps_timestamp - image_timestamp)
      if time_diff < 0:
        time_diff = time_diff * -1
      if time_diff < best:
        best = time_diff
        best_time = time_diff
    return best_time

  def get_current_location(self):
    """ Return timestamp and current location """
    r = redis.StrictRedis(host='localhost')
    time_keys = r.keys()
    timestamp = self._get_nearest_number(timestamp, time_keys)
    return json.loads(r.hget('GPS', timestamp))
