#!/usr/bin/python
import sys
sys.path.append('./RPi-LPD8806')

from bootstrap import *
from flask import Flask

led.all_off()

dawn = Flask(__name__)

@dawn.route('/')
def index():
    print('Get request made.')
    return 'Hello world'

if __name__ == '__main__':
    dawn.run(host='0.0.0.0', port='8090')
