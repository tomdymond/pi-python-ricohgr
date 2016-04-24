#!/usr/bin/env python

import requests
import os
import sys
import datetime

class Geo(object):
  def __init__(self, device):
    self.device = device

  def get_current_location(self):
    """ Return timestamp and current location """
    timestamp = datetime.datetime.now().strftime('%s')
    return [timestamp]