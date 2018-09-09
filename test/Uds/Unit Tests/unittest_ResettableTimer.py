#!/usr/bin/env python

__author__ = "Richard Clubb"
__copyrights__ = "Copyright 2018, the python-uds project"
__credits__ = ["Richard Clubb"]

__license__ = "MIT"
__maintainer__ = "Richard Clubb"
__email__ = "richard.clubb@embeduk.com"
__status__ = "Development"


import unittest
from Utilities.ResettableTimer import ResettableTimer
from time import sleep


class CanTpMessageTestCase(unittest.TestCase):

    ##
    # @brief tests the initialisation transition
    def testIsRunningWhenInitialised(self):
        a = ResettableTimer(0.6)
        self.assertEqual(False, a.isRunning())
        self.assertEqual(False, a.isExpired())

    ##
    # @brief tests the state after starting
    def testStategAfterStart(self):
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
    def testExpiredAfterRestart(self):
        a = ResettableTimer(0.4)
        a.start()
        sleep(0.3)
        self.assertEqual(False, a.isExpired())
        a.restart()
        sleep(0.45)
        self.assertEqual(True, a.isExpired())

    ##
    # @brief tests state for restart after expiry
    def testExpiryStateAfterExpiredThenRestart(self):
        a = ResettableTimer(0.4)
        a.start()
        sleep(0.45)
        a.restart()
        self.assertEqual(True, a.isRunning())
        self.assertEqual(False, a.isExpired())

    ##
    # @brief tests state after a stop
    def testTimerStopAfterStart(self):
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

if __name__ == "__main__":
    unittest.main()
