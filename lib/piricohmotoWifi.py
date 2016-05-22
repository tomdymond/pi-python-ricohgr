#!/usr/bin/env python
# piricohmotoWifi.py

import sh
import re
import sys
import time
import os
from piricohmotoConfig import Config

class Wifi(Config):
  def __init__(self, **kwargs):
    Config.__init__(self, **kwargs)
    self.camera_ssid = self.config['camera_ssid']
    self.camera_interface = self.config['camera_interface']
    os.environ['PATH'] += ":/sbin:/usr/sbin"

  def get_ssids(self):
    """ Return a list of access points """
    ssids = []
    try:
      output = sh.sudo('/sbin/iwlist', self.camera_interface, 'scan').stdout
      for line in output.split('\n'):
        if "ESSID" in line:
          ssid = re.findall(r'"(.*?)"', line)[0]
          if ssid:
            ssids.append(ssid)
    except Exception as e:
      print (e.message)
    print ssids
    return ssids

  def restart_connection(self):
    """ Restart the wifi """
    print "restart_connection"
    sh.sudo('killall','wpa_supplicant')     
    sh.sudo('wpa_supplicant', '-s', '-B', '-P', '/run/wpa_supplicant.{}.pid'.format(self.camera_interface), '-i', self.camera_interface, '-D', 'nl80211,wext', '-c', '/etc/wpa_supplicant/wpa_supplicant.conf')
    i = 0
    while not self.get_current_ssid():
      time.sleep(2)
      if i > 20:
        return False
    sh.sudo('dhclient',self.camera_interface)
    return True

  def get_current_ssid(self):
    """ Just return the current ssid """
    try:
      output = sh.sudo('/sbin/iwgetid').stdout
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

  def connect_to_camera_ssid(self):
    """ Return true if connected to camera SSID """
    if self.get_current_ssid() != self.camera_ssid:
      print ("Trying to connect to camera ssid {}".format(self.camera_ssid))
      print ("Current SSID: {}".format(self.get_current_ssid()))
      self.restart_connection()
      print ("Waiting for interface")
 

    print ("Connected to Camera SSID")
    if self.get_current_ssid() == self.camera_ssid:
      sh.sudo('ifconfig', self.camera_interface, '192.168.0.2/24', 'up')
      #sh.sudo('dhclient',self.camera_interface)
      return True
    else:
      print ("Problem connecting to SSID {}".format(self.camera_ssid))
    return False
