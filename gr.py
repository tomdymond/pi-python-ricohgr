#!/usr/bin/env python

import requests
from pprint import pprint
import sh
import re
import time
import sys
import os

RICOH_SSID=os.environ["RICOH_SSID"]

class Wifishit(object):
    def __init__(self):
        fo=1

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
            print e.message
        #print ssids
        #print self.get_current_ssid()
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
        if RICOH_SSID in self.get_ssids():
            print "Camera is ON!"
            return True
        print "Camera is OFF!"
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
            print e.message
            return False

    def restart_interface(self):
        """ Restart wlan0 interface """
        self.manage_wlan0('down')
        self.manage_wlan0('up')

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



a = Wifishit()

if a.is_camera_on():
    if a.get_current_ssid() != RICOH_SSID:
        print a.get_current_ssid()
        print RICOH_SSID
        a.restart_interface()
        print "Waiting for interface"
        time.sleep(2)
        i = 0
        while a.get_current_ssid() != RICOH_SSID:
            print a.get_current_ssid()
            time.sleep(1)
            if i > 20:
                print "Error connecting to the camera"
                sys.exit(1)
            i += 1

    print "current SSID is good!"
    if a.get_current_ssid() == RICOH_SSID:
        b = Grimage()
        for i in b.listimages('102RICOH'):
            for j in i:
                print j['n']
    else:
        print "Problem connecting to SSID {}".format(RICOH_SSID)

