#!/usr/bin/env python

__author__ = "Richard Clubb"
__copyrights__ = "Copyright 2018, the python-uds project"
__credits__ = ["Richard Clubb"]

__license__ = "MIT"
__maintainer__ = "Richard Clubb"
__email__ = "richard.clubb@embeduk.com"
__status__ = "Development"


from TpFactory import TpFactory


##
# @brief a description is needed
class Uds(object):

    ##
    # @brief a constructor
    # @param [in] reqId The request ID used by the UDS connection, defaults to None if not used
    # @param [in] resId The response Id used by the UDS connection, defaults to None if not used
    def __init__(self, reqId=None, resId=None):
        self.__tp = TpFactory.tpFactory("CAN", reqId=reqId, resId=resId)
        self.__reqId = reqId
        self.__resId = resId


    ##
    # @brief
    def send(self, msg, responseRequired = False):

        response = None

        self.__tp.send(msg)

        if(responseRequired):
            response = self.__tp.recv(5000)

        return response


if __name__ == "__main__":
    pass
