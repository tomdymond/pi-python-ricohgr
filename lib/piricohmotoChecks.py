#!/usr/bin/env python

import os
import requests
import sh
import psutil

class Check(object):
    def check_disk_space(self, paths=['/','/download']):
        """ """
        for path in paths:
            a = psutil.disk_usage(path)
            if a.percent > 90:
                return (False, 1206)
        return (True, 0206)

    def check_cpu_temp(self):
        os.environ['PATH'] += ':/opt/vc/bin'
        result = sh.sudo('vcgencmd','measure_temp')
        temp = float(result.stdout.rstrip().split('=')[1].split("'")[0])
        if temp > 70:
            return (False, 4004)
        return (True, 3004)

    def check_internet(self):
        try:
            response = requests.head('http://www.google.com')
            if int(response.status_code) in (200, 302):
                return (True, 0001)
            else:
                return (False, 1001)
        except Exception as e:
            return (False, 1001)


