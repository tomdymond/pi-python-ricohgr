#!/usr/bin/env python

import requests
import os
import sys
import datetime
from piricohmotoGeo import Geo
import dropbox
import yaml

# Register the files already uploaded. Mark them in database to they 
# don't get downloaded from the camera again but also not uploaded again

STATE_FILE_DOWNLOAD='/tmp/state'
STATE_FILE_UPLOAD='/tmp/state_upload'
DOWNLOAD_DIR='/tmp'

class Grimage(object):
  def __init__(self, config_file='/etc/piricohmoto.yml'):
    self.state_download = self.read_state(STATE_FILE_DOWNLOAD)
    self.state_upload = self.read_state(STATE_FILE_UPLOAD)
    self.geodata = Geo("foo")
    self.config = self.load_config(config_file)
    self.ip = self.config['ip']
    self.access_token = self.config['access_token']
    self.objs = requests.get('http://{ip}/_gr/objs'.format(ip=self.ip), timeout=10).json()

  def load_config(self, config_file):
    """ Load config """
    if os.path.exists(config_file):
      with open(config_file) as config:
        config = yaml.load(config)
      return config
    else:
      print "Cannot find config file. Create one and copy it to /etc/piricohmoto.yml"
      sys.exit(1)

  def listimages(self, dirname):
    """ Get the images from the camera """
    f = []
    files = []
    for i in self.objs['dirs']:
      if i['name'] == dirname:
        for image_file in i['files']:
          if image_file['n'].split('.')[1] == 'JPG':
            files.append(image_file)
        f.append(files)
    return f

  def listdirs(self):
    """ Return the list of directories on the SD card """
    d = []
    for i in self.objs['dirs']:
      d.append(i['name'])
    return d

  def getimage(self, dirname, filename, size='full'):
    """ Download an image """
    if filename in self.state_download:
      print "Skipping {}. Already downloaded".format(filename)
      return True
    try:
      timestamp_1 = int(datetime.datetime.now().strftime('%s'))
      r = requests.get('http://{ip}/v1/photos/{dirname}/{filename}?size={size}'.format(ip=self.ip, dirname=dirname, filename=filename, size=size), timeout=10)
      with open('{}/{}'.format(DOWNLOAD_DIR, filename), 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
          if chunk: # filter out keep-alive new chunks
            f.write(chunk)
      timestamp_2 = int(datetime.datetime.now().strftime('%s'))
      self.update_state(STATE_FILE_DOWNLOAD, filename)

      # This code is shit and i would expect requests is already giving me this
      size_on_disk = int(os.path.getsize('{}/{}'.format(DOWNLOAD_DIR, filename)))
      total_time = timestamp_2 - timestamp_1
      download_speed = ( size_on_disk / total_time )

      print "Download took {} seconds. Speed={} Bytes/s".format(total_time, download_speed)
      return True
    except Exception as e:
      print e.message
      sys.exit(1)
    return False

  def upload_image_to_dropbox(self, filename):
    """ Upload the picture to dropbox """
    try:
      print "Uploading photo {} to dropbox".format(filename)
      client = dropbox.client.DropboxClient(self.access_token)
      f = open('{}/{}'.format(DOWNLOAD_DIR, filename), 'rb')
      response = client.put_file('/{}'.format(filename), f)
      #print "uploaded:", response
      # Share it
      # response = client.share('/{}'.format(filename), short_url=False).
      self.update_state(STATE_FILE_UPLOAD, filename)
      return True
    except Exception as e:
      print e.message
    return False

  def get_gps_data(self, image_timestamp):
    """ Return a hash with all the tags gps related for this time """
    return self.geodata(image_timestamp)

  def geotag_image(self, image_file):
    """ Attempt to geo tag photo """
    a = Grimageexif(image_file)
    image_timestamp = a.get_taken_time()
    gps_data = self.get_gps_data(image_timestamp)
    a.write_gps_data(gps_data)

  def download_all(self):
    """ Download all images """
    for foldername in self.listdirs():
      for i in self.listimages(foldername):
        for j in i:
          filename = j['n']
          print filename
          self.getimage(foldername, filename)
          self.geotag_image(filename)

  def upload_all(self):
    """ Upload all images if jpeg """
    for f in state_download:
      if f not in self.state_upload:
        self.upload_image_to_dropbox(filename)
      print "Skipping {}. Already uploaded".format(f)

  def read_state(self, state_file):
    """ Just use a text file for now. Return a list of images """
    if os.path.exists(state_file):
      with open(state_file, 'r') as f:
        return f.read().split('\n')
    else:
      return []

  def update_state(self, state_file, image):
    """ Register what's been download """
    try:
      with open(state_file, 'ab') as f:
        f.write("{}\n".format(image))
      return True
    except Exception as e:
      print e.message
    return False
