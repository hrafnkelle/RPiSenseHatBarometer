import sense_hat
import time
from util import *

def main():
	sense = sense_hat.SenseHat()
	sense.clear()

	pressureHistory = PressureHistory()
	pressureAcc = []

	secCnt = 0
	updateInterval = 10*60*8

	currPixel = (0,0)

	while True:
		time.sleep(0.1)
		pressureAcc.append(sense.pressure)
		secCnt = secCnt + 1
		col = tuple(int(x*255) for x in colorsys.hsv_to_rgb(pressureToHue(sense.pressure), 1,(secCnt%10)/float(10)))
		sense.set_pixel(currPixel[0], currPixel[1], col)
		if secCnt%updateInterval == 0:
			pressureAvg = listAverage(pressureAcc)
			pressureAcc = []
			print(pressureAvg)
			pressureHistory.add(pressureAvg)
			sense.set_pixels(pressureHistory.asHatRGBList())
			print(pressureHistory.asHatRGBList()[1])

if __name__ == "__main__":
	main()
