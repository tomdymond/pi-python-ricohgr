#!/usr/bin/env python
# piricohmotoImage.py

import requests
from piricohmotoGeo import Geo
from piricohmotoConfig import Config
from piricohmotoExif import Exif
import dropbox
import redis
import json
import os
import PIL
from PIL import Image as Image2

class Image(Config):
  def __init__(self, **kwargs):
    Config.__init__(self, **kwargs)
    self.filename = kwargs['filename']
    self.access_token = self.config['access_token']
    self.download_dir = self.config['download_dir']

  def create_smallsize(self, basewidth):
    b = self.filename.split('.')
    base_name = b[0]
    file_extension = b[1]
    newname = '{}/{}_{}.{}'.format(self.download_dir, base_name, basewidth, file_extension)
    if os.path.exists(newname):
      return True

    img = Image2.open('{}/{}'.format(self.download_dir, self.filename))
    wpercent = (basewidth / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
    img.save(newname)
    return True

  def upload_to_dropbox(self):
    """ Upload the picture to dropbox """
    r = redis.StrictRedis(host='localhost')
    try:
      print ("Uploading photo {} to dropbox".format(self.filename))
      client = dropbox.client.DropboxClient(self.access_token)
      f = open('{}/{}'.format(self.download_dir, self.filename), 'rb')
      response = client.put_file('/{}'.format(self.filename), f)
      print ("uploaded:", response)
      # Share it
      response = client.share('/{}'.format(self.filename), short_url=False)

      j = json.loads(r.hget('IMAGES', self.filename))
      j['UPLOAD'] = True
      r.hmset('IMAGES', {self.filename: json.dumps(j)})
      self.notify.status_payload(0103)
      return True
    except Exception as e:
      self.notify.status_payload(1103)
      print (e.message)
    return False

  def is_uploaded(self):
    r = redis.StrictRedis(host='localhost')
    if r.keys('IMAGES') and self.filename in r.hkeys('IMAGES'):
      j = json.loads(r.hget('IMAGES', self.filename))
      if j['UPLOAD']:
        return True
    return False

  def is_downloaded(self):
    """ Bool. If the image is already downloaded """
    r = redis.StrictRedis(host='localhost')
    if r.hexists('IMAGES', self.filename) and os.path.exists('{}/{}'.format(self.download_dir, self.filename)):
      return True
    return False

  def is_geotagged(self):
    """ Bool. If the image is already geo tagged """
    r = redis.StrictRedis(host='localhost')
    if r.hexists('IMAGES', self.filename):
      j = json.loads(r.hget('IMAGES', self.filename))
      #print j
      if j['GPS']:
        print "Image {} already geotagged".format(self.filename)
        return True
    return False

  def size(self):
    """ Return image size """
    return int(os.path.getsize('{}/{}'.format(self.download_dir, self.filename)))

  def exifdata(self):
    """ Return exif data """
    exif = Exif(config_file=self.config_file, filename=self.filename)
    return exif

  def geodata(self):
    """ Return geo data """
    r = redis.StrictRedis(host='localhost')
    j = json.loads(r.hget('IMAGES', self.filename))
    location = j['GPS']
    if not location:
      exif = self.exifdata()
      image_timestamp = exif.get_taken_time()
      geo = Geo(config_file=self.config_file, image_timestamp=image_timestamp)
      location = geo.get_current_location()
      j['GPS'] = location
      r.hmset('IMAGES', {self.filename: json.dumps(j)})
    return location

  def geotag_image(self):
    """ Attempt to geo tag photo """
    print "About to geotag {}".format(self.filename)
    geo_data = self.geodata()
    exif = self.exifdata()
    latitude = geo_data['latitude']
    longitude = geo_data['longitude']

    try:
      int(latitude)
      int(longitude)
    except Exception as e:
      latitude = float(0)
      longitude = float(0)
      print "Invalid GPS data. Replacing with 0 values"

    try:
      exif.set_gps_location(self.filename, latitude, longitude)
      self.notify.status_payload(0102)
    except Exception as e:
      self.notify.status_payload(1102)
      print e.message
      