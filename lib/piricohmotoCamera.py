#!/usr/bin/env python

import requests
import os
import sys
import datetime
from piricohmotoConfig import Config

class Ricoh(Config):
  def __init__(self):
    super(self.__class__, self).__init__(**kwargs)
    self.ip = self.config['ip']
    self.objs = requests.get('http://{ip}/_gr/objs'.format(ip=self.ip), timeout=10).json()
    self.download_dir = self.config['download_dir ']
    self.state_file_download = self.config['state_file_download']
    self.state_download = self.read_state(self.state_file_download)

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

  def download_all(self):
    """ Download all images """
    for foldername in self.listdirs():
      for i in self.listimages(foldername):
        for j in i:
          filename = j['n']
          print filename
          self.getimage(foldername, filename)

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
