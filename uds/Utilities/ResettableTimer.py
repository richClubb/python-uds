from time import time
from Utilities.iResettableTimer import iResettableTimer
from Utilities.TimerState import TimerState


class ResettableTimer(iResettableTimer):

    def __init__(self, timeoutTime):
        self.__timeoutTime = timeoutTime
        self.__running = False
        self.__state = TimerState.STOPPED

    @property
    def timeoutTime(self):
        return self.__timeoutTime

    @timeoutTime.setter
    def timeoutTime(self, val):
        self.__timeoutTime = val

    @property
    def state(self):
        _ = self.expired()
        return self.__state

    def start(self):
        self.__startTime = time()
        self.__running = True
        self.__state = TimerState.RUNNING

    def reset(self):
        self.start()

    def stop(self):
        self.__expired = False
        self.__state = TimerState.STOPPED

    def isRunning(self):
        _ = self.expired()
        return self.__running

    ##
    # @brief checks if the timer has expired
    # the check to see if the timeoutTime == 0 is due to a limitation in the
    # time comparison. If the timer is tarted  (with a timeout of 0) and then
    # checked if it is running immediately it will think it i running.
    def expired(self):
        if(self.__timeoutTime == 0):
            self.__running = False
            self.__state = TimerState.STOPPED
            return True
        if(self.__running):
            startTime = self.__startTime
            currTime = time()
            timeoutTime = self.__timeoutTime
            delta = currTime - startTime
            if(delta > timeoutTime):
                self.__running = False
                self.__state = TimerState.STOPPED
                return True
            else:
                self.__state = TimerState.RUNNING
                return False
        else:
            return False


if __name__ == "__main__":

    pass
