import time
import math
import random
from bootstrap import *

TARGET_COLORS = [
    [0,0,0],
    [97,49,50],
    [110,55,48],
    [141,67,56],
    [197,96,74],
    [253,129,91],
    [253,154,105],
    [253,196,135],
    [254,239,179],
    [252,255,239]
]
MIN_TICK_LENGTH = 0.1
MAX_TICKS = 1000
LED_COUNT = 32

class Sunrise:
    def __init__(self, sunriseDuration):
        self.sunriseDuration = sunriseDuration
        self.timeElapsed = 0
        self.speedMults = self.genSpeedMults()
        print('self.speedMults')
        print(self.speedMults)

    def genSpeedMults(self):
        speedMults = []
        for index in range(LED_COUNT):
            speedMults.append(random.uniform(0.25, 1.0))
        return speedMults

    def test(self):
        self.start()
        time.sleep(2)
        self.end()

    def start(self):
        led = LEDStrip(LED_COUNT)
        for colorIndex in range(len(TARGET_COLORS)-1):
            self.transitionBetweenColors(TARGET_COLORS[colorIndex],
                TARGET_COLORS[colorIndex+1],
                self.sunriseDuration/len(TARGET_COLORS))

    def end(self):
        led = LEDStrip(LED_COUNT)
        for colorIndex in reversed(range(1, len(TARGET_COLORS))):
            self.transitionBetweenColors(TARGET_COLORS[colorIndex],
                TARGET_COLORS[colorIndex-1], 0.1)
        led.all_off()

    def transitionBetweenColors(self, color1, color2, duration):
        ticksPassed = 0
        tickLength = MIN_TICK_LENGTH
        ticksTotal = math.floor(duration / MIN_TICK_LENGTH)
        if (ticksTotal > MAX_TICKS):
            ticksTotal = MAX_TICKS
            tickLength = duration / ticksTotal
        for tickIndex in range(ticksTotal):
            ticksPassed += 1
            self.timeElapsed += tickLength
            progress = ticksPassed / ticksTotal
            for ledIndex in range(LED_COUNT):
                self.applyColorToOneLed(color1, color2, progress, ledIndex)
            led.update()
            time.sleep(tickLength)

    def applyColorToOneLed(self, color1, color2, progress, ledIndex):
        appliedProgress = progress * self.speedMults[ledIndex]
        colorSet = self.genColorSet(color1, color2, appliedProgress)
        led.setRGB(ledIndex, colorSet[0], colorSet[1], colorSet[2])

    def genColorSet(self, color1, color2, progress):
        colorSet = []
        for ci in range(3):
            color = (color1[ci] + (color2[ci] - color1[ci]) * progress)
            colorSet.append(color)
        return colorSet
