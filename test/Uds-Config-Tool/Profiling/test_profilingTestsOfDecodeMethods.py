#!/usr/bin/env python

__author__ = "Richard Clubb"
__copyrights__ = "Copyright 2018, the python-uds project"
__credits__ = ["Richard Clubb"]

__license__ = "MIT"
__maintainer__ = "Richard Clubb"
__email__ = "richard.clubb@embeduk.com"
__status__ = "Development"


import cProfile
import sys
from functools import reduce


# ----------------------------------------------------------------
# Profiler Code
# ----------------------------------------------------------------
def do_cprofile(func):
    def profiled_func(*args, **kwargs):
        profile = cProfile.Profile()
        try:
            profile.enable()
            result = func(*args, **kwargs)
            profile.disable()
            return result
        finally:
            profile.print_stats()
    return profiled_func

# ----------------------------------------------------------------
# buildIntFromList Tests
# ----------------------------------------------------------------


@do_cprofile
def buildIntFromListNonRecursiveFunc(aList):
    def buildIntFromList(aList):
        result = 0
        for i in range(0, len(aList)):
            result += (aList[i] << (8 * (len(aList) - (i+1))))
        return result
    return buildIntFromList(aList)


@do_cprofile
def buildIntFromListRecursiveFunc(aList):
    def buildIntFromList(aList):
        if(len(aList) == 1):
            return aList[0]
        else:
            return (aList[0] << (8 * (len(aList) - 1) )) + buildIntFromList(aList[1:])
    return buildIntFromList(aList)


@do_cprofile
def buildIntFromListReduceFunc(aList):
    def buildIntFromList(aList):
        return reduce(lambda x, y: (x << 8) + y, aList)
    return buildIntFromList(aList)


# ----------------------------------------------------------------
# byteListToString Tests
# ----------------------------------------------------------------


@do_cprofile
def byteListToStringNonRecursiveFunc(aList):
    def byteListToString(aList):
        result = ""
        for i in aList:
            result += chr(i)
        return result
    return byteListToString(aList)


@do_cprofile
def byteListToStringRecursiveFunc(aList):
    def byteListToString(aList):
        if(len(aList) == 1):
            return chr(aList[0])
        else:
            return chr(aList[0]) + byteListToString(aList[1:])
    return byteListToString(aList)


@do_cprofile
def byteListToStringReduceFunc(aList):
    def byteListToString(aList):
        return reduce(lambda x, y: x + y, list(map(chr, aList)))
    return byteListToString(aList)


if __name__ == "__main__":

    sys.setrecursionlimit(4000)

    testListA = []
    for i in range(0, 2500):
        testListA.append(0x5a)

    testListB = []
    for i in range(0, 2500):
        testListB.append(0x30)

    print("Testing the buildIntFromList methods")
    resultA = buildIntFromListNonRecursiveFunc(testListA)
    resultB = buildIntFromListRecursiveFunc(testListA)
    resultC = buildIntFromListReduceFunc(testListA)

    assert(resultA == resultB == resultC)

    print("Testing the byteListToString methods")
    resultA = byteListToStringNonRecursiveFunc(testListB)
    resultB = byteListToStringRecursiveFunc(testListB)
    resultC = byteListToStringReduceFunc(testListB)

    assert (resultA == resultB == resultC)
    pass
