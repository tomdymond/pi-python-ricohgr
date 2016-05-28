#!/home/venvs/piricohmoto/bin/python

import json
import requests
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--flashing", help="flashing. 0 or 1", default=0)
parser.add_argument("--led", help="LED to light up. 1 to 18")
parser.add_argument("--power", help="Power, 1 to 200", default=100)
parser.add_argument("--duration", help="How long to turn on for in seconds", default=3)
args = parser.parse_args()

a=[int(args.flashing), int(args.led), int(args.power), int(args.duration)]
requests.post('http://127.0.0.1:5000', json=json.dumps(a))
