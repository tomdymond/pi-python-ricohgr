#!/usr/bin/env python

import requests

class Grimage(object):
  def __init__(self, ip='192.168.0.1'):
    self.ip = ip
    self.objs = requests.get('http://{ip}/_gr/objs'.format(ip=ip), timeout=10).json()

  def listimages(self, dirname):
    """ Get the images from the camera """
    f = []
    for i in self.objs['dirs']:
      if i['name'] == dirname:
        f.append(i['files'])
    return f

  def listdirs(self):
    for i in self.objs['dirs']:
      print i['name']

  def getimage(self, dirname, filename):
    """ Download an image """
    return requests.get('http://{ip}/v1/photos/{dirname}/{filename}?size=full'.format(ip=self.ip, dirname=dirname, filename=filename))
