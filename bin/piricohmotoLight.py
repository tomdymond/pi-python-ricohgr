#!/usr/bin/env python

import argparse
from os import sys, path


cwd = path.dirname(path.abspath(__file__))
sys.path.append('{}/lib/'.format(cwd))
sys.path.append('{}/../lib/'.format(cwd))

from piricohmotoNotifier import Notifier

parser = argparse.ArgumentParser()
parser.add_argument("--flashing", help="flashing. 0 or 1", default=0)
parser.add_argument("--led", help="LED to light up. 1 to 18")
parser.add_argument("--power", help="Power, 1 to 200", default=100)
parser.add_argument("--duration", help="How long to turn on for in seconds", default=3)
args = parser.parse_args()

a = Notifier()
a.led([args.led])
a.flashing = args.flashing
a.duration = args.duration
a.power = args.power
a.send()

