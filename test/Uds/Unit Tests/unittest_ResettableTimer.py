#!/usr/bin/env python

__author__ = "Richard Clubb"
__copyrights__ = "Copyright 2018, the python-uds project"
__credits__ = ["Richard Clubb"]

__license__ = "MIT"
__maintainer__ = "Richard Clubb"
__email__ = "richard.clubb@embeduk.com"
__status__ = "Development"


import unittest
from uds import ResettableTimer
from time import sleep, perf_counter


class CanTpMessageTestCase(unittest.TestCase):

    ##
    # @brief tests the initialisation transition
    def testStateWhenInitialised(self):
        a = ResettableTimer(0.6)
        self.assertEqual(False, a.isRunning())
        self.assertEqual(False, a.isExpired())

    ##
    # @brief tests the state after starting
    def testStateAfterStart(self):
        a = ResettableTimer(0.2)
        a.start()
        self.assertEqual(True, a.isRunning())
        self.assertEqual(False, a.isExpired())

    ##
    # @brief tests state after timeout
    def testStateAfterTimeoutTime(self):
        a = ResettableTimer(0.2)
        a.start()
        sleep(0.25)
        self.assertEqual(False, a.isRunning())
        self.assertEqual(True, a.isExpired())

    ##
    # @brief tests state after reset
    def testStateAfterRestart(self):
        a = ResettableTimer(0.4)
        a.start()
        sleep(0.3)
        a.restart()
        sleep(0.2)
        self.assertEqual(True, a.isRunning())
        self.assertEqual(False, a.isExpired())

    ##
    # @brief tests state for restart while running
    def testStateAfterRestartAndExpiry(self):
        a = ResettableTimer(0.4)
        a.start()
        sleep(0.3)
        self.assertEqual(False, a.isExpired())
        self.assertEqual(True, a.isRunning())
        a.restart()
        sleep(0.45)
        self.assertEqual(True, a.isExpired())
        self.assertEqual(False, a.isRunning())

    ##
    # @brief tests state for restart after expiry
    def testStateAfterExpiredThenRestart(self):
        a = ResettableTimer(0.4)
        a.start()
        sleep(0.45)
        self.assertEqual(False, a.isRunning())
        self.assertEqual(True, a.isExpired())
        a.restart()
        self.assertEqual(True, a.isRunning())
        self.assertEqual(False, a.isExpired())

    ##
    # @brief tests state after a stop
    def testStopAfterStart(self):
        a = ResettableTimer(0.4)
        a.start()
        self.assertEqual(True, a.isRunning())
        self.assertEqual(False, a.isExpired())
        a.stop()
        self.assertEqual(False, a.isRunning())
        self.assertEqual(False, a.isExpired())

    ##
    # @brief tests state with a 0 timeout
    def testIsExpiredWith0Time(self):
        a = ResettableTimer(0)
        a.start()
        self.assertEqual(False, a.isRunning())
        self.assertEqual(True, a.isExpired())

    ##
    # @brief tests the accuracy of the timer
    def testTimerAccuracy(self):
        testTimes = [1, 0.3, 0.2, 0.1, 0.01, 0.01]
        for i in testTimes:
            a = ResettableTimer(i)
            startTime = perf_counter()
            a.start()
            while(a.isRunning()):
                pass
            endTime = perf_counter()
            delta = endTime - startTime
            self.assertAlmostEqual(delta, i, delta=0.001)


if __name__ == "__main__":
    unittest.main()
