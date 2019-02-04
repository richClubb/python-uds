#!/usr/bin/env python

__author__ = "Richard Clubb"
__copyrights__ = "Copyright 2018, the python-uds project"
__credits__ = ["Richard Clubb"]

__license__ = "MIT"
__maintainer__ = "Richard Clubb"
__email__ = "richard.clubb@embeduk.com"
__status__ = "Development"


##
# @brief pads out an array with a fill value
def fillArray(data, length, fillValue=0):
    output = []
    for i in range(0, length):
        output.append(fillValue)
    for i in range(0, len(data)):
        output[i] = data[i]
    return output
