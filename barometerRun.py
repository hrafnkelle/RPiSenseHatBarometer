import sense_hat
from Barometer import Barometer
from PressureHistory import PressureHistory

def main():
	pressureHistory = PressureHistory()
	barometer = Barometer(sense_hat.SenseHat(), pressureHistory)

	initialPressureDelta = 0.01
	pressureHistory.max = barometer.sense.pressure+initialPressureDelta
	pressureHistory.min = pressureHistory.max-2*initialPressureDelta

	barometer.run()

if __name__ == "__main__":
	main()
