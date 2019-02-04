#!/usr/bin/env python

__author__ = "Richard Clubb"
__copyrights__ = "Copyright 2018, the python-uds project"
__credits__ = ["Richard Clubb"]

__license__ = "MIT"
__maintainer__ = "Richard Clubb"
__email__ = "richard.clubb@embeduk.com"
__status__ = "Development"


from abc import ABCMeta, abstractmethod


class iTp(object):
    __metaclass__ = ABCMeta

    ##
    # @brief interface method
    @abstractmethod
    def send(self, payload):
        raise NotImplementedError("send function not implemented")

    ##
    # @brief interface method
    @abstractmethod
    def recv(self, timeout_ms):
        raise NotImplementedError("receive function not implemented")

    ##
    # @brief interface method
    @abstractmethod
    def closeConnection(self):
        raise NotImplementedError("closeConnection function not implemented")