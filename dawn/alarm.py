from datetime import datetime, timedelta
import time
import math
from sunrise import Sunrise

class Alarm:
    def __init__(self):
        self.timeStr = '06:00'
        self.alarmDatetime = datetime.now()
        self.alarmDelta = ''
        self.sunriseDuration = (10 * 60000)
        self.sunRising = False
        try:
            results = self.readAlarmFromFile()
            timeStr = results[0]
            sunriseDuration = results[1]
            self.setAlarmData(timeStr, sunriseDuration)
        except Exception as e:
            self.setAlarmData(self.timeStr, self.sunriseDuration)
            self.writeAlarmToFile(self.timeStr, self.sunriseDuration)


    def readAlarmFromFile(self):
        fileObj = open("alarmdata.csv", "r")
        fileStrs = fileObj.read().split(',')
        timeStr = fileStrs[0]
        sunriseDuration = int(fileStrs[1])
        fileObj.close()
        return (timeStr, sunriseDuration)

    def writeAlarmToFile(self, alarmStr, sunriseDuration):
        fileObj = open("alarmdata.csv", "w")
        fileObj.write(alarmStr + ',' + str(sunriseDuration))
        fileObj.close()

    def setAlarmData(self, timeStr, sunriseDuration):
        results = self.formAlarmData(timeStr, sunriseDuration)
        self.timeStr = timeStr
        self.alarmDatetime = results[0]
        self.alarmDelta = results[1]
        self.sunriseDuration = sunriseDuration

    def formAlarmData(self, timeStr, sunriseDuration):
        alarmDatetime = datetime.now()
        nowDatetime = datetime.now()
        alarmToday = datetime(nowDatetime.year, nowDatetime.month,
            nowDatetime.day, int(timeStr[0:2]), int(timeStr[3:5]))
        if (alarmToday > nowDatetime):
            alarmDatetime = alarmToday
        else:
            alarmDatetime = alarmToday + timedelta(days=1)
        alarmDelta = alarmDatetime - nowDatetime
        deltaString = ''
        if (alarmDelta.days > 0):
            deltaString = alarmDelta.days + ' day'
            if (alarmDelta.days > 1):
                deltaString += 's'
            deltaString += ', '
        minutes = math.ceil(alarmDelta.seconds/60)
        hours = 0
        if (minutes > 60):
            hours = math.floor(alarmDelta.seconds/3600)
        minutes -= hours*60
        if (hours > 0):
            deltaString += str(hours) + ' hour'
            if (hours > 1):
                deltaString += 's'
            deltaString += ', '
        if (minutes > 0):
            deltaString += str(minutes) + ' minute'
            if (minutes > 1):
                deltaString += 's'
        return (alarmDatetime, deltaString)

    def checkAlarmSleeper(self):
        if not (self.sunRising):
            nowDatetime = datetime.now()
            if (nowDatetime > self.alarmDatetime):
                self.callAlarm()


    def callAlarm(self):
        aSunrise = Sunrise(self.sunriseDuration)
        aSunrise.start()
        aSunrise.end()
