#!/usr/bin/env python

import requests
import os
import sys
import datetime
from piricohmotoGeo import Geo
from piricohmotoConfig import Config
import dropbox

class Image(Config):
  def __init__(self):
    super(self.__class__, self).__init__(**kwargs)
    self.state_file_upload = self.config['state_file_upload']
    self.state_upload = self.read_state(self.state_file_upload)
    self.geodata = Geo()
    self.access_token = self.config['access_token']
    self.download_dir = self.config['download_dir']

  def upload_image_to_dropbox(self, filename):
    """ Upload the picture to dropbox """
    try:
      print "Uploading photo {} to dropbox".format(filename)
      client = dropbox.client.DropboxClient(self.access_token)
      f = open('{}/{}'.format(self.download_dir, filename), 'rb')
      response = client.put_file('/{}'.format(filename), f)
      #print "uploaded:", response
      # Share it
      # response = client.share('/{}'.format(filename), short_url=False).
      self.update_state(self.state_file_upload, filename)
      return True
    except Exception as e:
      print e.message
    return False

  def get_gps_data(self, image_timestamp):
    """ Return a hash with all the tags gps related for this time """
    print self.geodata(image_timestamp)

  def geotag_image(self, image_file):
    """ Attempt to geo tag photo """
    a = Grimageexif(image_file)
    image_timestamp = a.get_taken_time()
    gps_data = self.get_gps_data(image_timestamp)
    latitude = gps_data['latitude']
    longitude = gps_data['longitude']
    a.set_gps_location(image_file, latitude, longitude)
      
  def geotag_all(self):
    """ Upload all images if jpeg """
    for f in state_download:
      self.geotag_image(filename)

  def upload_all(self):
    """ Upload all images if jpeg """
    for f in state_download:
      if f not in self.state_upload:
        self.upload_image_to_dropbox(filename)
      print "Skipping {}. Already uploaded".format(f)

