#!/usr/bin/env python

import os
from piricohmotoConfig import Config
import redis

class Camera(Config):
  def __init__(self):
    super(self.__class__, self).__init__(**kwargs)
    self.redis_connection = redis.StrictRedis(host='localhost')

  def geotag_all(self):
    """ Upload all images if jpeg """
    for image in self.redis_connection.hgetall('IMAGES').keys():
      if 'GEO' not in self.redis_connection.hget('IMAGES', image)
        image = Image(f)
        image.geotag_image()

  def download_all(self):
    """ Download all images """
    images_downloaded = self.redis_connection.hkeys('IMAGES')
    images = []
    for foldername in self.listdirs():
      for i in self.listimages(foldername):
        for j in i:
          filename = j['n']
          print filename
          if filename not in images_downloaded:
            images.append(self.getimage(foldername, filename))
    for image in images:
      image.download()
      image.save()

  def upload_all(self):
    """ Upload all images if jpeg """
    for k in self.redis_connection.hkeys('IMAGES'):
      image = Image(f)
      if not image.is_uploaded():
        image.upload_image_to_dropbox()
      print "Skipping {}. Already uploaded".format(f)