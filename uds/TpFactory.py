#!/usr/bin/env python

__author__ = "Richard Clubb"
__copyrights__ = "Copyright 2018, the python-uds project"
__credits__ = ["Richard Clubb"]

__license__ = "MIT"
__maintainer__ = "Richard Clubb"
__email__ = "richard.clubb@embeduk.com"
__status__ = "Development"


from CanTp import CanTp


##
# @brief class for creating Tp objects
class TpFactory(object):

    ##
    # @brief method to create the different connection types
    @staticmethod
    def tpFactory(tpType, **kwargs):
        if(tpType == "CAN"):
            if('reqId' in kwargs):
                reqId = kwargs['reqId']
            else:
                reqId = None

            if('resId' in kwargs):
                resId = kwargs['resId']
            else:
                resId = None
            return CanTp(reqId, resId)
        elif(tpType == "IP"):
            raise NotImplementedError("IP transport not currently supported")
        elif(tpType == "KLINE"):
            raise NotImplementedError("K-Line Transport not currently supported")
        elif(tpType == "LIN"):
            raise NotImplementedError("LIN Transport not currently supported")
        elif(tpType == "FLEXRAY"):
            raise NotImplementedError("FlexRay Transport not currently supported")
        else:
            raise Exception("Unknown transport type selected")

if __name__ == "__main__":

    a = TpFactory.create('CAN')
    print(a)