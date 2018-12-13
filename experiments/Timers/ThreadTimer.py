"""This file is an experiment and should not be used for any serious coding"""

from .iTimer import ITimer
from threading import Timer
import gc
from time import perf_counter


class ThreadTimer(ITimer):

    def __init__(self, timeout=0):

        self.__timeout = timeout

        self.__active_flag = False
        self.__expired_flag = False

        self.__timer = None

    def start(self):
        self.__active_flag = True
        self.__expired_flag = False
        self.__timer = Timer(self.__timeout, self.__timerFunc)
        self.__timer.start()

    def restart(self):
        self.start()

    def stop(self):
        if self.__timer is not None:
            if self.__timer.is_alive():
                self.__timer.cancel()

    def isExpired(self):
        return self.__expired_flag

    def isRunning(self):
        return self.__active_flag

    def __timerFunc(self):
        self.__expired_flag = True
        self.__active_flag = False

if __name__ == "__main__":

    a = ThreadTimer(0.001)

    gc.disable()
    results = []

    for i in range(0, 10000):
        startTime = perf_counter()
        a.start()
        while (a.isExpired() == False):
            pass
        endTime = perf_counter()
        delta = endTime - startTime
        results.append(delta)

    gc.enable()
    print("Min: {0}".format(min(results)))
    print("Max: {0}".format(max(results)))
    print("Avg: {0}".format(sum(results)/len(results)))
