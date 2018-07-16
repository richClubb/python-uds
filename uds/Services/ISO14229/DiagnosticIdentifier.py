#!/usr/bin/env python

__author__ = "Richard Clubb"
__copyrights__ = "Copyright 2018, the python-uds project"
__credits__ = ["Richard Clubb"]

__license__ = "MIT"
__maintainer__ = "Richard Clubb"
__email__ = "richard.clubb@embeduk.com"
__status__ = "Development"


## @package test
#

##
#
class DiagnosticIdentifier(object):

    ##
    # @brief the constructor for the diagnostic identifier class
    def __init__(self):
        pass

    ##
    # @param encodes a value to a raw payload
    def encode(self, val):
        raise NotImplementedError("Encode function not implemented")

    ##
    # @return a physical value and the units as two params
    def decode(self):
        raise NotImplementedError("Decode function not implemented")
