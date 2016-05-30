#!/usr/bin/env python

from flask import Flask, render_template, make_response
from flask_bootstrap import Bootstrap
import os
import redis

def create_app():
  app = Flask(__name__)
  Bootstrap(app)
  return app

def remove_ext(item):
  base = item.split('.')
  ext = base[1]
  s = base[0].split('_')
  return s[0]

app = create_app()

@app.route("/")
def hello():
  r = redis.StrictRedis(host='localhost')
  images = r.hkeys('IMAGES')
  foo = map(remove_ext, images)

  return render_template('test.html', images=foo)

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=8080)

