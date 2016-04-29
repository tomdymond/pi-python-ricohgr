#!/usr/bin/env python

import requests
import sys
from piricohmotoImage import Image
from piricohmotoCamera import Camera
from piricohmotoWifi import Wifi

class RicohWifi(Wifi):
  def __init__(self):
    super(self.__class__, self).__init__

class RicohImage(Image):
  def __init__(self, dirname, filename):
    super(self.__class__, self, filename).__init__
    self.name = name
    self.filename = filename
    self.dirname = dirname
    
  def download(self, size='full'):
    """ Download an image. 
        For now just return the requests object. keep is simple
    """
    return requests.get('http://{ip}/v1/photos/{dirname}/{filename}?size={size}'.format(ip=self.ip, dirname=dirname, filename=filename, size=size), timeout=10)

class Ricoh(Camera):
  def __init__(self):
    super(self.__class__, self).__init__(**kwargs)
    self.ip = self.config['ip']
    self.objs = requests.get('http://{ip}/_gr/objs'.format(ip=self.ip), timeout=10).json()
    self.download_dir = self.config['download_dir ']

  def connection(self):
    """
      Boolean. Return a Wifi object
    """
    return RicohWifi()

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

  def getimage(self, dirname, filename):
    """ Return an Image object """
    return RicohImage(dirname, filename)