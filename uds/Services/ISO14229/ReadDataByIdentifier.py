#!/usr/bin/env python

__author__ = "Richard Clubb"
__copyrights__ = "Copyright 2018, the python-uds project"
__credits__ = ["Richard Clubb"]

__license__ = "MIT"
__maintainer__ = "Richard Clubb"
__email__ = "richard.clubb@embeduk.com"
__status__ = "Development"

from UdsService import UdsService
from UdsMessage import UdsMessage
# from ISO14229 import DiagnosticId, NegativeResponseCodes

__all__ = ['ReadDataByIdentifier']


##
#
class ReadDataByIdentifier(UdsService):

    ##
    #
    def __init__(self):
        super(ReadDataByIdentifier, self).__init__()
        self.__serviceId = 0x22

    ##
    #
    def ecuSerialNumber(self):
        outputMsg = UdsMessage()
        data = []
        data.append(0x22)
        data.append(0xF1)
        data.append(0x8C)
        outputMsg.payload = data
        return outputMsg

    ##
    #
    def decode(self):
        raise NotImplementedError("No decode method implemented for this identifier")
