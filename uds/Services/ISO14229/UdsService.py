#!/usr/bin/env python

__author__ = "Richard Clubb"
__copyrights__ = "Copyright 2018, the python-uds project"
__credits__ = ["Richard Clubb"]

__license__ = "MIT"
__maintainer__ = "Richard Clubb"
__email__ = "richard.clubb@embeduk.com"
__status__ = "Development"


from Uds import Uds
from abc import ABC, abstractmethod


##
#
class UdsService(Uds, ABC):

    ##
    # @brief
    def __init__(self):
        self.__serviceId = None
        self.__positiveResponse = None
        self.__negativeResponseList = None

    @abstractmethod
    def send(self, msg):
        raise NotImplementedError("Function not implemented")
