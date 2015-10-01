import sense_hat
from Barometer import Barometer
from PressureHistory import PressureHistory, CSVLogger
import argparse

def parseCmdline():
	parser = argparse.ArgumentParser(description='Visualize ambient pressure variations by color coding the pressure on the RPi Sense Hat')
	parser.add_argument('--initiallow',dest='initiallow',help='Pressure mapped to red color until a lower pressure is observed',type=float)
	parser.add_argument('--initialhigh',dest='initialhigh',help='Pressure mapped to blue color until a higher pressure is observed',type=float)
	parser.add_argument('--updaterate',dest='updaterate',help='Update rate in seconds',type=int)
	parser.add_argument('--log', dest='logFilename', help='Name of CSV file for logging pressure', type=str)

	return parser.parse_args()

def main():
	args = parseCmdline()

	pressureHistorySettings = {}
	if args.initiallow:
		pressureHistorySettings['initialpressurelow'] = args.initiallow
	if args.initialhigh:
		pressureHistorySettings['initialpressurehigh'] = args.initialhigh
	if args.logFilename:
		csvfile = open(args.logFilename,'w')
		pressureHistorySettings['logger'] = CSVLogger(csvfile=csvfile)

	pressureHistory = PressureHistory(**pressureHistorySettings)
	barometer = Barometer(sense_hat.SenseHat(), pressureHistory, updaterate=args.updaterate)

	barometer.run()

if __name__ == "__main__":
	main()
