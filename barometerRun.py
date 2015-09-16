import sense_hat
from Barometer import Barometer
from PressureHistory import PressureHistory
import argparse

def parseCmdline():
	parser = argparse.ArgumentParser(description='Visualize ambient pressure variations by color coding the pressure on the RPi Sense Hat')
	parser.add_argument('--initiallow',dest='initiallow',help='Pressure mapped to red color until a lower pressure is observed',type=float)
	parser.add_argument('--initialhigh',dest='initialhigh',help='Pressure mapped to blue color until a higher pressure is observed',type=float)
	parser.add_argument('--updaterate',dest='updaterate',help='Update rate in seconds',type=int)

	return parser.parse_args()

def main():
	args = parseCmdline()

	pressureHistory = PressureHistory(initialpressurelow=args.initiallow, initialpressurehigh=args.initialhigh)
	barometer = Barometer(sense_hat.SenseHat(), pressureHistory, updaterate=args.updaterate)

	barometer.run()

if __name__ == "__main__":
	main()
