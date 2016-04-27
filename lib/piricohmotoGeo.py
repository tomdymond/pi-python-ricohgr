#!/usr/bin/env python

import requests
import os
import sys
import datetime

class Geo(object):
  def __init__(self, device):
    self.device = device

  def get_geo_payload_from_google(self):
    """ Retrive information on the location from google """
    a = requests.get('http://maps.googleapis.com/maps/api/geocode/json?latlng={},{}&sensor=true'.format(gpsd.fix.latitude, gpsd.fix.longitude)).json()

  def get_current_location(self):
    """ Return timestamp and current location """
    timestamp = datetime.datetime.now().strftime('%s')
    return [timestamp]