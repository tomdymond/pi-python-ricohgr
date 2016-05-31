#!/usr/bin/env python
# piricohmotoImage.py

import requests
from piricohmotoGeo import Geo
from piricohmotoConfig import Config, Data
from piricohmotoExif import Exif
import dropbox
import json
import os
import PIL
from PIL import Image as Image2
import base64

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

    try:
      img = Image2.open('{}/{}'.format(self.download_dir, self.filename))
      wpercent = (basewidth / float(img.size[0]))
      hsize = int((float(img.size[1]) * float(wpercent)))
      img = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
      img.save(newname)
      return True
    except Exception as e:
      print "Failed to create thumbnail for {}".format(self.filename)
      os.remove('{}/{}'.format(self.download_dir, self.filename))
      Data.remove_image(self.filename)
      print e.message

  def upload_to_dropbox(self):
    """ Upload the picture to dropbox """
    try:
      print ("Uploading photo {} to dropbox".format(self.filename))
      client = dropbox.client.DropboxClient(self.access_token)
      f = open('{}/{}'.format(self.download_dir, self.filename), 'rb')
      response = client.put_file('/{}'.format(self.filename), f)
      print ("uploaded:", response)
      # Share it
      response = client.share('/{}'.format(self.filename), short_url=False)

      j = Data.unpack('IMAGES', self.filename)
      j['UPLOAD'] = True
      Data.repack('IMAGES', self.filename, j)
      self.notify.status_payload(0103)
      return True
    except Exception as e:
      self.notify.status_payload(1103)
      print (e.message)
    return False

  def is_uploaded(self):
    if self.filename in Data.get_hkeys('IMAGES'):
      j = Data.unpack('IMAGES', self.filename)
      if j['UPLOAD']:
        return True
    return False

  def is_downloaded(self):
    """ Bool. If the image is already downloaded """
    if Data.image_exists(self.filename) and os.path.exists('{}/{}'.format(self.download_dir, self.filename)):
      return True
    return False

  def is_geotagged(self):
    """ Bool. If the image is already geo tagged """
    if Data.image_exists(self.filename):
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


  def get_geo_map_from_google(self, width=200, height=200):
    """ get_geo_map_from_google """
    print "getting get_geo_map_from_google"
    geo_data = self.geodata()
    latitude = geo_data['latitude']
    longitude = geo_data['longitude']

    # https://maps.googleapis.com/maps/api/staticmap?center=51,0&zoom=12&size=200x200
    filename = '/download/maps/{}.JPG'.format(self.get_gps_key())
    if not os.path.exists(filename):
      try:
        response = requests.get('https://maps.googleapis.com/maps/api/staticmap?center={latitude},{longitude}&zoom=12&size={width}x{height}'.format(latitude=latitude, longitude=longitude, width=width, height=height), timeout=5)
      except Exception as e:
        print e.message
        return False
      with open(filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024): 
          if chunk: # filter out keep-alive new chunks
            f.write(chunk)
      return True
    else:
      print "Already have location picture for {}".format(self.filename)
    return True

  def get_gps_key(self):
    geo_data = self.geodata()
    latitude = geo_data['latitude']
    longitude = geo_data['longitude']
    return base64.b64encode(str((latitude,longitude)))

  def get_geo_payload_from_google(self):
    """ Retrive information on the location from google """
    print "getting get_geo_payload_from_google"
    geo_data = self.geodata()
    latitude = geo_data['latitude']
    longitude = geo_data['longitude']
    if not Data.gpskey_exits( self.get_gps_key() ):
      try:
        request = requests.get('http://maps.googleapis.com/maps/api/geocode/json?latlng={},{}&sensor=true'.format(latitude, longitude), timeout=5)
        Data.create_new_gpskey( self.get_gps_key(), request.json() )
        return True
      except Exception as e:
        print e.message
    print "Already retreived GPS data from google for image {}".format(self.filename)
    return False

  def geodata(self):
    """ Return geo data """
    j = Data.unpack('IMAGES', self.filename)
    location = j['GPS']
    if not location:
      exif = self.exifdata()
      image_timestamp = exif.get_taken_time()
      geo = Geo(config_file=self.config_file, image_timestamp=image_timestamp)
      location = geo.get_current_location()

      j['GPS'] = location
      Data.repack('IMAGES', self.filename, j)
    return location


  def geotag_image(self):
    """ Attempt to geo tag photo """
    print "About to geotag {}".format(self.filename)
    geo_data = self.geodata()
    exif = self.exifdata()
    latitude = geo_data['latitude']
    longitude = geo_data['longitude']



    try:
      exif.set_gps_location(self.filename, latitude, longitude)
      self.notify.status_payload(0102)
    except Exception as e:
      self.notify.status_payload(1102)
      print e.message
      