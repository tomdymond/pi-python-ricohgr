#!/usr/bin/env python

import requests
from piricohmotoGeo import Geo
from piricohmotoConfig import Config
from piricohmotoExif import Exif
import dropbox


class Image(Config):
  def __init__(self, filename):
    super(self.__class__, self).__init__(**kwargs)
    self.filename = filename
    self.access_token = self.config['access_token']
    self.download_dir = self.config['download_dir']

  def upload_image_to_dropbox(self):
    """ Upload the picture to dropbox """
    try:
      print "Uploading photo {} to dropbox".format(self.filename)
      client = dropbox.client.DropboxClient(self.access_token)
      f = open('{}/{}'.format(self.download_dir, self.filename), 'rb')
      response = client.put_file('/{}'.format(self.filename), f)
      #print "uploaded:", response
      # Share it
      # response = client.share('/{}'.format(filename), short_url=False).
      self.update_state(self.state_file_upload, self.filename)
      return True
    except Exception as e:
      print e.message
    return False

  def geotag_image(self):
    """ Attempt to geo tag photo """
    exif = Exif(self.filename)
    geodata = Geo()
    image_timestamp = exif.get_taken_time()
    gps_data = geodata(image_timestamp)
    latitude = gps_data['latitude']
    longitude = gps_data['longitude']
    exif.set_gps_location(self.filename, latitude, longitude)
      


