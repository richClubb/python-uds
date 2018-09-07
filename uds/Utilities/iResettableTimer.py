#!/usr/bin/env python

__author__ = "Richard Clubb"
__copyrights__ = "Copyright 2018, the python-uds project"
__credits__ = ["Richard Clubb"]

__license__ = "MIT"
__maintainer__ = "Richard Clubb"
__email__ = "richard.clubb@embeduk.com"
__status__ = "Development"


import abc


class iResettableTimer(object):
    __metaclass__ = abc.ABCMeta

    @property
    @abc.abstractmethod
    def timeoutTime(self):
        raise NotImplementedError("class has not implemented this method")

    @timeoutTime.setter
    @abc.abstractmethod
    def timeoutTime(self, val):
        raise NotImplementedError("class has not implemented this method")

    @abc.abstractmethod
    def start(self):
        raise NotImplementedError("class has not implemented this method")

    @abc.abstractmethod
    def restart(self):
        raise NotImplementedError("class has not implemented this method")

    @abc.abstractmethod
    def stop(self):
        raise NotImplementedError("class has not implemented this method")

    @abc.abstractmethod
    def isRunning(self):
        raise NotImplementedError("class has not implemented this method")

    @abc.abstractmethod
    def isExpired(self):
        raise NotImplementedError("class has not implemented this method")