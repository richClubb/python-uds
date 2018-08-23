import unittest
from Utilities.TimerState import TimerState
from Utilities.ResettableTimer import ResettableTimer
#from Utilities.ResettableTimerThreaded import ResettableTimerThreaded as ResettableTimer
import time

class CanTpMessageTestCase(unittest.TestCase):

    def testStateWhenInitialised(self):
        a = ResettableTimer(0.6)
        self.assertEqual(TimerState.STOPPED, a.state)

    def testStateWhenStarted(self):
        a = ResettableTimer(0.6)
        a.start()
        self.assertEqual(TimerState.RUNNING, a.state)

    def testExpiredAfterStarted(self):
        pass

    def testStateWhenExpired(self):
        a = ResettableTimer(0.5)
        a.start()
        time.sleep(0.6)
        self.assertEqual(TimerState.STOPPED, a.state)

    def testIsExpired(self):
        a = ResettableTimer(0.5)
        a.start()
        time.sleep(0.6)
        self.assertEqual(True, a.expired())

    def testNotExpired(self):
        a = ResettableTimer(0.5)
        a.start()
        time.sleep(0.4)
        self.assertEqual(False, a.expired())

    def testResetTimerStateCheckBeforeExpiry(self):
        a = ResettableTimer(0.5)
        a.start()
        time.sleep(0.4)
        a.reset()
        time.sleep(0.4)
        self.assertEqual(TimerState.RUNNING, a.state)

    def testResetTimerStateCheckBeforeAndAfterExpiry(self):
        a = ResettableTimer(0.5)
        a.start()
        time.sleep(0.4)
        a.reset()
        time.sleep(0.4)
        self.assertEqual(TimerState.RUNNING, a.state)
        time.sleep(0.2)
        self.assertEqual(TimerState.STOPPED, a.state)

    def testResetTimerExpiredCheckBeforeAndAfterExpiry(self):
        a = ResettableTimer(0.5)
        a.start()
        time.sleep(0.4)
        self.assertEqual(False, a.expired())
        time.sleep(0.2)
        self.assertEqual(True, a.expired())

    def testExpiryWhenTimeoutIsZero(self):
        a = ResettableTimer(0)
        a.start()
        self.assertEqual(True, a.expired())

    def testStateAfterRunWhenTimeoutIsZero(self):
        a = ResettableTimer(0)
        a.start()
        self.assertEqual(TimerState.STOPPED, a.state)

    def testTimeoutChangedWhileStopped(self):
        a = ResettableTimer(0.5)
        a.timeoutTime = 0.7
        a.start()
        time.sleep(0.6)
        self.assertEqual(TimerState.RUNNING, a.state)
        time.sleep(0.2)
        self.assertEqual(TimerState.STOPPED, a.state)

    def testTimeoutChangedWhileRunning(self):
        a = ResettableTimer(1)
        a.start()
        time.sleep(0.4)
        self.assertEqual(TimerState.RUNNING, a.state)
        a.timeoutTime = 0.5
        time.sleep(0.1)
        self.assertEqual(TimerState.STOPPED, a.state)

    def testResetWhenStopped(self):
        a = ResettableTimer(0.5)
        a.reset()
        self.assertEqual(TimerState.RUNNING, a.state)
        time.sleep(0.4)
        self.assertEqual(TimerState.RUNNING, a.state)
        time.sleep(0.2)
        self.assertEqual(TimerState.STOPPED, a.state)

if __name__ == "__main__":
    unittest.main()
