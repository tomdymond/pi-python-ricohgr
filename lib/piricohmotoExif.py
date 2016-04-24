#!/usr/bin/env python

import pyexiv2

# http://exiv2.org/tags.html

class Grimageexif(pyexiv2):
  def __init__(self, image_file):
    self.image_file = image_file
    self.metadata = self.ImageMetadata(self.image_file)
    self.metadata.read()

  def return_tags(self):
    """ Just for testing, return the tags """
    return self.metadata.keys()

  def update_add_key(self, k, v):
    """ Update metadata """
    self.metadata[k] = v
    self.metadata.write()