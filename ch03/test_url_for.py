# -*- coding: utf-8 -*-

from flask import Flask, url_for

app = Flask(__name__)

@app.route('/hello/')
def hello():
    return 'Hello Flask!'

@app.route('/profile/<username>')
def get_profile(username):
    return 'profile : ' + username

if __name__ == '__main__':
    with app.test_request_context():
        print (url_for('hello'))
        print (url_for('get_profile', username='flask'))
