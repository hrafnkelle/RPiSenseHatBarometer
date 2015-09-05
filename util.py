import colorsys
from functools import reduce

class PressureHistory:
	MAXLEN=63

	def __init__(self):
		self.history=(None,)*PressureHistory.MAXLEN
		self.pmin=None
		self.pmax=None

	def add(self, newPressure):
		if self.max==None or newPressure>self.max:
			self.max = newPressure
		if self.min==None or newPressure<self.min:
			self.min= newPressure

		self.history = (newPressure,)+self.history[0:(len(self.history)-1)]

	def asHatList(self):
		return (None,)+self.normalized()

	def asHatHueList(self):
		return tuple(p*0.75 if p!=None else None for p in self.asHatList())

	def asHatRGBList(self):
		rgbList=tuple(list(colorsys.hsv_to_rgb(h,1,1) if h!=None else [0,0,0]) for h in self.asHatHueList())
		def to255Range(x):
			return tuple(int(xx*255) for xx in x)
		return tuple(to255Range(c) for c in rgbList)

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

def listAverage(l):
	x=reduce(lambda x, y: x+y, l)/float(len(l))
	return x
