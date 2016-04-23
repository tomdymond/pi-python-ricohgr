!/usr/bin/env python
""" Test suite for pi ricoh motorbike project """

import unittest
from mock import Mock
from os import sys, path
import yaml
import json

cwd = path.dirname(path.dirname(path.abspath(__file__)))
sys.path.append('{}/lib/'.format(cwd))

from piricohmotoWifi import Wifishit
from piricohmoto import Grimage

CONFIG_FILE = '{}/test/test-data/piricohmoto.yml'.format(cwd)

class Test(unittest.TestCase):
  """ Test stuff """


