#!/usr/bin/env python

__author__ = "Richard Clubb"
__copyrights__ = "Copyright 2018, the python-uds project"
__credits__ = ["Richard Clubb"]

__license__ = "MIT"
__maintainer__ = "Richard Clubb"
__email__ = "richard.clubb@embeduk.com"
__status__ = "Development"


from ISO14229.UdsService import UdsService
from UdsMessage import UdsMessage
from enum import IntEnum

class EcuResetSubFunctions(IntEnum):
    hardReset = 0x01
    keyOffOnReset = 0x02
    softReset = 0x03
    enableRapidPowerShutDown = 0x04
    disableRapidPowerShutDown = 0x05

# class EcuResetNegativeResponse(IntEnum):


class EcuReset(UdsService):

    def __init__(self):
        super(EcuReset, self).__init__()

    def hardReset(self, respReq=True):
        outputMsg = UdsMessage()
        outputMsg.serviceId = 0x11
        if(respReq):
            offset = 0x80
        else:
            offset = 0x00
        outputMsg.payload = [EcuResetSubFunctions.hardReset+offset]
        return outputMsg