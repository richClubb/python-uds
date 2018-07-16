#!/usr/bin/env python

__author__ = "Richard Clubb"
__copyrights__ = "Copyright 2018, the python-uds project"
__credits__ = ["Richard Clubb"]

__license__ = "MIT"
__maintainer__ = "Richard Clubb"
__email__ = "richard.clubb@embeduk.com"
__status__ = "Development"

from CanTp import CanTp
from UdsMessage import UdsMessage
import time
import config
import logging


class UdsMessageTimeoutError(Exception):

    def __init__(self, message):
        self.message = message


##
# @brief a description is needed
class Uds(object):

    ##
    # @brief a constructor
    def __init__(self, reqId=None, resId=None):
        # this might need a factory to create the relevant class
        self.__tp = CanTp(reqId, resId)
        self.__reqId = reqId
        self.__resId = resId

        # set up logger
        self.__logger = logging.getLogger('python-uds')

    ##
    # @brief
    def send(self, msg):
        self.__tp.send(msg.request)
        response = None

        if(msg.responseRequired):
            msg.response_raw = self.__tp.recv(5000)

        return response


if __name__ == "__main__":
    a = Uds()
    b = UdsMessage()
    a.recv(b, 5000)
