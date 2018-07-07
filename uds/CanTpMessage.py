#!/usr/bin/env python

__author__ = "Richard Clubb"
__copyrights__ = "Copyright 2018, the python-uds project"
__credits__ = ["Richard Clubb"]

__license__ = "MIT"
__maintainer__ = "Richard Clubb"
__email__ = "richard.clubb@embeduk.com"
__status__ = "Development"

from enum import IntEnum
from CanTpExceptions import CanTpPayloadTooLarge, \
    CanTpPayloadTooLargeForSfError, \
    CanTpPayloadTooSmallForMfError


##
#
class CanTpMessageType(IntEnum):
    SINGLE_FRAME = 0
    FIRST_FRAME = 1
    CONSECUTIVE_FRAME = 2
    FLOW_CONTROL = 3
    MULTI_FRAME = 4


##
#
class CanTpMessage(object):

    def __init__(self, payload=None):
        if(payload is None):
            self.__payload = None
            self.__length = None
        else:
            self.payload = payload

        self.__dlc = None
        self.__payloadPtr = 0
        self.__blockList = []
        self.__blockPtr = 0
        self.__cfCounter = 0
        self.__bs = 0
        self.__stMin = 0

    ##
    # @brief getter method for the length of the message
    @property
    def length(self):
        if self.__length is None:
            raise TypeError("payload not initialised")
        else:
            return self.__length

    ##
    # @brief getter method for the payload of the message
    @property
    def payload(self):
        if self.__payload is None:
            raise TypeError("payload not initialised")
        else:
            return self.__payload

    ##
    # @brief setter method for the payload of the message
    @payload.setter
    def payload(self, val):
        if(len(val) > 4095):
            raise CanTpPayloadTooLarge("Payload exceeds 4095 bytes")
        self.__payload = val
        self.__length = len(val)

    ##
    # @brief method to segment the payload into blocks
    def blockPayload(self):
        payload = self.payload
        length = self.length
        payloadPtr = self.payloadPtr
        bs = self.__bs
        bs = 50

        if(bs == 0):
            self.__blockList.append(payload[payloadPtr:length])
            self.__payloadPtr = length
        while( payloadPtr < length ):
            if( ( bs - payloadPtr ) > length ):
                currBlock = payload[payloadPtr:length]
                self.__blockList.append(currBlock)
                payloadPtr = length
            else:
                end = bs+payloadPtr
                currBlock = payload[payloadPtr:end]
                self.__blockList.append(currBlock)
                payloadPtr = end
        self.__payloadPtr = length

    ##
    # @brief method to get the next frame in the sequence
    def getNextFrame(self):

        return None

    ##
    # @brief this may need improvement as there are different lengths depending on the type of TP used
    @property
    def sf(self):
        payload = []
        dlc = self.__length
        if(dlc > 7):
            raise CanTpPayloadTooLargeForSfError("Can not send payload as SF greater than 7")
        payload.append(dlc)
        for i in range(0, 7):
            if(i < dlc):
                payload.append(self.__payload[i])
            else:
                payload.append(0)
        return payload

    ##
    # @brief method to get the first frame of a multi-frame sequence
    @property
    def ff(self):
        payload = []
        dlc = self.__length
        if(dlc <= 7):
            raise CanTpPayloadTooSmallForMfError("Can not send payload as FF as smaller than 7 bytes")
        else:
            payloadHighNibble = int(self.length & 0x0F00) >> 8
            payloadLowNibble  = int(self.length & 0x00FF)
            payload.append((CanTpMessageType.FIRST_FRAME << 4) | payloadHighNibble)
            payload.append(payloadLowNibble)
            for i in range(0, 6):
                payload.append(self.__payload[i])
            self.__payloadPtr = 6
            return payload

    ##
    # @brief method to get the next consecutive frame in the sequence
    @property
    def cf(self):
        #this needs changing to suit the block segmentation
        payload = []
        payload.append((CanTpMessageType.CONSECUTIVE_FRAME << 4) | self.__cfCounter)
        self.__cfCounter = (self.__cfCounter + 1) % 16
        for i in range(0, 7):
            payload.append(self.__payload[self.__payloadPtr])
            self.__payloadPtr += 1
        return payload

    ##
    # @brief method to get the type of message
    @property
    def msgType(self):
        dlc = self.__length
        if(dlc <= 7):
            return CanTpMessageType.SINGLE_FRAME
        else:
            return CanTpMessageType.MULTI_FRAME

    ##
    # @brief method to get the current pointer in the payload
    @property
    def payloadPtr(self):
        return self.__payloadPtr

    ##
    # @brief method to process a flow-control response
    def process_fc(self, payload):
        self.__bs = payload[1]
        self.__stMin = payload[2]
        #create the blocks

if __name__ == "__main__":
    payloadVal = [10,9,8,7,6,5,4,3,2,1,0]
    a = CanTpMessage(payloadVal)
    print(a.ff)

    payloadVal = []
    for i in range(0, 0xFF):
        payloadVal.append(i)
    a = CanTpMessage(payloadVal)
    print(a.ff)
    print(a.payloadPtr)
    a.blockPayload()
