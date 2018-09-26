#!/usr/bin/env python

__author__ = "Richard Clubb"
__copyrights__ = "Copyright 2018, the python-uds project"
__credits__ = ["Richard Clubb"]

__license__ = "MIT"
__maintainer__ = "Richard Clubb"
__email__ = "richard.clubb@embeduk.com"
__status__ = "Development"


from time import perf_counter
from uds.uds_communications.Utilities.iResettableTimer import iResettableTimer


class ResettableTimer(iResettableTimer):

    def __init__(self, timeoutTime=0):

        self.__timeoutTime = timeoutTime
        self.__active_flag = False
        self.__expired_flag = False
        self.__startTime = None

    @property
    def timeoutTime(self):
        return self.__timeoutTime

    @timeoutTime.setter
    def timeoutTime(self, val):
        self.__timeoutTime = val

    def start(self):
        self.__startTime = perf_counter()
        self.__active_flag = True
        self.__expired_flag = False

    def restart(self):
        self.start()

    def stop(self):
        self.__active_flag = False
        self.__expired_flag = False

    def isRunning(self):
        self.__timerCheck()
        return self.__active_flag

    def isExpired(self):
        self.__timerCheck()
        return self.__expired_flag

    def __timerCheck(self):
        if (self.__active_flag):
            currTime = perf_counter()
            if (currTime - self.__startTime) > self.__timeoutTime:
                self.__expired_flag = True
                self.__active_flag = False


if __name__ == "__main__":

    pass
