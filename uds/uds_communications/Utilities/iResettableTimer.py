#!/usr/bin/env python

__author__ = "Richard Clubb"
__copyrights__ = "Copyright 2018, the python-uds project"
__credits__ = ["Richard Clubb"]

__license__ = "MIT"
__maintainer__ = "Richard Clubb"
__email__ = "richard.clubb@embeduk.com"
__status__ = "Development"


from abc import ABCMeta, abstractmethod


class iResettableTimer(object):
    __metaclass__ = ABCMeta

    @property
    @abstractmethod
    def timeoutTime(self):
        raise NotImplementedError("class has not implemented this method")

    @timeoutTime.setter
    @abstractmethod
    def timeoutTime(self, val):
        raise NotImplementedError("class has not implemented this method")

    @abstractmethod
    def start(self):
        raise NotImplementedError("class has not implemented this method")

    @abstractmethod
    def restart(self):
        raise NotImplementedError("class has not implemented this method")

    @abstractmethod
    def stop(self):
        raise NotImplementedError("class has not implemented this method")

    @abstractmethod
    def isRunning(self):
        raise NotImplementedError("class has not implemented this method")

    @abstractmethod
    def isExpired(self):
        raise NotImplementedError("class has not implemented this method")