#!/usr/bin/env python

import requests

response = requests.get('http://www.google.com')

print response.status_code