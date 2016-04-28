#!/usr/bin/env python

import os
from piricohmotoConfig import Config
from piricohmotoCamera import Ricoh

class Dosomething(Config):
  def __init__(self):
    super(self.__class__, self).__init__(**kwargs)
    self.state_file_upload = self.config['state_file_upload']
    self.state_upload = self.read_state(self.state_file_upload)
    self.state_file_download = self.config['state_file_download']
    self.state_download = self.read_state(self.state_file_download)
    self.camera = Ricoh()

  def geotag_all(self):
    """ Upload all images if jpeg """
    for f in self.state_download:
      image = Image(f)
      image.geotag_image()

  def download_all(self):
    """ Download all images """
    for foldername in self.camera.listdirs():
      for i in self.camera.listimages(foldername):
        for j in i:
          filename = j['n']
          print filename
          self.camera.getimage(foldername, filename)

  def upload_all(self):
    """ Upload all images if jpeg """
    for f in self.state_download:
      if f not in self.state_upload:
        image = Image(f)
        image.upload_image_to_dropbox()
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
