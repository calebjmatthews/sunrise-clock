#!/usr/bin/python
sys.path.append('/RPi-LPD8806')

from bootstrap import *
from flask import Flask

print('led:')
print(led)

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello world'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
