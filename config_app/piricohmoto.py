#!/usr/bin/env python

from flask import Flask, render_template, make_response
from flask_bootstrap import Bootstrap

def create_app():
  app = Flask(__name__)
  Bootstrap(app)
  return app

@app.route("/")
def hello():
  return render_template('test.html',testvar='foo')

if __name__ == "__main__":
  app = create_app()
  app.run(host='0.0.0.0', port=8080)

