#!/usr/bin/env python

__author__ = "Richard Clubb"
__copyrights__ = "Copyright 2018, the python-uds project"
__credits__ = ["Richard Clubb"]

__license__ = "MIT"
__maintainer__ = "Richard Clubb"
__email__ = "richard.clubb@embeduk.com"
__status__ = "Development"

# import CanTpMessage
import can

##
# @class CanTp
# @brief This is the main class to support CAN transport protocol
#
# Will spawn a CanTpListener class for incoming messages
# depends on a bus object for communication on CAN
class CanTp(object):

    ##
    # @brief constructor for the CanTp object
    def __init__(self, logger=None):
        self.__bus = None
        self.__logger = logger
        pass

    ##
    # @brief connection method
    def createBusConnection(self):
        self.__bus = can.interface.Bus('test', bustype='virtual')

    ##
    # @brief send method
    def send(self, payload):
        pass

    ##
    # @brief recv method
    def recv(self):
        return None


if __name__ == "__main__":
    pass
