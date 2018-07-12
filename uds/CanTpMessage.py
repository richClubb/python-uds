#!/usr/bin/env python

__author__ = "Richard Clubb"
__copyrights__ = "Copyright 2018, the python-uds project"
__credits__ = ["Richard Clubb"]

__license__ = "MIT"
__maintainer__ = "Richard Clubb"
__email__ = "richard.clubb@embeduk.com"
__status__ = "Development"


from CanTpTypes import CanTpMessageType, CanTpMessageState, CanTpFsType


##
#
class CanTpMessage(object):

    def __init__(self, payload=None):
        self.__payload = None
        self.__length = None
        self.__lengthExpected = None

        self.__messageState = CanTpMessageState.IDLE
        if(payload is not None):
            self.payload = payload

        self.__response = None
        self.__sequenceNumber = None
        self.__payloadPtr = 0
        self.__blockList = []
        self.__blockIndex = 0
        self.__blockPtr = 0
        self.__currBlock = None

    ##
    #
    @property
    def payload(self):
        payload = self.__payload
        if(payload is None):
            raise NotImplementedError("Payload not initialised")
        else:
            return payload

    ##
    #
    @payload.setter
    def payload(self, val):
        self.__payload = val
        self.__length = len(val)
        if(self.__length > 7):
            self.messageState = CanTpMessageState.SENDING_FF

    ##
    # @brief
    @property
    def response(self):
        return self.__response

    ##
    # @brief
    @response.setter
    def response(self, val):
        self.__response = val

    @property
    def lengthExpected(self):
        return self.__lengthExpected

    @lengthExpected.setter
    def lengthExpected(self, val):
        self.__lengthExpected = val

    @property
    def messageState(self):
        return self.__messageState

    @messageState.setter
    def messageState(self, val):
        self.__messageState = val

    ##
    # @brief
    def getNextSendFrame(self):
        payload = self.__payload
        length = self.__length
        if(length <= 7):
            self.messageState = CanTpMessageState.SENDING_SF

        output = list()
        if(self.messageState == CanTpMessageState.SENDING_SF):
            output.append(length)
            for i in range(0, 7):
                if(i < length):
                    output.append(payload[i])
                else:
                    output.append(0)
            self.messageState = CanTpMessageState.FINISHED
            return output
        elif(self.messageState == CanTpMessageState.SENDING_FF):
            highNibble = (0x10) | ((length & 0xF00) >> 8)
            lowNibble = (length & 0xFF)
            output.append(highNibble)
            output.append(lowNibble)
            for i in range(0, 6):
                output.append(payload[i])
                self.__payloadPtr += 1
            self.messageState = CanTpMessageState.WAITING_FC_CTS
            return output
        elif(self.messageState == CanTpMessageState.SENDING_CF):
            if(self.__sequenceNumber is None):
                self.__sequenceNumber = 0
            highNibble = (0x20) | (self.__sequenceNumber)
            self.__sequenceNumber = (self.__sequenceNumber + 1) % 16
            output.append(highNibble)
            blockEnd = len(self.__currBlock)
            incrementBlock = False
            blockPtr = self.__blockPtr
            for i in range(0, 7):
                if(blockPtr < blockEnd):
                    output.append(self.__currBlock[blockPtr])
                    blockPtr += 1
                    self.__payloadPtr += 1
                else:
                    output.append(0)
                    incrementBlock = True

            if((incrementBlock) | (blockPtr == blockEnd)):
                blockPtr = 0
                self.messageState = CanTpMessageState.WAITING_FC_CTS
                self.__blockIndex += 1
                if(self.__blockIndex == len(self.__blockList)):
                    self.messageState = CanTpMessageState.FINISHED
                else:
                    self.__currBlock = self.__blockList[self.__blockIndex]

            self.__blockPtr = blockPtr
            return output



    def getNextReceiveFrame(self):
        messageState = self.messageState
        output = None

        if(messageState == CanTpMessageState.SENDING_FC_CTS):
            output = [0, 0, 0, 0, 0, 0, 0, 0]
            output[0] = (CanTpMessageType.FLOW_CONTROL << 4)
            self.messageState = CanTpMessageState.RECEIVING_CF

        return output

    ##
    #
    def addToPayload(self, val):
        if(self.__payload == None):
            self.__payload = val
        else:
            self.__payload += val

    ##
    # @brief method to process the responses from the ECU
    def processResponse(self, response):
        N_PCI = (response[0] & 0xF0) >> 4
        if(N_PCI == CanTpMessageType.SINGLE_FRAME):
            self.lengthExpected = response[0] & 0x0F
            self.payload = response[1:self.lengthExpected+1]
            self.messageState = CanTpMessageState.FINISHED
        elif(N_PCI == CanTpMessageType.FIRST_FRAME):
            lengthExpected = ((response[0] & 0x0F) << 8) | (response[1])
            self.addToPayload(response[2:])
            self.lengthExpected = lengthExpected
            self.messageState = CanTpMessageState.SENDING_FC_CTS
            self.__payloadPtr = 6
        elif(N_PCI == CanTpMessageType.CONSECUTIVE_FRAME):
            sequenceCounter_last = self.__sequenceNumber
            sequenceCounter_current = (response[0] & 0x0F)
            if(sequenceCounter_last is None):
                if(sequenceCounter_current != 0):
                    raise Exception("Sequence counter out of order")
                else:
                    self.addToPayload(response[1:])
                    self.__payloadPtr += 7
                    self.__sequenceNumber = sequenceCounter_current
            else:
                sequenceCounter_next = (sequenceCounter_last + 1) % 16
                if(sequenceCounter_next != sequenceCounter_current):
                    raise Exception("Sequence counter out of order")
                else:
                    self.addToPayload(response[1:])
                    self.__payloadPtr += 7
                    self.__sequenceNumber = sequenceCounter_current

                if(self.__payloadPtr >= self.lengthExpected):
                    self.payload = self.payload[0:self.lengthExpected]
                    self.messageState = CanTpMessageState.FINISHED
            pass
        elif(N_PCI == CanTpMessageType.FLOW_CONTROL):
            fs = (response[0] & 0x0F)
            if(fs == CanTpFsType.WAIT):
                print("Wait!!!")
            elif(fs == CanTpFsType.OVERFLOW):
                Exception("OVERFLOW!!!")
            elif(fs == CanTpFsType.CTS):
                bs = response[1]
                stMin = response[2]
                if(len(self.__blockList) == 0):
                    self.blockPayload(bs)
                if(self.messageState == CanTpMessageState.WAITING_FC_CTS):
                    self.messageState = CanTpMessageState.SENDING_CF
        else:
            raise Exception("Message N_PCI not supported")
        pass

    def blockPayload(self, bs):
        payloadPtr = self.__payloadPtr
        blockSize = bs * 7
        length = self.__length
        payload = self.payload

        currBlock = []
        blockPtr = 0

        for i in range(payloadPtr, length):
            currBlock.append(payload[i])
            blockPtr += 1
            payloadPtr += 1
            if(blockPtr == blockSize):
                self.__blockList.append(currBlock)
                blockPtr = 0
                currBlock = []
            elif(payloadPtr == length):
                self.__blockList.append(currBlock)
                blockPtr = 0
                currBlock = []

        self.__currBlock = self.__blockList[blockPtr]

    def reset(self):
        self.__payload = None
        self.__length = None
        self.__lengthExpected = None
        self.__response = None
        self.__messageState = None
        self.__sequenceNumber = None
        self.__blockPtr = 0