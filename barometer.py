import sense_hat
import time
from util import *

def main():
	sense = sense_hat.SenseHat()
	sense.clear()

	pressureHistory = PressureHistory()
	initialDelta = 0.01
	pressureHistory.max = sense.pressure+initialDelta
	pressureHistory.min = pressureHistory.max-2*initialDelta

	pressureAcc = []

	secCnt = 0
	updateInterval = 10*60*4

	currPixel = (0,0)

	while True:
		time.sleep(0.1)
		pressureAcc.append(sense.pressure)
		secCnt = secCnt + 1
		col = tuple(int(x*255) for x in colorsys.hsv_to_rgb(0.75*pressureHistory.normalizeOneValue(sense.pressure), 1,(secCnt%10)/float(10)))
		sense.set_pixel(currPixel[0], currPixel[1], col)
		if secCnt%updateInterval == 0:
			pressureAvg = listAverage(pressureAcc)
			pressureAcc = []
			print("%f < %f < %f"%(pressureHistory.min, pressureAvg, pressureHistory.max))
			pressureHistory.add(pressureAvg)
			print("%f < %f < %f"%(pressureHistory.min, pressureAvg, pressureHistory.max))
			sense.set_pixels(pressureHistory.asHatRGBList())

if __name__ == "__main__":
	main()
