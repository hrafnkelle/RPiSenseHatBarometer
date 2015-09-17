import unittest
import mock

from PressureHistory import PressureHistory, LEDMatrixAdapter
from Barometer import Barometer

class TestPressureHistoryInit(unittest.TestCase):
    def test_initReadsFromKwargs(self):
        settings = {'initialpressurelow': 950, 'initialpressurehigh':1020}
        pressureHistory = PressureHistory(**settings)
        self.assertEqual(pressureHistory.min, settings['initialpressurelow'])
        self.assertEqual(pressureHistory.max, settings['initialpressurehigh'])

    def test_initialLimitsOverridesHistoryExtremesIfHistoryBoundedByInitialLimits(self):
        settings = {'initialpressurelow': 950, 'initialpressurehigh':1020}
        pressureHistory = PressureHistory(**settings)
        pressureHistory.add(951)
        pressureHistory.add(1019)
        self.assertEqual(pressureHistory.min, settings['initialpressurelow'])
        self.assertEqual(pressureHistory.max, settings['initialpressurehigh'])

class TestPressureHistory(unittest.TestCase):
    def setUp(self):
        self.pressureHistory = PressureHistory()

    def test_averageOfSingleValueIsSingleValue(self):
        somePressure = 42
        self.pressureHistory.includeInAverage(somePressure)
        avgPressure=self.pressureHistory.averageOfAccumulated()
        self.assertEqual(avgPressure, somePressure)

    def test_averageOfNoValuesIsNone(self):
        avgPressure=self.pressureHistory.averageOfAccumulated()
        self.assertEqual(avgPressure, None)

    def test_addingAccumulatedAverageResetsAccumulator(self):
        somePressures = (42,41,40)
        for p in somePressures:
            self.pressureHistory.includeInAverage(p)
        self.pressureHistory.addFromAccumulator()
        self.assertEqual(len(self.pressureHistory.pressureAccumulator), 0)

    def test_addingAccumulatedAverageIsInPressureHistory(self):
        somePressure=1020
        otherPressure=1001
        self.pressureHistory.add(somePressure)
        self.pressureHistory.includeInAverage(otherPressure)
        self.pressureHistory.addFromAccumulator()
        self.assertEqual(self.pressureHistory.history[0],otherPressure)
        self.assertEqual(self.pressureHistory.history[1],somePressure)

    def test_latestValueAddedCanBeQueriedFor(self):
        somePressure=1021
        self.pressureHistory.add(somePressure)
        self.assertEqual(self.pressureHistory.latestAdded(), somePressure)

    def test_addDoesnModifyLength(self):
        self.pressureHistory.add(1)
        self.assertEqual(self.pressureHistory.history.maxlen, PressureHistory.MAXLEN)

    def test_addValueIsTheLatestValue(self):
        newPressure = 7
        self.pressureHistory.add(newPressure)
        self.assertEqual(self.pressureHistory.history[0], newPressure)

    def test_fillingHistoryHasFirstValueNextToBeForgotten(self):
        for n in range(1,PressureHistory.MAXLEN+1):
            self.pressureHistory.add(n)
        self.assertEqual(self.pressureHistory.history[PressureHistory.MAXLEN-1],1)

    def test_pressureMax(self):
        maxPressure = 100
        for n in range(maxPressure+1):
            self.pressureHistory.add(n)

        self.assertEqual(self.pressureHistory.max, maxPressure)

    def test_pressureMin(self):
        maxPressure = 100
        for n in range(maxPressure+1):
            self.pressureHistory.add(n)

        self.assertEqual(self.pressureHistory.min, maxPressure-self.pressureHistory.history.maxlen+1)

    def test_pressureIsNormalizedToExtremes(self):
        minPressure = 1025
        maxPressure = 1030
        self.pressureHistory.add(minPressure)
        self.pressureHistory.add(maxPressure)
        self.pressureHistory.add((minPressure+maxPressure)/2)
        self.assertEqual(self.pressureHistory.normalized()[0:3],[0.5,1,0])

    def test_normalizedPressureIsFullLengthWithNoneIfNoValueAdded(self):
        self.assertEqual(self.pressureHistory.normalized(), [None]*self.pressureHistory.MAXLEN)

    def test_normalizedPressureHistoryHasExtremesAndNoneIfFewAdded(self):
        minPressure = 1025
        maxPressure = 1030
        self.pressureHistory.add(minPressure)
        self.pressureHistory.add(maxPressure)
        self.assertEqual(self.pressureHistory.normalized(),[1,0]+[None]*(self.pressureHistory.MAXLEN-2))

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

    def test_addFromIterator(self):
        self.pressureHistory.addFromIterator(iter((1,2,3,4)))

        self.assertEqual(self.pressureHistory.max, 4)
        self.assertEqual(self.pressureHistory.min, 1)

