#!/usr/bin/env python

__author__ = "Richard Clubb"
__copyrights__ = "Copyright 2018, the python-uds project"
__credits__ = ["Richard Clubb"]

__license__ = "MIT"
__maintainer__ = "Richard Clubb"
__email__ = "richard.clubb@embeduk.com"
__status__ = "Development"


class UdsMessage(object):

    """
        General constructor for the UdsMessage class
    """
    def __init__(self, payload=None):
        self.__length = None  # length can not be manually set
        self.__payload = payload
        pass

    """
        @return an integer, the length of the payload
    """
    @property
    def length(self):
        if(self.__length is None):
            raise TypeError("ServiceId not initialised")
        return self.__length

    """
        @return a list
        @throws TypeError if the payload is not initialised with a value
    """
    @property
    def payload(self):
        if(self.__payload is None):
            raise TypeError("Payload not initialised")
        return self.__payload

    """
        @param val - a list
        @throws TypeError if the val is not a list
    """
    @payload.setter
    def payload(self, val):
        if type(val) == list:
            self.__length = len(val)
            self.__payload = val
        else:
            raise TypeError("Attempt to enter non-list value to payload")


if __name__ == "__main__":
    pass
