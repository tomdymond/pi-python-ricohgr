#!/usr/bin/env python
# piricohmotoWifi.py

import sh
import re
import sys
import time
from piricohmotoConfig import Config

class Wifi(Config):
  def __init__(self, **kwargs):
    Config.__init__(self, **kwargs)
    self.camera_ssid = self.config['camera_ssid']

  def get_ssids(self):
    """ Return a list of access points """
    ssids = []
    try:
      output = sh.sudo('iwlist','wlan0','scan').stdout
      for line in output.split('\n'):
        if "ESSID" in line:
          ssid = re.findall(r'"(.*?)"', line)[0]
          if ssid:
            ssids.append(ssid)
    except Exception as e:
      print (e.message)
    return ssids

  def get_current_ssid(self):
    """ Just return the current ssid """
    try:
      output = sh.sudo('iwgetid').stdout
      if output:
        s = output.split()[1]
        ssid = re.findall(r'"(.*?)"', s)[0]
      return ssid
    except Exception as e:
      message = e.message
    return False

  def is_camera_on(self):
    """ Return true if the camera is turned on """
    if self.camera_ssid in self.get_ssids():
      print ("Camera is ON!")
      return True
    print ("Camera is OFF!")
    return False

  def manage_wlan0(self, action="up"):
    """ Manage wlan0 """
    if action == 'up':
      if_script = 'ifup'
    else:
      if_script = 'ifdown'

    try:
      sh.sudo(if_script, 'wlan0')
      return True
    except Exception as e:
      print (e.message)
      return False

  def restart_interface(self):
    """ Restart wlan0 interface """
    self.manage_wlan0('down')
    self.manage_wlan0('up')

  def connect_to_camera_ssid(self):
    """ Return true if connected to camera SSID """
    if self.get_current_ssid() != self.camera_ssid:
      print ("Trying to connect to camera ssid {}".format(self.camera_ssid))
      print ("Current SSID: {}".format(self.get_current_ssid()))
      self.restart_interface()
      print ("Waiting for interface")
      time.sleep(2)
      i = 0
      while self.get_current_ssid() != self.camera_ssid:
        time.sleep(1)
        if i > 20:
          print ("Error connecting to the camera")
          sys.exit(1)
        i += 1

    print ("Connected to Camera SSID")
    if self.get_current_ssid() == self.camera_ssid:
      return True
    else:
      print ("Problem connecting to SSID {}".format(self.camera_ssid))
    return False
