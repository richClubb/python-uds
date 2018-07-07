#!/usr/bin/env python

__author__ = "Richard Clubb"
__copyrights__ = "Copyright 2018, the python-uds project"
__credits__ = ["Richard Clubb"]

__license__ = "MIT"
__maintainer__ = "Richard Clubb"
__email__ = "richard.clubb@embeduk.com"
__status__ = "Development"

from CanTp import CanTp
from CanTpListener import CanTpListener
from UdsMessage import UdsMessage
import time


class UdsMessageTimeoutError(Exception):

    def __init__(self, message):
        self.message = message


##
# @brief a description is needed
class Uds(object):

    ##
    # @brief a constructor
    def __init__(self, logger=None, reqId=None, resId=None):
        # this might need a factory to create the relevant class
        self.__tp = CanTp()
        self.__listener = CanTpListener()
        self.__logger = logger
        self.__reqId = reqId
        self.__resId = resId

    ##
    # @brief
    def send(self, msg):
        self.__tp.send(msg.payload)

        return 0

    def recv(self, msg, timeout_ms=0):
        startTime = time.time()
        currTime = startTime
        timeout_flag = False
        rc = -1
        while(timeout_flag is False):
            # rc = self.__tp.recv(msg)
            currTime = time.time()
            if(
                    (currTime - startTime) >
                    (timeout_ms / 1000.0)
            ): timeout_flag = True
            if(rc != -1): timeout_flag = True
        if(rc == -1):
            raise UdsMessageTimeoutError("Message timed out")
        print("Finished")


if __name__ == "__main__":
    a = Uds()
    b = UdsMessage()
    a.recv(b, 5000)
