#!/usr/bin/env python

import sys

cwd = sys.path.dirname(path.abspath(__file__))
sys.path.append('{}/lib/'.format(cwd))
sys.path.append('{}/../lib/'.format(cwd))
from piricohmotoWifi import Wifishit
from piricohmoto import Grimage

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

