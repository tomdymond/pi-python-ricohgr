#!/usr/bin/env python

import requests
import os
import sys
import datetime
from piricohmotoConfig import Config
from piricohmotoImage import Image

class RicohImage(Image):
  def __init__(self, filename):
    super(self.__class__, self, filename).__init__
    self.name = name
    self.filename = filename
    
  def download(self):
    
  

class Ricoh(Config):
  def __init__(self):
    super(self.__class__, self).__init__(**kwargs)
    self.ip = self.config['ip']
    self.objs = requests.get('http://{ip}/_gr/objs'.format(ip=self.ip), timeout=10).json()
    self.download_dir = self.config['download_dir ']

  def listimages(self, dirname):
    """ Get the images from the camera """
    
    # This should return a list of image objects rather than just primitives
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

  def download_image(self, dirname, filename, size='full'):
    """ Download an image """
    # This function should download the photo from the camera and store it into the image class 
    
    if filename in self.state_download:
      print "Skipping {}. Already downloaded".format(filename)
      return True
      
    # Remove this try statement and kill the sys exit. not good.
    # Too much code in this function. break it up. 
    try:
      timestamp_1 = int(datetime.datetime.now().strftime('%s'))
      r = requests.get('http://{ip}/v1/photos/{dirname}/{filename}?size={size}'.format(ip=self.ip, dirname=dirname, filename=filename, size=size), timeout=10)
      with open('{}/{}'.format(self.download_dir, filename), 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
          if chunk: # filter out keep-alive new chunks
            f.write(chunk)
      timestamp_2 = int(datetime.datetime.now().strftime('%s'))
      self.update_state(self.state_file_download, filename)

      # This code is shit and i would expect requests is already giving me this
      size_on_disk = int(os.path.getsize('{}/{}'.format(self.download_dir, filename)))
      total_time = timestamp_2 - timestamp_1
      download_speed = ( size_on_disk / total_time )

      print "Download took {} seconds. Speed={} Bytes/s".format(total_time, download_speed)
      return True
    except Exception as e:
      print e.message
      sys.exit(1)
    return False


