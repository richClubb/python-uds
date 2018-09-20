#!/usr/bin/env python

__author__ = "Richard Clubb"
__copyrights__ = "Copyright 2018, the python-uds project"
__credits__ = ["Richard Clubb"]

__license__ = "MIT"
__maintainer__ = "Richard Clubb"
__email__ = "richard.clubb@embeduk.com"
__status__ = "Development"


from uds_communications.TransportProtocols.TpFactory import TpFactory
from uds_configuration.ConfigSingleton import get_config

##
# @brief a description is needed
class Uds(object):

    ##
    # @brief a constructor
    # @param [in] reqId The request ID used by the UDS connection, defaults to None if not used
    # @param [in] resId The response Id used by the UDS connection, defaults to None if not used
    def __init__(self, reqId=None, resId=None):

        self.__config = get_config()

        self.__reqId = reqId
        self.__resId = resId

        if reqId is None:
            self.__reqId = int(self.__config['connection']['defaultReqId'], 16)

        if resId is None:
            self.__resId = int(self.__config['connection']['defaultResId'], 16)

        if (
                (self.__reqId is None) |
                (self.__resId is None)
            ):
            raise Exception("No IDs")

        # currently the TP Factory only supports can
        self.__tp = TpFactory.tpFactory("CAN", reqId=self.__reqId, resId=self.__resId)

        self.__P2_CAN_Client = int(self.__config['connection']['P2_Client'])
        self.__P2_CAN_Server = int(self.__config['connection']['P2_Server'])

        # used as a semaphore for the tester present
        self.__transmissionActive_flag = False

    ##
    # @brief
    def send(self, msg, responseRequired=True, functionalReq=False):

        # sets a current transmission in progress
        self.__transmissionActive_flag = True

        response = None

        self.__tp.send(msg, functionalReq)

        if functionalReq is True:
            responseRequired = False

        if responseRequired:
            response = self.__tp.recv(self.__P2_CAN_Client)

        # lets go of the hold on transmissions
        self.__transmissionActive_flag = False

        return response


if __name__ == "__main__":
    pass
