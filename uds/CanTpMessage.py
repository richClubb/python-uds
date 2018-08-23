#!/usr/bin/env python

__author__ = "Richard Clubb"
__copyrights__ = "Copyright 2018, the python-uds project"
__credits__ = ["Richard Clubb"]

__license__ = "MIT"
__maintainer__ = "Richard Clubb"
__email__ = "richard.clubb@embeduk.com"
__status__ = "Development"


from CanTpTypes import CanTpMessageState


##
#
class CanTpMessage(object):

    ##
    # @brief
    def __init__(self, payload):

        self.__state = CanTpMessageState.INIT

        self.__payload = payload
        self.__length = len(payload)

        self.__blockList = []
        self.__blockPtr = 0
        self.__payloadPtr = 0

        self.processState() # begins the state processing

    ##
    # @brief, getter method for the message.
    # @returns a CanTpMessageState enumeration
    @property
    def state(self):
        return self.__state

    ##
    # @brief getter method for the length of the message
    # @returns an integer corresponding to the length of the message
    @property
    def length(self):
        return self.__length

    ##
    # @brief process the message state machine
    def processState(self):

        state = self.__state
        output = None

        # if
        if state == CanTpMessageState.INIT:
            length = self.__length
            if(length == 0):
                newState = CanTpMessageState.INIT
            elif(length <= 7):
                newState = CanTpMessageState.SINGLE_FRAME
            else:
                newState = CanTpMessageState.FIRST_FRAME
        elif(state == CanTpMessageState.SINGLE_FRAME):
            payload = self.__payload
            length = self.__length
            output = [0, 0, 0, 0, 0, 0, 0]
            for i in range(0, length):
                output[i] = payload[i]
            newState = CanTpMessageState.END_OF_MESSAGE
        elif(state == CanTpMessageState.FIRST_FRAME):
            output = self.__payload[0:6]
            self.__payloadPtr = 6
            newState = CanTpMessageState.END_OF_BLOCK
        elif(state == CanTpMessageState.CONSECUTIVE_FRAME):
            block = self.__blockList[0]
            blockLength = len(block)
            blockPtr = self.__blockPtr
            payloadPtr = self.__payloadPtr
            output = [0, 0, 0, 0, 0, 0, 0]
            newState = CanTpMessageState.CONSECUTIVE_FRAME
            for i in range(0, 7):
                if(blockPtr < blockLength):
                    output[i] = block[blockPtr]
                    blockPtr += 1
                    payloadPtr += 1
            if(blockPtr == blockLength):
                _ = self.__blockList.pop(0)
                newState = CanTpMessageState.END_OF_BLOCK
            if(len(self.__blockList) == 0):
                newState = CanTpMessageState.END_OF_MESSAGE
            self.__blockPtr = blockPtr
            self.__payloadPtr = payloadPtr

        elif(state == CanTpMessageState.END_OF_BLOCK):
            newState = CanTpMessageState.CONSECUTIVE_FRAME
        self.__state = newState
        return output

    ##
    # @brief calculates the remaining payload blocking
    # @param [in] bs The blocksize required for the receiver end.
    def blockPayload(self, bs):
        blockSize = bs * 7

        #special case where the server doesn't have any constraints
        if (blockSize == 0):
            payloadPtr = self.__payloadPtr
            block = self.__payload[payloadPtr:]
            self.__blockList.append(block)

        #chunk payload into managable chunks
        else:
            payloadPtr = self.__payloadPtr
            payload = self.__payload[payloadPtr:]
            i = 0
            j = 0
            length = len(payload)
            block = []
            blockList = []
            while(i < length):
                block.append(payload[i])
                i += 1
                j += 1
                if(j == blockSize):
                    blockList.append(block)
                    block = []
                    j = 0
                elif(i == length):
                    blockList.append(block)
            self.__blockList = blockList
            self.__blockPtr = 0

    ##
    # @brief checks if the message is at the end
    # could be deprecated.
    def isEndOfMessage(self):
        state = self.__state
        if(state == CanTpMessageState.END_OF_MESSAGE):
            return True
        else:
            return False

if __name__ == "__main__":
    pass