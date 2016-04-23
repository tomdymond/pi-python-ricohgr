#!/usr/bin/env python

import requests

class Grimage(object):
  def __init__(self, ip='192.168.0.1'):
    self.ip = ip
    self.objs = requests.get('http://{ip}/_gr/objs'.format(ip=ip), timeout=10).json()

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

  def getimage(self, dirname, filename, size=full):
    """ Download an image """
    r = requests.get('http://{ip}/v1/photos/{dirname}/{filename}?size={size}'.format(ip=self.ip, dirname=dirname, filename=filename, size=size))
    with open('/tmp/{}'.format(filename), 'wb') as f:
      for chunk in r.iter_content(chunk_size=1024): 
        if chunk: # filter out keep-alive new chunks
          f.write(chunk)
 