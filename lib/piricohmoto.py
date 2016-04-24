#!/usr/bin/env python

import requests
import os
import sys

STATE_FILE='/tmp/state'
DOWNLOAD_DIR='/tmp'

class Grimage(object):
  def __init__(self, ip='192.168.0.1'):
    self.ip = ip
    self.objs = requests.get('http://{ip}/_gr/objs'.format(ip=ip), timeout=10).json()
    self.state = self.read_state()

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
    if filename in self.state:
      print "Skipping {}. Already downloaded".format(filename)
      return True
    try:
      r = requests.get('http://{ip}/v1/photos/{dirname}/{filename}?size={size}'.format(ip=self.ip, dirname=dirname, filename=filename, size=size), timeout=10)
      with open('{}/{}'.format(DOWNLOAD_DIR, filename), 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
          if chunk: # filter out keep-alive new chunks
            f.write(chunk)
      self.update_state(filename)
      return True
    except Exception as e:
      print e.message
      sys.exit(1)
    return False

  def download_all(self):
    """ Download all images """
    for d in self.listdirs():
      for i in self.listimages(d):
        for j in i:
          self.getimage(d, j['n'])
          print j['n']

  def read_state(self):
    """ Just use a text file for now. Return a list of images """
    if os.path.exists(STATE_FILE):
      with open(STATE_FILE, 'r') as f:
        return f.read().split('\n')
    else:
      return []

  def update_state(self, image):
    """ Register what's been download """
    try:
      with open(STATE_FILE, 'ab') as f:
        f.write("{}\n".format(image))
      return True
    except Exception as e:
      print e.message
    return False


 