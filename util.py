import colorsys
from functools import reduce

class PressureHistory:
	MAXLEN=63

	def __init__(self):
		self.history=[None]*PressureHistory.MAXLEN

	def add(self, newPressure):
		self.history.pop()
		self.history.insert(0, newPressure)

	def asHatList(self):
		return [None]+self.history

	def asHatHueList(self):
		return [pressureToHue(p) for p in self.asHatList()]

	def asHatRGBList(self):
		rgbList=[list(colorsys.hsv_to_rgb(h,1,1) if h!=None else [0,0,0]) for h in self.asHatHueList()]
		def to255Range(x):
			return [int(xx*255) for xx in x]
		return [to255Range(c) for c in rgbList]

pressureMin = 1020
pressureMax = 1030


def pressureToHue(pressure):

	if pressure==None:
		return None
	else:
		normalizedPressure = (pressure - pressureMin)/(pressureMax-pressureMin)
		return min(0.75,max(0,0.75*(1-normalizedPressure)))

def listAverage(l):
	x=reduce(lambda x, y: x+y, l)/float(len(l))
	return x

def nextPixel(currPixel):
	nextPixelNum = currPixel[0]*8 + currPixel[1] +1
	return ((nextPixelNum//8)%8, nextPixelNum%8)
