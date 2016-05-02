#!/usr/bin/env python
# piricohmotoImage.py

import requests
from piricohmotoGeo import Geo
from piricohmotoConfig import Config
from piricohmotoExif import Exif
import dropbox
import redis

class Image(Config):
  def __init__(self, **kwargs):
    Config.__init__(self, **kwargs)
    self.filename = kwargs['filename']
    self.access_token = self.config['access_token']
    self.download_dir = self.config['download_dir']

  def upload_to_dropbox(self):
    """ Upload the picture to dropbox """
    try:
      print ("Uploading photo {} to dropbox".format(self.filename))
      client = dropbox.client.DropboxClient(self.access_token)
      f = open('{}/{}'.format(self.download_dir, self.filename), 'rb')
      response = client.put_file('/{}'.format(self.filename), f)
      print ("uploaded:", response)
      # Share it
      response = client.share('/{}'.format(filename), short_url=False)
      r = redis.StrictRedis(host='localhost')
      j = json.loads(r.hget('IMAGES', self.filename))
      j['UPLOAD'] = True
      r.hmset('IMAGES', {self.filename: json.dumps(j)})
      return True
    except Exception as e:
      print (e.message)
    return False

  def is_uploaded(self):
    r = redis.StrictRedis(host='localhost')
    j = json.loads(self.redis_connection.hget('IMAGES', self.filename))
    if j['UPLOAD']:
      return True
    return False

  def is_downloaded(self):
    """ Bool. If the image is already downloaded """
    r = redis.StrictRedis(host='localhost')
    return r.hexists('IMAGES', self.filename)

  def size(self):
    """ Return image size """
    return int(os.path.getsize('{}/{}'.format(self.download_dir, filename)))

  def exifdata(self):
    """ Return exif data """
    exif = Exif(self.filename)
    return exif

  def geodata(self):
    """ Return geo data """
    r = redis.StrictRedis(host='localhost')
    j = json.loads(r.hget('IMAGES', self.filename))
    location = j['GPS']
    if not location:
      exif = exifdata()
      image_timestamp = exif.get_taken_time()
      geo = Geo(image_timestamp)
      location = geo.get_current_location()
      j['GPS'] = location
      r.hmset('IMAGES', {self.filename: json.dumps(j)})
    return location

  def geotag_image(self):
    """ Attempt to geo tag photo """
    geo_data = self.geodata()
    exif = exifdata()
    latitude = geo_data['latitude']
    longitude = geo_data['longitude']
    exif.set_gps_location(self.filename, latitude, longitude)
      