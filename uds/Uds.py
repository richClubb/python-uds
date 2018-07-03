#!/usr/bin/env python

__author__ = "Richard Clubb"
__copyrights__ = "Copyright 2018, the python-uds project"
__credits__ = ["Richard Clubb"]

__license__ = "MIT"
__maintainer__ = "Richard Clubb"
__email__ = "richard.clubb@embeduk.com"
__status__ = "Development"

import CanTp
import CanTpListener

##
# @brief a description is needed
class Uds(object):

    ##
    # @brief a constructor
    def __init__(self, logger=None):
        self.__tp = CanTp.CanTp()
        self.__listener = CanTpListener.CanTpListener()
        self.__logger = logger

    ##
    # @brief
    def send(self, message):
        # if message length < 7 then single frame

        # if message length > 7 then multi frame


        return message

