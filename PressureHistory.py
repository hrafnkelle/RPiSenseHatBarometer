import colorsys
from functools import reduce

class PressureHistory:
	MAXLEN=63

	def __init__(self):
		self.history=(None,)*PressureHistory.MAXLEN
		self.pressureAccumulator = ()
		self.pmin=None
		self.pmax=None

	def add(self, newPressure):
		if self.max==None or newPressure>self.max:
			self.max = newPressure
		if self.min==None or newPressure<self.min:
			self.min= newPressure

		self.history = (newPressure,)+self.history[0:(len(self.history)-1)]

	def addFromIterator(self, iter):
		for p in iter:
			self.add(p)

	@property
	def max(self):
		return self.pmax
	@max.setter
	def max(self,value):
		self.pmax = value
	@property
	def min(self):
		return self.pmin
	@min.setter
	def min(self,value):
		self.pmin = value

	def normalizeOneValue(self, pressure):
		if pressure==None:
			return None
		if self.max==self.min or self.max==None or self.min==None:
			return 0.5
		normalizedValue = (pressure-self.min)/(self.max-self.min)
		return min(1,max(0,normalizedValue))

	def normalized(self):
		return tuple(self.normalizeOneValue(p) for p in self.history)

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
