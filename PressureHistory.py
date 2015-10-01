import csv
import colorsys
import datetime
import collections

class PressureHistory:
	MAXLEN=63

	def __init__(self, **kwargs):
		self.history = collections.deque(maxlen=PressureHistory.MAXLEN)
		self.pressureAccumulator = ()
		self.lowestObservedPressure=kwargs['initialpressurelow'] if 'initialpressurelow' in kwargs else float('Inf')
		self.highestObservedPressure=kwargs['initialpressurehigh'] if 'initialpressurehigh' in kwargs else float('-Inf')

		if 'logger' in kwargs:
			self.logger = kwargs['logger']
		else:
			self.logger = NoLogger()

	def add(self, newPressure):
		self.history.appendleft(newPressure)
		self.lowestObservedPressure = min(self.lowestObservedPressure,newPressure)
		self.highestObservedPressure = max(self.highestObservedPressure,newPressure)
		self.logger.log(newPressure)

	def addFromIterator(self, iter):
		for p in iter:
			self.add(p)

	@property
	def max(self):
		return self.highestObservedPressure
	@property
	def min(self):
		return self.lowestObservedPressure

	def normalizeOneValue(self, pressure):
		if pressure==None:
			return None
		if len(self.history)<=1 or self.max==self.min: #self.max==None or self.min==None:
			return 0.5
		normalizedValue = (pressure-self.min)/(self.max-self.min)
		return min(1,max(0,normalizedValue))

	def normalized(self):
		return [self.normalizeOneValue(p) for p in self.history]+[None]*(self.history.maxlen-len(self.history))

	def averageOfAccumulated(self):
		if len(self.pressureAccumulator):
			return sum(self.pressureAccumulator)/len(self.pressureAccumulator)
		return None

	def includeInAverage(self, pressureValue):
		self.pressureAccumulator = (pressureValue,)+self.pressureAccumulator

	def addFromAccumulator(self):
		self.add(self.averageOfAccumulated())
		self.pressureAccumulator=()

	def latestAdded(self):
		return self.history[0]


class LEDMatrixAdapter:
	MINHUE = 0
	MAXHUE = float(2/3)

	def __init__(self, pressureHistory):
		self.pressureHistory = pressureHistory

	@staticmethod
	def normalValueAsHue(normalizedPressure):
		return normalizedPressure*LEDMatrixAdapter.MAXHUE if normalizedPressure!=None else None

	def asHueList(self):
		normHistory = self.pressureHistory.normalized()
		return tuple(LEDMatrixAdapter.normalValueAsHue(p) for p in normHistory)

	@staticmethod
	def to255Range(x):
		return tuple(int(xx*255) for xx in x)

	def asHatRGBList(self):
		rgbList=tuple(list(colorsys.hsv_to_rgb(h,1,1) if h!=None else [0,0,0]) for h in (None,)+self.asHueList())
		return tuple(LEDMatrixAdapter.to255Range(c) for c in rgbList)

class Logger:
	def log(self, value):
		pass

class NoLogger(Logger):
	pass

class CSVLogger:
	def __init__(self, csvfile=None):
		self.writer = csv.writer(csvfile)
		pass

	def log(self, value):
		nowStr = datetime.datetime.strftime(datetime.datetime.now(),"%Y-%m-%d %H:%M:%S")
		self.writer.writerow([nowStr, value])
		pass
