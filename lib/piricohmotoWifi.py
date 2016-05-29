#!/usr/bin/env python
# piricohmotoWifi.py

import sh
import re
import sys
import time
from time import sleep
import os
from piricohmotoConfig import Config
import redis

class Wifi(Config):
  def __init__(self, **kwargs):
    Config.__init__(self, **kwargs)
    self.cached_ssid = self.get_cached_ssid()
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


  def get_cached_ssid(self):
    r = redis.StrictRedis(host='localhost')
    return r.get('SSID')

  def write_cached_ssid(self, ssid):
    r = redis.StrictRedis(host='localhost')
    return r.set('SSID', ssid)

  def restart_connection(self):
    """ Restart the wifi """
    print "restart_connection"


    print "Entering a while loop until I'm connected to an SSID"
    i = 0
    while not self.get_current_ssid():
      print "waiting... {}/{}".format(i, 20)
      time.sleep(1)
      if i > 20:
        print "Timed out waiting for confirmation I was conncted to any AP"
        return False


    current_ssid = self.get_current_ssid()

    if current_ssid:
      print "Connected with {}. Previous was {}".format(current_ssid, self.cached_ssid)
      if current_ssid != self.cached_ssid:
        print "Detected an SSID change. restarting DHCP"
        self.write_cached_ssid(current_ssid)
        try:
          sh.sudo('killall', 'dhclient')
        except Exception as e:
          print e.message
        try:
          sh.sudo('dhclient', self.camera_interface)
        except Exception as e:
          print e.message
          return False   
    return True
    


  def get_current_ssid(self):
    """ Just return the current ssid """
    print "In function get_current_ssid"
    try:
      output = sh.sudo('/sbin/iwgetid').stdout
      if output:
        s = output.split()[1]
        print s
        ssid = re.findall(r'"(.*?)"', s)[0]
        print 'ssid={}'.format(ssid) 
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


  def restart_wpasupplicant(self):
    print "Restarting wpa_supplicant"
    try:
      sh.sudo('killall','wpa_supplicant')
    except Exception as e:
      print e.message
    sleep(1)
    sh.sudo('wpa_supplicant', '-s', '-B', '-P', '/run/wpa_supplicant.{}.pid'.format(self.camera_interface), '-i', self.camera_interface, '-D', 'nl80211,wext', '-c', '/etc/wpa_supplicant/wpa_supplicant.conf')
    sleep(10)

  def connect_to_camera_ssid(self):
    """ Return true if connected to camera SSID """

    if self.get_current_ssid() != self.camera_ssid:
      self.restart_wpasupplicant()
      sleep(1)

    if self.get_current_ssid() == self.camera_ssid:
      print ("Connected to Camera SSID")
      self.restart_connection()
      return True
    else:
      print ("Problem connecting to SSID {}".format(self.camera_ssid))
    return False
