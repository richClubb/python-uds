#!/usr/bin/env python

__author__ = "Richard Clubb"
__copyrights__ = "Copyright 2018, the python-uds project"
__credits__ = ["Richard Clubb"]

__license__ = "MIT"
__maintainer__ = "Richard Clubb"
__email__ = "richard.clubb@embeduk.com"
__status__ = "Development"


from functools import reduce


def extractBitFromPosition(aInt, position):
    return (aInt & (2**position)) >> position


def extractIntFromPosition(aInt, size, position):
    return (aInt >> position) & ((2**size)-1)


##
# @brief uses the reduce pattern to concatenate the list into a single integer
# tests were performed the assess the benefit of using functional methods
# and the reduce and for loops gave similar times. Using a recursive function
# was almost 10 times slower.
def buildIntFromList(aList):
    return reduce(lambda x, y: (x << 8) + y, aList)


##
# @brief uses list comprehension to deal with the input string
# todo: implement the encoding type
def stringToIntList(aString, encodingType):
    result = []
    [result.append(ord(i)) for i in aString]
    return result


##
# @brief uses the map, reduce pattern to deal with the input list functionally
# todo: implement the encoding type
def intListToString(aList, encodingType):
    return reduce(lambda x, y: x + y, list(map(chr, aList)))


def intArrayToUInt8Array(aArray, inputType):
    return intArrayToIntArray(aArray, inputType, 'int8')


def intArrayToIntArray(aArray, inputType, outputType):
    if type(aArray) != list:
        aArray = [aArray]
    if (inputType == 'uint32'):
        inputFunc = lambda x: [extractIntFromPosition(x, 8, 24), extractIntFromPosition(x, 8, 16),
                          extractIntFromPosition(x, 8, 8), extractIntFromPosition(x, 8, 0)]
    elif (inputType == 'uint16'):
        inputFunc = lambda x: [extractIntFromPosition(x, 8, 8), extractIntFromPosition(x, 8, 0)]
    elif (inputType == 'uint8'):
        inputFunc = lambda x: [x]
    elif (inputType == 'int32'):
        inputFunc = lambda x: [extractIntFromPosition(x, 8, 24), extractIntFromPosition(x, 8, 16),
                          extractIntFromPosition(x, 8, 8), extractIntFromPosition(x, 8, 0)]
    elif (inputType == 'int16'):
        inputFunc = lambda x: [extractIntFromPosition(x, 8, 8), extractIntFromPosition(x, 8, 0)]
    elif (inputType == 'int8'):
        inputFunc = lambda x: [x]
    else:
        raise TypeError('inputType not currently supported')

    result = reduce(lambda x, y: x + y, list(map(inputFunc, aArray)))

    if(outputType == 'int8'):
        return result
    if(outputType == 'int32'):
        size = 4
        numberOfEntries = int(len(result) / size)
    elif(outputType == 'int16'):
        size = 2
        numberOfEntries = int(len(result) / size)

    output = list(map(buildIntFromList, [result[(i * size):(i * size + size)] for i in range(numberOfEntries)]))
    return output


if __name__ == "__main__":
    a = intArrayToIntArray([0x5AA55AA5, 0xA55AA55A], 'int32', 'int32')
    print(a)
    assert([0x5aa55aa5, 0xa55aa55a] == a)
    a = intArrayToIntArray([0x5AA55AA5, 0xA55AA55A], 'int32', 'int16')
    print(a)
    assert ([0x5aa5, 0x5aa5, 0xa55a, 0xa55a] == a)
    a = intArrayToIntArray([0x5AA55AA5, 0xA55AA55A], 'int32', 'int8')
    print(a)
    assert ([0x5a, 0xa5, 0x5a, 0xa5, 0xa5, 0x5a, 0xa5, 0x5a] == a)
    a = intArrayToIntArray([0x5AA5, 0xA55A], 'int16', 'int16')
    print(a)
    assert ([0x5aa5, 0xA55A] == a)
    a = intArrayToIntArray([0x5AA5, 0xA55A], 'int16', 'int32')
    print(a)
    assert ([0x5aa5A55A] == a)
    a = intArrayToIntArray([0x5AA5, 0xA55A], 'int16', 'int8')
    print(a)
    assert ([0x5a, 0xa5, 0xa5, 0x5a] == a)
    a = intArrayToIntArray([0x5A, 0xA5, 0xA5, 0x5A], 'int8', 'int8')
    print(a)
    assert ([0x5a, 0xa5, 0xa5, 0x5a] == a)
    a = intArrayToIntArray([0x5A, 0xA5, 0xA5, 0x5A], 'int8', 'int16')
    print(a)
    assert ([0x5aa5, 0xa55a] == a)
    a = intArrayToIntArray([0x5A, 0xA5, 0xA5, 0x5A], 'int8', 'int32')
    print(a)
    assert ([0x5aa5a55a] == a)
    a = intArrayToIntArray([0x5A, 0xA5, 0xA5, 0x5A, 0xA5, 0x5A, 0xA5, 0x5A], 'int8', 'int32')
    print(a)
    assert ([0x5aa5a55a, 0xa55aa55a] == a)

    a = intArrayToIntArray([0x01], 'int8', 'int8')
    print(a)

    a = intArrayToUInt8Array([0x01], 'int8')
    print(a)
