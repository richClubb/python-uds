#!/usr/bin/env python

__author__ = "Richard Clubb"
__copyrights__ = "Copyright 2018, the python-uds project"
__credits__ = ["Richard Clubb"]

__license__ = "MIT"
__maintainer__ = "Richard Clubb"
__email__ = "richard.clubb@embeduk.com"
__status__ = "Development"

import logging
import configparser


##
#
#
class UdsMessage(object):

    ##
    # @brief constructor method for a UdsMessage
    #
    def __init__(self, request=None):
        self.__length = None  # length can not be manually set
        self.__request = request
        self.__response = None
        self.__responseRequired = True

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
    def request(self):
        if(self.__request is None):
            raise TypeError("Request not initialised")
        return self.__request

    ##
    # @brief Sets the value of the payload
    # @param val - a list
    # @throws TypeError if the val is not a list
    @request.setter
    def request(self, val):
        self.__request = self.encodeFunc(val)
        self.__length = len(self.__request)
    ##
    # @brief
    @request.setter
    def request_raw(self, val):
        self.__request = val
        self.__length = len(self.__request)

    ##
    # @brief
    @property
    def response(self):
        raise NotImplementedError("response function not implemented")

    ##
    # @brief
    @response.setter
    def response(self, val):
        raise NotImplementedError("response set not implemented")

    ##
    # @brief
    @property
    def response_raw(self):
        return self.__response

    ##
    # @brief
    @response_raw.setter
    def response_raw(self, val):
        self.__response = val

    ##
    # @brief
    @property
    def responseRequired(self):
        return self.__responseRequired

    ##
    # @brief
    @responseRequired.setter
    def responseRequired(self, val):
        self.__responseRequired = val

    ##
    # @brief
    def decodeFunc(self):
        raise NotImplementedError("decode function not implemented for this UdsMessage")

    ##
    # @brief
    def encodeFunc(self, val):
        raise NotImplementedError("Encode function not implemented for this UdsMessage")

    ##
    # @brief
    def checkResponse(self):
        raise NotImplementedError("Check response not implemented for this UdsMessage")


if __name__ == "__main__":
    pass
