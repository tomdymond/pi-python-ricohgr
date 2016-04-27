#!/usr/bin/env python

import requests
import os
import sys
import datetime
import redis

class Geo(object):
  def __init__(self):
    self.foo = 'foo'

  def get_geo_payload_from_google(self):
    """ Retrive information on the location from google """
    a = requests.get('http://maps.googleapis.com/maps/api/geocode/json?latlng={},{}&sensor=true'.format(gpsd.fix.latitude, gpsd.fix.longitude)).json()

  def get_nearest_number(self, n, numberlist):
    """ From list of numbers, return the closest number """
    best = 999999
    for i in numberlist:
      t = (i - n)-1
      if t < 0:
        t = t * -1
      if t < best:
        best = t
        best_time = i
    return best_time

  def get_current_location(self, timestamp):
    """ Return timestamp and current location """
    return self.logger_dict[timestamp]
    r = redis.StrictRedis(host='localhost')
    time_keys = r.keys()
    timestamp = self.get_nearest_number(timestamp, time_keys)
    return r.hgetall(timestamp)
