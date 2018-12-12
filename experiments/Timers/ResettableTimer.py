"""This file is an experiment and should not be used for any serious coding"""

from .iTimer import ITimer
from time import perf_counter
import gc

class ResettableTimer(ITimer):

    def __init__(self, timeout=0):

        self.__timeout = timeout

        self.__active_flag = False
        self.__expired_flag = False

        self.__startTime = 0

    def start(self):
        self.__startTime = perf_counter()
        self.__active_flag = True
        self.__expired_flag = False

    def restart(self):
        self.start()

    def stop(self):
        self.__active_flag = False

    def isExpired(self):
        if(self.__active_flag):
            if (perf_counter() - self.__startTime) > self.__timeout:
                self.__active_flag = False
                self.__expired_flag = True
                return self.__expired_flag
            else:
                return False
        return self.__expired_flag

    def isRunning(self):
        return self.__active_flag


if __name__ == "__main__":
    a = ResettableTimer(0.001)

    results = []
    for i in range(0, 10000):
        startTime = perf_counter()
        a.start()
        while (a.isExpired() == False):
            pass
        endTime = perf_counter()
        delta = endTime - startTime
        results.append(delta)

    print("Min: {0}".format(min(results)))
    print("Max: {0}".format(max(results)))
    print("Avg: {0}".format(sum(results)/len(results)))
