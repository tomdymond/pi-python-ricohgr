#!/usr/bin/env python
# piricohmotoCamera.py

import os
from piricohmotoConfig import Config
from piricohmotoImage import Image
import dropbox
import json

class Camera(Config):
  def __init__(self, **kwargs):
    #super(self.__class__, self).__init__(**kwargs)
    Config.__init__(self, **kwargs)
    self.access_token = self.config['access_token']
    
  def thumbnail_all(self):
    """ Upload all images if jpeg """
    for image in self.data.get_hkeys('IMAGES'):
      image = Image(config_file=self.config_file, filename=image)
      if image.is_downloaded():
        image.create_smallsize(1000)
        image.create_smallsize(500)
        image.create_smallsize(100)

  def geotag_all(self):
    """ Upload all images if jpeg """
    for image in self.data.get_hkeys('IMAGES'):
      image = Image(config_file=self.config_file, filename=image)
      if image.is_downloaded() and not image.is_geotagged():
        image.get_geo_map_from_google()
        image.get_geo_payload_from_google()
        image.geotag_image()

  def download_all(self):
    """ Download all images """
    print "download_all"
    images_downloaded = self.data.get_hkeys('IMAGES')
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
    for filename in self.data.get_hkeys('IMAGES'):
      image = Image(config_file=self.config_file, filename=filename)
      if not image.is_uploaded() and image.is_geotagged():
        if filename in self.dropbox_images:
          j = self.data.unpack('IMAGES', filename)
          j['UPLOAD'] = True
          self.data.repack('IMAGES', filename, j)
        else:
          image.upload_to_dropbox()
      print ("Skipping {}. Already uploaded".format(filename))
