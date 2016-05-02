#!/usr/bin/env python
# piricohmotoRicoh.py

import requests
import sys
from piricohmotoImage import Image
from piricohmotoCamera import Camera
from piricohmotoConfig import Config
from piricohmotoWifi import Wifi

class RicohWifi(Wifi):
  def __init__(self, **kwargs):
    Wifi.__init__(self, **kwargs)

class RicohImage(Image):
  def __init__(self, **kwargs):
    Image.__init__(self, **kwargs)
    self.filename = kwargs['filename']
    self.dirname = kwargs['dirname']
    self.ip = self.config['ip']
    
  def download(self, size='full'):
    """ Download an image. 
        Return true if successful
    """
    print "Starting download of {}".format(self.filename)
    a =  requests.get('http://{ip}/v1/photos/{dirname}/{filename}?size={size}'.format(ip=self.ip, dirname=self.dirname, filename=self.filename, size=size), timeout=10)
    print a.status_code
    if a.status_code == 200:
      print "saving file..."
      with open('{}/{}'.format(self.download_dir, self.filename), 'wb') as f:
        for chunk in request_response.iter_content(chunk_size=1024): 
          if chunk: # filter out keep-alive new chunks
            f.write(chunk)
      r = redis.StrictRedis(host='localhost')
      gg = {'UPLOAD': False, 'GPS': {}}
      r.hmset('IMAGES', {self.filename: json.dumps(gg)})
      return True
    return False

class Ricoh(Camera):
  def __init__(self, **kwargs):
    Camera.__init__(self, **kwargs)
    self.ip = self.config['ip']
    self.download_dir = self.config['download_dir']
    self.objs = []

  def get_objs(self):
    """ Return objects """
    if not self.objs:
      a = requests.get('http://{ip}/_gr/objs'.format(ip=self.ip), timeout=10).json()
      self.objs = a
    return self.objs

  def connection(self):
    """
      Boolean. Return a Wifi object
    """
    return RicohWifi(config_file=self.config_file)

  def listimages(self, dirname):
    """ Get the images from the camera """
    # This should return a list of image objects rather than just primitives
    f = []
    files = []
    for i in self.get_objs()['dirs']:
      if i['name'] == dirname:
        for image_file in i['files']:
          if image_file['n'].split('.')[1] == 'JPG':
            files.append(image_file)
        f.append(files)
    return f

  def listdirs(self):
    """ Return the list of directories on the SD card """
    d = []
    for i in self.get_objs()['dirs']:
      d.append(i['name'])
    return d

  def getimage(self, dirname, filename):
    """ Return an Image object """
    return RicohImage(config_file=self.config_file, dirname=dirname, filename=filename)