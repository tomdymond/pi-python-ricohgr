#!/usr/bin/env python
"""
Pretend to be the camera so I can test my code. Sort of like integration
"""

from flask import Flask, send_file

app = Flask(__name__)
import json

@app.route('/v1/photos/<dirname>/<filename>')
def get_file():
  with open('SAMPLE_PHOTOS/{}'.format(filename)) as f:
    image = f.read()
  return send_file(io.BytesIO(image),
                   attachment_filename=filename,
                   mimetype='image/jpeg')

@app.route('/_gr/objs')
def objs():
  a = {u'dirs': [{u'files': [{u'd': u'2016-03-28T09:24:02',
     u'n': u'R0040162.JPG',
     u'o': 0,
     u's': u''},
    {u'd': u'2016-03-28T11:14:00', u'n': u'R0040163.JPG', u'o': 0, u's': u''},
    {u'd': u'2016-03-28T11:14:00', u'n': u'R0040163.DNG', u'o': 0, u's': u''}],
   u'name': u'102RICOH'},
  {u'files': [{u'd': u'2016-04-02T14:37:24',
     u'n': u'P4020001.JPG',
     u'o': 0,
     u's': u''}],
   u'name': u'103OLYMP'},
  {u'files': [{u'd': u'2016-04-03T09:30:16',
     u'n': u'R0050001.JPG',
     u'o': 0,
     u's': u''},
    {u'd': u'2016-04-03T09:30:32', u'n': u'R0050002.JPG', u'o': 0, u's': u''},
    {u'd': u'2016-04-03T09:30:32', u'n': u'R0050002.DNG', u'o': 0, u's': u''}],
   u'name': u'875RICOH'}],
 u'errCode': 200,
 u'errMsg': u'OK'}
  return a

