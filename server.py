#!/usr/bin/python
import sys
sys.path.append('./RPi-LPD8806')
sys.path.append('./dawn')

# from bootstrap import *
from flask import Flask, render_template, request, redirect, url_for
from alarm import Alarm
anAlarm = Alarm()
import atexit
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()
scheduler.add_job(func=anAlarm.checkAlarmSleeper, trigger="interval",
    seconds=10)
scheduler.start()
atexit.register(lambda: scheduler.shutdown())

# led.all_off()

server = Flask(__name__)

@server.route('/')
def index():
    timeStr = anAlarm.readAlarmFromFile()
    return render_template('index.html', alarmtime=timeStr)

@server.route('/alarmset', methods=['POST'])
def alarmset():
    timeStr = request.form['alarmtime']
    anAlarm.writeAlarmToFile(timeStr)
    anAlarm.setAlarmDatetime(timeStr)
    return redirect(url_for('index'))

if __name__ == '__main__':
    server.run()
    # server.run(host='0.0.0.0', port='8090')

    url_for('static', filename='style.css')
