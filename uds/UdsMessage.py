#!/usr/bin/env python

__author__ = "Richard Clubb"
__copyrights__ = "Copyright 2018, the python-uds project"
__credits__ = ["Richard Clubb"]

__license__ = "MIT"
__maintainer__ = "Richard Clubb"
__email__ = "richard.clubb@embeduk.com"
__status__ = "Development"


##
#
#
class UdsMessage(object):

    ##
    # @brief constructor method for a UdsMessage
    #
    def __init__(self, payload=None):
        self.__length = None  # length can not be manually set
        self.__payload = payload
        pass

    ##
    # @brief getter function for the length
    # @return an integer, the length of the payload
    @property
    def length(self):
        if(self.__length is None):
            raise TypeError("no length, payload not initialised")
        return self.__length

    ##
    # @brief function to get the payload of the uds message
    # @throws TypeError if the payload is not initialised
    # @returns a list - the payload of the message
    @property
    def payload(self):
        if(self.__payload is None):
            raise TypeError("Payload not initialised")
        return self.__payload

    ##
    # @brief Sets the value of the payload
    # @param val - a list
    # @throws TypeError if the val is not a list
    @payload.setter
    def payload(self, val):
        if type(val) == list:
            self.__length = len(val)
            self.__payload = val
        else:
            raise TypeError("Attempt to enter non-list value to payload")

    @property
    def raw(self):
        return self.__payload

    @property
    def decode(self):
        raise NotImplementedError("decode function not implemented for this UdsMessage")

    def decodeFunc(self):
        raise NotImplementedError("decode function not implemented for this UdsMessage")

if __name__ == "__main__":
    pass
