#!/usr/bin/env python

__author__ = "Richard Clubb"
__copyrights__ = "Copyright 2018, the python-uds project"
__credits__ = ["Richard Clubb"]

__license__ = "MIT"
__maintainer__ = "Richard Clubb"
__email__ = "richard.clubb@embeduk.com"
__status__ = "Development"

from uds import iTp
##
# @brief pads out an array with a fill value
def fillArray(data, length, fillValue=0):
    output = []
    for i in range(0, length):
        output.append(fillValue)
    for i in range(0, len(data)):
        output[i] = data[i]
    return output


##
# @class CanTp
# @brief This is the main class to support CAN transport protocol
#
# Will spawn a CanTpListener class for incoming messages
# depends on a bus object for communication on CAN
class TestTp(object):

    __metaclass__ = iTp

    ##
    # @brief send method
    # raises exception
    def send(self, payload, functionalReq=False):
        raise NotImplemented("Test send should not be used directly, only mocked")

    ##
    # @brief recv method
    # raises exception
    def recv(self, timeout_s):
        raise NotImplemented("Test recv should not be implemented directly, only mocked")
