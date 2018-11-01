from datetime import datetime, timedelta
import time

class Alarm:
    def __init__(self):
        timeStr = '06:00'
        self.alarmDatetime = None
        try:
            timeStr = self.readAlarmFromFile()
        except Exception as e:
            self.writeAlarmToFile(timeStr)
        self.setAlarmDatetime(timeStr)

    def readAlarmFromFile(self):
        fileObj = open("alarmtime.txt", "r")
        timeStr = fileObj.read()
        fileObj.close()
        return timeStr

    def writeAlarmToFile(self, alarmStr):
        fileObj = open("alarmtime.txt", "w")
        fileObj.write(alarmStr)
        fileObj.close()

    def setAlarmDatetime(self, timeStr):
        alarmDatetime = datetime.now()
        nowDatetime = datetime.now()
        alarmToday = datetime(nowDatetime.year, nowDatetime.month,
            nowDatetime.day, int(timeStr[0:2]), int(timeStr[3:5]))
        if (alarmToday > nowDatetime):
            alarmDatetime = alarmToday
        else:
            alarmDatetime = alarmToday + timedelta(days=1)
        sleeperDelta = nowDatetime - alarmDatetime
        self.alarmDatetime = alarmDatetime

    def checkAlarmSleeper(self):
        nowDatetime = datetime.now()
        if (nowDatetime > self.alarmDatetime):
            self.callAlarm()

    def callAlarm(self):
        print('ALARM ALARM ALARM')