class TestLEDMatrixAdapter(unittest.TestCase):

    def test_hueListretrievesNormalizedHistory(self):
        mock_pressureHistory = mock.create_autospec(PressureHistory)
        ledAdapter = LEDMatrixAdapter(mock_pressureHistory)
        ledAdapter.asHueList()
        self.assertTrue(mock_pressureHistory.normalized.called,"Didn't get the normalized pressure history")

    def test_hueListIsInRedBlueRange(self):
        mock_pressureHistory = mock.create_autospec(PressureHistory)
        mock_pressureHistory.normalized.return_value = (0,1)

        ledAdapter = LEDMatrixAdapter(mock_pressureHistory)
        hueList = ledAdapter.asHueList()
        self.assertEqual(hueList,(ledAdapter.MINHUE,ledAdapter.MAXHUE))

    def testHueListMapsNoneToNone(self):
        mock_pressureHistory = mock.create_autospec(PressureHistory)
        mock_pressureHistory.normalized.return_value = (None,)

        ledAdapter = LEDMatrixAdapter(mock_pressureHistory)
        hueList = ledAdapter.asHueList()
        self.assertEqual(hueList,(None,))

    def test_normalRangeTo255Range(self):
        self.assertEqual(LEDMatrixAdapter.to255Range((0,0.5,1)),(int(0),int(0.5*255),int(255)))


    def test_RGBListIs64ElementsLong(self):
        mock_pressureHistory = mock.create_autospec(PressureHistory)
        mock_pressureHistory.normalized.return_value = (0,)*PressureHistory.MAXLEN

        ledAdapter = LEDMatrixAdapter(mock_pressureHistory)
        self.assertEqual(len(ledAdapter.asHatRGBList()),64)

    def test_RGBListHasBlankInFront(self):
        mock_pressureHistory = mock.create_autospec(PressureHistory)
        mock_pressureHistory.normalized.return_value = (0,)*PressureHistory.MAXLEN

        ledAdapter = LEDMatrixAdapter(mock_pressureHistory)
        self.assertEqual(ledAdapter.asHatRGBList()[0],(0,0,0))

    def test_extermeNormalizedPressuresResultInRedToBlueWithBlankInFront(self):
        mock_pressureHistory = mock.create_autospec(PressureHistory)
        mock_pressureHistory.normalized.return_value = (0,1)

        ledAdapter = LEDMatrixAdapter(mock_pressureHistory)

        self.assertEqual(ledAdapter.asHatRGBList(),((0,0,0),(255,0,0),(0,0,255)))


class TestBarometer(unittest.TestCase):

    def setUp(self):
        self.mock_senseHat = mock.Mock()
        self.mock_pressureHistory = mock.create_autospec(PressureHistory)
        self.barometer = Barometer(self.mock_senseHat, self.mock_pressureHistory)

    def test_clearsMatrixOnStartup(self):
        self.mock_senseHat.clear.assert_called_with()

class TestBarometerInit(unittest.TestCase):
    def test_readsUpdateRateFromKeyValueInitArgs(self):
        mock_senseHat = mock.Mock()
        mock_pressureHistory = mock.create_autospec(PressureHistory)

        settings = {'updaterate': 10}
        barometer = Barometer(mock_senseHat, mock_pressureHistory, **settings)
        self.assertEqual(barometer.updateInterval, settings['updaterate']*Barometer.TICKS_PER_SECOND)

    def test_usesDefaultUpdateIntervaIfNotProvided(self):
        mock_senseHat = mock.Mock()
        mock_pressureHistory = mock.create_autospec(PressureHistory)

        barometer = Barometer(mock_senseHat, mock_pressureHistory)
        self.assertEqual(barometer.updateInterval, Barometer.DEFAULT_UPDATE_INTERVAL)

    def test_usesDefaultUpdateIntervaIfNoneProvided(self):
        mock_senseHat = mock.Mock()
        mock_pressureHistory = mock.create_autospec(PressureHistory, updaterate=None)

        barometer = Barometer(mock_senseHat, mock_pressureHistory)
        self.assertEqual(barometer.updateInterval, Barometer.DEFAULT_UPDATE_INTERVAL)



if __name__ == '__main__':
    unittest.main()
