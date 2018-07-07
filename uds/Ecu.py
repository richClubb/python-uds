#!/usr/bin/env python

__author__ = "Richard Clubb"
__copyrights__ = "Copyright 2018, the python-uds project"
__credits__ = ["Richard Clubb"]

__license__ = "MIT"
__maintainer__ = "Richard Clubb"
__email__ = "richard.clubb@embeduk.com"
__status__ = "Development"

from Uds import Uds
from UdsMessage import UdsMessage


class Ecu(object):

    def __init__(self, reqId=0, resId=0, stMin=0, bs=0):
        self.__reqId = reqId
        self.__resId = resId
        self.__stMin = stMin
        self.__bs = bs

        self.__udsChannel = Uds(logger=None, reqId=self.__reqId, resId=self.__resId)

        # this part defines how the services are loaded

    def send(self, msg, respReq=True):
        self.__udsChannel.send(msg)

        if(respReq is False):
            self.__udsChannel.recv(msg)
        else:
            return None

