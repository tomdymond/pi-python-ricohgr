#!/usr/bin/env python

import requests
import os
import sys
import datetime
from piricohmotoConfig import Config
from piricohmotoImage import Image
from piricohmotoCamera import Camera
import redis
import json

class RicohImage(Image):
  def __init__(self, dirname, filename):
    super(self.__class__, self, filename).__init__
    self.name = name
    self.filename = filename
    self.dirname = dirname
    
  def download(self, size='full'):
    """ Download an image """
    try:
      #timestamp_1 = int(datetime.datetime.now().strftime('%s'))
      request = requests.get('http://{ip}/v1/photos/{dirname}/{filename}?size={size}'.format(ip=self.ip, dirname=dirname, filename=filename, size=size), timeout=10)
      #timestamp_2 = int(datetime.datetime.now().strftime('%s'))
      #size_on_disk = self.size()
      #total_time = timestamp_2 - timestamp_1
      #download_speed = ( size_on_disk / total_time )
      #print "Download took {} seconds. Speed={} Bytes/s".format(total_time, download_speed)
      return request
    except Exception as e:
      print e.message
    return False

  def save(self, request_response):
    """ Save the requests reponse to disk """
    with open('{}/{}'.format(self.download_dir, self.filename), 'wb') as f:
      for chunk in request_response.iter_content(chunk_size=1024): 
        if chunk: # filter out keep-alive new chunks
          f.write(chunk)
    r = redis.StrictRedis(host='localhost')
    r.hmset('IMAGES', {self.filename: json.dumps({'UPLOAD': False, 'GPS': {}}}))

  def already_downloaded(self):
    """ Bool. If the image is already downloaded """
    r = redis.StrictRedis(host='localhost')
    return r.hexists('IMAGES', self.filename)

  def size(self):
    """ Return image size """
    return int(os.path.getsize('{}/{}'.format(self.download_dir, filename)))

class Ricoh(Camera):
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

  def getimage(self, dirname, filename):
    """ Return an Image object """
    return RicohImage(dirname, filename)