#!/usr/bin/env python

import requests
import os
import sys
import datetime
import csv


class Geo(object):
  def __init__(self, logger_file):
    self.logger_file = logger_file
    self.logger_dict = self.read_logger_file()

  def get_geo_payload_from_google(self):
    """ Retrive information on the location from google """
    a = requests.get('http://maps.googleapis.com/maps/api/geocode/json?latlng={},{}&sensor=true'.format(gpsd.fix.latitude, gpsd.fix.longitude)).json()

  def read_logger_file(self):
    """ Return a dictionary. Key is the timestamp, value is the GPS data """
    b = {}
    with open(self.logger_file) as f:
      reader = csv.DictReader(f)
      for row in reader:
        t = row['localtime']
        b[t] = row
    return b

  def get_current_location(self, timestamp):
    """ Return timestamp and current location """
    return self.logger_dict[timestamp]
