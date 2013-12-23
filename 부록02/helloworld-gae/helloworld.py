# -*- coding: utf-8 -*-

from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return '<h1>Hello Flask on Google App Engine</h1>'

if __name__ == '__main__':
    app.run()

