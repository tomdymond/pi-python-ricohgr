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

  def get_geo_map_from_google(self, latitude, longitude, width=200, height=200):
    # https://maps.googleapis.com/maps/api/staticmap?center=51,0&zoom=12&size=200x200
    gps_key = self.get_gps_key(latitude, longitude)
    filename = '/download/maps/{}.JPG'.format(gps_key)
    if not os.path.exists(filename):
      reponse = requests.get('https://maps.googleapis.com/maps/api/staticmap?center={latitude},{longitude}&zoom=12&size={width}x{height}'.format(latitude=latitude, longitude=longitude))
      with open(filename), 'wb') as f:
        for chunk in reponse.iter_content(chunk_size=1024): 
          if chunk: # filter out keep-alive new chunks
            f.write(chunk)

  def get_gps_key(self, latitude, longitude):
    return base64.b64encode(str((latitude,longitude)))

  def get_geo_payload_from_google(self, latitude, longitude):
    """ Retrive information on the location from google """
    request = requests.get('http://maps.googleapis.com/maps/api/geocode/json?latlng={},{}&sensor=true'.format(latitude, longitude)).json()
    gps_key = self.get_gps_key(latitude, longitude)
    r = redis.StrictRedis(host='localhost')
    if not r.hexists('GPSKEYS', gps_key ):
      r.hmset('GPSKEYS', {gps_key: json.dumps(request.json()) })


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
    

    print "self_timestamp={}".format(self.timestamp)
    timestamp = self._get_nearest_number(self.timestamp, time_keys)
    print "closest timestamp is {}".format(timestamp)
    #print r.hget('GPS', timestamp)
    return json.loads(r.hget('GPS', timestamp))
