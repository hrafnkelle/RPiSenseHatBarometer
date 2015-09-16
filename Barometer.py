from PressureHistory import *
import time

class Barometer:
    TICKS_PER_SECOND = float(10)
    CORNERPIXEL = (0,0)
    DEFAULT_UPDATE_INTERVAL = TICKS_PER_SECOND*60*4

    def __init__(self, senseHat, pressureHistory, **kwargs):
       self.sense = senseHat
       self.pressureHistory = pressureHistory
       self.ledAdapter = LEDMatrixAdapter(pressureHistory)
       self.sense.clear()
       self.ticks = 0
       self.updateInterval = kwargs['updaterate']*Barometer.TICKS_PER_SECOND if ('updaterate' in kwargs) and (kwargs['updaterate']!=None) else Barometer.DEFAULT_UPDATE_INTERVAL

    def updateDisplay(self):
        self.sense.set_pixels(self.ledAdapter.asHatRGBList())

    def updateCornerPixel(self):
        normalizedCurrentPressure = self.pressureHistory.normalizeOneValue(self.sense.pressure)
        updateHue = LEDMatrixAdapter.normalValueAsHue(normalizedCurrentPressure)
        updateValue = (self.ticks%Barometer.TICKS_PER_SECOND)/float(Barometer.TICKS_PER_SECOND)
        updateRGBColor = tuple(int(x*255) for x in colorsys.hsv_to_rgb(updateHue, 1, updateValue))
        self.sense.set_pixel(Barometer.CORNERPIXEL[0], Barometer.CORNERPIXEL[1], updateRGBColor)

    def shouldUpdateDisplay(self):
        return (self.ticks%self.updateInterval)==0

    def run(self):
        while True:
            time.sleep(1/Barometer.TICKS_PER_SECOND)
            self.ticks = self.ticks + 1
            self.pressureHistory.includeInAverage(self.sense.pressure)
            self.updateCornerPixel()
            if self.shouldUpdateDisplay():
                self.pressureHistory.addFromAccumulator()
                print("%f < %f < %f"%(self.pressureHistory.min, self.pressureHistory.latestAdded(), self.pressureHistory.max))
                self.sense.set_pixels(self.ledAdapter.asHatRGBList())
                self.ticks = 0
