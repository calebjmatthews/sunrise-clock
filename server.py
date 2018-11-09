#!/usr/bin/python
import math
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
    results = anAlarm.readAlarmFromFile()
    anAlarm.setAlarmData(results[0], results[1])
    displayDuration = math.floor(results[1] / 60)
    return render_template('index.html', alarmtime=anAlarm.timeStr,
        alarmDelta=anAlarm.alarmDelta, sunriseDuration=displayDuration)

@server.route('/alarmset', methods=['POST'])
def alarmset():
    timeStr = request.form['alarmtime']
    sunriseDuration = math.floor(int(request.form['sunriseDuration']) * 60)
    anAlarm.writeAlarmToFile(timeStr, sunriseDuration)
    anAlarm.setAlarmData(timeStr, sunriseDuration)
    return redirect(url_for('index'))

if __name__ == '__main__':
    server.run()
    # server.run(host='0.0.0.0', port='8090')

    url_for('static', filename='style.css')
