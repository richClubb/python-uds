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

    def testIsRunningWhenInitialised(self):
        a = ResettableTimer(0.6)
        result = a.isRunning()

        self.assertEqual(False, result)


    def testIsExpiredWhenInitialised(self):
        a = ResettableTimer(0.2)
        result = a.isExpired()

        self.assertEqual(False, result)

    def testIsRunningAfterStart(self):
        a = ResettableTimer(0.2)
        a.start()
        result = a.isRunning()

        self.assertEqual(True, result)

    def testIsExpiredAfterStart(self):
        a = ResettableTimer(0.2)
        a.start()
        result = a.isExpired()

        self.assertEqual(False, result)

    def testIsRunningAfterTimeoutTime(self):
        a = ResettableTimer(0.2)
        a.start()
        sleep(0.25)
        result = a.isRunning()

        self.assertEqual(False, result)

    def testIsExpiredAfterTimeoutTime(self):
        a = ResettableTimer(0.2)
        a.start()
        sleep(0.25)
        result = a.isExpired()

        self.assertEqual(True, result)

    def testIsRunningAfterRestart(self):
        a = ResettableTimer(0.4)
        a.start()
        sleep(0.3)
        a.restart()
        sleep(0.2)
        result = a.isRunning()

        self.assertEqual(True, result)

    def testIsExpiredAfterRestart(self):
        a = ResettableTimer(0.4)
        a.start()
        sleep(0.3)
        a.restart()
        sleep(0.2)
        result = a.isExpired()

        self.assertEqual(False, result)

    def testExpiredAfterRestart(self):
        a = ResettableTimer(0.4)
        a.start()
        sleep(0.3)
        result = a.isExpired()
        self.assertEqual(False, result)
        a.restart()
        sleep(0.45)
        result = a.isExpired()
        self.assertEqual(True, result)

if __name__ == "__main__":
    unittest.main()
