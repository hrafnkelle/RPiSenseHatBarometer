import unittest

import util

class TestHest(unittest.TestCase):
    def test_listAverage_averageOfOneElementIsSame(self):
        self.assertEqual(util.listAverage([42]),42)


class TestPressureHistory(unittest.TestCase):
    def setUp(self):
        self.pressureHistory = util.PressureHistory()

    def test_addDoesnModifyLength(self):
        self.pressureHistory.add(1)
        self.assertEqual(len(self.pressureHistory.history), util.PressureHistory.MAXLEN)

    def test_addValueIsTheLatestValue(self):
        newPressure = 7
        self.pressureHistory.add(newPressure)
        self.assertEqual(self.pressureHistory.history[0], newPressure)

    def test_fillingHistoryHasFirstValueNextToBeForgotten(self):
        for n in range(1,util.PressureHistory.MAXLEN+1):
            self.pressureHistory.add(n)
        self.assertEqual(self.pressureHistory.history[util.PressureHistory.MAXLEN-1],1)

    def test_asHatList(self):
        minPressure = 1025
        maxPressure = 1030
        self.pressureHistory.add(minPressure)
        self.pressureHistory.add(maxPressure)
        self.assertEqual(self.pressureHistory.asHatList(), (None,1,0)+(None,)*(util.PressureHistory.MAXLEN-2))

    def test_pressureHistoryAsHueValues(self):
        minPressure = 1025
        maxPressure = 1030
        self.pressureHistory.add(minPressure)
        self.pressureHistory.add(maxPressure)
        hueList = self.pressureHistory.asHatHueList()
        self.assertEqual(hueList[0:3], (None, 0.75, 0))

    def test_pressureHistoryAsRGBList(self):
        minPressure = 1025
        maxPressure = 1030
        self.pressureHistory.add(minPressure)
        self.pressureHistory.add(maxPressure)
        self.assertEqual(self.pressureHistory.asHatRGBList()[1:3],((127,0,255),(255,0,0)))

    def test_pressureMax(self):
        maxPressure = 100
        for n in range(maxPressure+1):
            self.pressureHistory.add(n)

        self.assertEqual(self.pressureHistory.max, maxPressure)

    def test_pressureMin(self):
        maxPressure = 100
        for n in range(maxPressure+1):
            self.pressureHistory.add(n)

        self.assertEqual(self.pressureHistory.min, 0)

    def test_pressureIsNormalizedToExtremes(self):
        minPressure = 1025
        maxPressure = 1030
        self.pressureHistory.add(minPressure)
        self.pressureHistory.add(maxPressure)
        self.pressureHistory.add((minPressure+maxPressure)/2)
        self.assertEqual(self.pressureHistory.normalized()[0:3],(0.5,1,0))

    def test_normalizedPressureIsFullLengthWithNoneIfNoValueAdded(self):
        self.assertEqual(self.pressureHistory.normalized(), (None,)*self.pressureHistory.MAXLEN)

    def test_normalizedPressureHistoryHasExtremesAndNoneIfFewAdded(self):
        minPressure = 1025
        maxPressure = 1030
        self.pressureHistory.add(minPressure)
        self.pressureHistory.add(maxPressure)
        self.assertEqual(self.pressureHistory.normalized(),(1,0)+(None,)*(self.pressureHistory.MAXLEN-2))

    def test_normalizeOneValueClamps(self):
        minPressure = 1025
        maxPressure = 1030
        self.pressureHistory.add(minPressure)
        self.pressureHistory.add(maxPressure)
        self.assertEqual(self.pressureHistory.normalizeOneValue(minPressure-1), 0)
        self.assertEqual(self.pressureHistory.normalizeOneValue(maxPressure+1), 1)

    def test_normalizeOneValueWhenNothingAdded(self):
        somePressure = 1020
        someOtherPressure = 1031
        self.pressureHistory.add(somePressure)
        self.assertEqual(self.pressureHistory.normalizeOneValue(someOtherPressure), 0.5)

    def test_normalizeOneValueWhenOneAddedIsHalf(self):
        self.assertEqual(self.pressureHistory.normalizeOneValue(1020), 0.5)

    def test_normalizeOneValueNoneIsNone(self):
        self.assertEqual(self.pressureHistory.normalizeOneValue(None), None)

if __name__ == '__main__':
    unittest.main()
