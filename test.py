import unittest

import util

class TestHest(unittest.TestCase):
    def test_pressureToHue(self):
        pressure=0
        col = util.pressureToHue(pressure)
        self.assertTrue(col>=0)
        self.assertTrue(col<=255)

    def test_listAverage_averageOfOneElementIsSame(self):
        self.assertEqual(util.listAverage([42]),42)

    def test_nextPixel(self):
        self.assertEqual(util.nextPixel((0,0)),(0,1))
        self.assertEqual(util.nextPixel((7,7)),(0,0))
        self.assertEqual(util.nextPixel((0,7)),(1,0))
        self.assertEqual(util.nextPixel((5,0)),(5,1))

    def test_nonePressureNoneHue(self):
        self.assertEqual(util.pressureToHue(None),None)

class TestPressureHistory(unittest.TestCase):

    def test_addDoesnModifyLength(self):
        pressureHistory = util.PressureHistory()
        pressureHistory.add(1)
        self.assertEqual(len(pressureHistory.history), util.PressureHistory.MAXLEN)

    def test_addValueIsTheLatestValue(self):
        pressureHistory = util.PressureHistory()
        newPressure = 7
        pressureHistory.add(newPressure)
        self.assertEqual(pressureHistory.history[0], newPressure)

    def test_fillingHistoryHasFirstValueNextToBeForgotten(self):
        pressureHistory = util.PressureHistory()
        for n in range(1,util.PressureHistory.MAXLEN+1):
            pressureHistory.add(n)
        self.assertEqual(pressureHistory.history[util.PressureHistory.MAXLEN-1],1)

    def test_asHatList(self):
        pressureHistory = util.PressureHistory()
        newPressure = 3
        pressureHistory.add(newPressure)
        self.assertEqual(pressureHistory.asHatList()[1], newPressure)
        self.assertEqual(pressureHistory.asHatList()[0], None)

    def test_pressureHistoryAsHueValues(self):
        pressureHistory = util.PressureHistory()
        pressureHistory.add(1028)
        pressureHistory.add(1033)
        hueList = pressureHistory.asHatHueList()
        self.assertEqual(hueList[0:3], [None, 0.75, 0])

    def test_pressureHistoryAsRGBList(self):
        pressureHistory = util.PressureHistory()
        pressureHistory.add(1028)
        pressureHistory.add(1033)
        self.assertEqual(pressureHistory.asHatRGBList()[1:3],[[127,0,255],[255,0,0]])

if __name__ == '__main__':
    unittest.main()
