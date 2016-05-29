#!/usr/bin/env python
# piricohmotoCamera.py

import os
from piricohmotoConfig import Config
from piricohmotoImage import Image
import dropbox
import redis

class Camera(Config):
  def __init__(self, **kwargs):
    #super(self.__class__, self).__init__(**kwargs)
    Config.__init__(self, **kwargs)
    self.redis_connection = redis.StrictRedis(host='localhost')
    self.access_token = self.config['access_token']
    


  def geotag_all(self):
    """ Upload all images if jpeg """
    for image in self.redis_connection.hgetall('IMAGES').keys():
      if 'GEO' not in self.redis_connection.hget('IMAGES', image):
        image = Image(config_file=self.config_file, filename=image)
        if image.is_downloaded() and not image.is_geotagged():
          image.geotag_image()

  def download_all(self):
    """ Download all images """
    images_downloaded = self.redis_connection.hkeys('IMAGES')
    images = []
    for foldername in self.listdirs():
      for i in self.listimages(foldername):
        for j in i:
          filename = j['n']
          images.append(self.getimage(foldername, filename))
    for image in images:
      if not image.is_downloaded() and not image.is_uploaded():
        image.download()

  def get_dropbox_images(self):
    """ Return of list of images already uploaded """
    remote_list = set()
    try:
      client = dropbox.client.DropboxClient(self.access_token)
      for i in client.metadata('/')['contents']:
        remote_list.add(i['path'].split('/')[1])
    except Exception as e:
      print e.message
    return list(remote_list)
     
  def upload_all(self):
    """ Upload all images if jpeg """
    self.dropbox_images = self.get_dropbox_images()
    for filename in self.redis_connection.hkeys('IMAGES'):
      image = Image(config_file=self.config_file, filename=filename)
      if not image.is_uploaded() and image.is_geotagged():
        if filename in self.dropbox_images:
          j = json.loads(self.redis_connection.hget('IMAGES', filename))
          j['UPLOAD'] = True
          r.hmset('IMAGES', {self.filename: json.dumps(j)})
        else:
          image.upload_to_dropbox()
      print ("Skipping {}. Already uploaded".format(filename))
