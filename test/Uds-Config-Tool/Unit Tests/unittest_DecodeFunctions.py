#!/usr/bin/env python

__author__ = "Richard Clubb"
__copyrights__ = "Copyright 2018, the python-uds project"
__credits__ = ["Richard Clubb"]

__license__ = "MIT"
__maintainer__ = "Richard Clubb"
__email__ = "richard.clubb@embeduk.com"
__status__ = "Development"


from uds.uds_config_tool import DecodeFunctions
import unittest


class CanTpMessageTestCase(unittest.TestCase):

    def testBitExtractFromBytePos0True(self):
        testVal = 0x01
        result = DecodeFunctions.extractBitFromPosition(testVal, 0)
        self.assertEqual(True, result)

    def testBitExtractFromBytePos0False(self):
        testVal = 0x00
        result = DecodeFunctions.extractBitFromPosition(testVal, 0)
        self.assertEqual(False, result)

    def testBitExtractFromBytePos1True(self):
        testVal = 0x02
        result = DecodeFunctions.extractBitFromPosition(testVal, 1)
        self.assertEqual(True, result)

    def testBitExtractFromBytePos1False(self):
        testVal = 0x00
        result = DecodeFunctions.extractBitFromPosition(testVal, 1)
        self.assertEqual(False, result)

    def testMultipleBitExtractFromByte(self):
        testVal = 0x5A
        result = DecodeFunctions.extractBitFromPosition(testVal, 0)
        self.assertEqual(False, result)
        result = DecodeFunctions.extractBitFromPosition(testVal, 1)
        self.assertEqual( True, result)
        result = DecodeFunctions.extractBitFromPosition(testVal, 2)
        self.assertEqual(False, result)
        result = DecodeFunctions.extractBitFromPosition(testVal, 3)
        self.assertEqual( True, result)
        result = DecodeFunctions.extractBitFromPosition(testVal, 4)
        self.assertEqual( True, result)
        result = DecodeFunctions.extractBitFromPosition(testVal, 5)
        self.assertEqual(False, result)
        result = DecodeFunctions.extractBitFromPosition(testVal, 6)
        self.assertEqual( True, result)
        result = DecodeFunctions.extractBitFromPosition(testVal, 7)
        self.assertEqual(False, result)

    def testBitExtractFromWordPos8True(self):
        testVal = 0x100
        result = DecodeFunctions.extractBitFromPosition(testVal, 8)
        self.assertEqual(True, result)

    def testBitExtractFromWordPos8False(self):
        testVal = 0x000
        result = DecodeFunctions.extractBitFromPosition(testVal, 8)
        self.assertEqual(False, result)

    def test4BitIntExtractFromPos0Of8BitInt(self):
        testVal = 0xA5
        result = DecodeFunctions.extractIntFromPosition(testVal, 4, 0)
        self.assertEqual(0x05, result)

    def test4BitIntExtractFromPos1Of8BitInt(self):
        testVal = 0xA5
        result = DecodeFunctions.extractIntFromPosition(testVal, 4, 1)
        self.assertEqual(0x2, result)

    def test4BitIntExtractFromPos2Of8BitInt(self):
        testVal = 0xA5
        result = DecodeFunctions.extractIntFromPosition(testVal, 4, 2)
        self.assertEqual(0x9, result)

    def test6BitIntExtractFromPos2Of8BitInt(self):
        testVal = 0xA5
        result = DecodeFunctions.extractIntFromPosition(testVal, 6, 2)
        self.assertEqual(0x29, result)

    def testBuildIntFromArray1ByteArray(self):
        testVal = [0x5A]
        result = DecodeFunctions.buildIntFromList(testVal)
        self.assertEqual(0x5A, result)

    def testBuildIntFromArray2ByteArray(self):
        testVal = [0x5A, 0xA5]
        result = DecodeFunctions.buildIntFromList(testVal)
        self.assertEqual(0x5AA5, result)

    def testBuildIntFromArray3ByteArray(self):
        testVal = [0x5A, 0xA5, 0x5A]
        result = DecodeFunctions.buildIntFromList(testVal)
        self.assertEqual(0x5AA55A, result)

    def testBuildIntFromArray4ByteArray(self):
        testVal = [0x5A, 0xA5, 0xA5, 0x5A]
        result = DecodeFunctions.buildIntFromList(testVal)
        self.assertEqual(0x5AA5A55A, result)

    def testBuildIntFromArray8ByteArray(self):
        testVal = [0x5A, 0xa5, 0xA5, 0x5A, 0x5A, 0xA5, 0xA5, 0x5A]
        result = DecodeFunctions.buildIntFromList(testVal)
        self.assertEqual(0x5AA5A55A5AA5A55A, result)

    def testStringToByteArrayAlphaOnlyAscii(self):
        testVal = 'abcdefghijklmn'
        result = DecodeFunctions.stringToIntList(testVal, 'ascii')
        self.assertEqual([0x61, 0x62, 0x63, 0x64, 0x65, 0x66, 0x67, 0x68, 0x69, 0x6A, 0x6B, 0x6C, 0x6D, 0x6E], result)

    def testStringToByteArrayNumericOnlyAscii(self):
        testVal = 'abcdefg01234'
        result = DecodeFunctions.stringToIntList(testVal, 'ascii')
        self.assertEqual([0x61, 0x62, 0x63, 0x64, 0x65, 0x66, 0x67, 0x30, 0x31, 0x32, 0x33, 0x34], result)

    def testStringToByteArrayAlphaOnlyUtf8(self):
        testVal = 'abcdefg'
        result = DecodeFunctions.stringToIntList(testVal, 'utf-8')
        self.assertEqual([0x61, 0x62, 0x63, 0x64, 0x65, 0x66, 0x67], result)

    def testByteArrayToStringAlphaOnlyAscii(self):
        testVal = [0x61, 0x62, 0x63, 0x64, 0x65, 0x66, 0x67, 0x68, 0x69, 0x6A, 0x6B, 0x6C, 0x6D, 0x6E]
        result = DecodeFunctions.intListToString(testVal, 'ascii')
        self.assertEqual('abcdefghijklmn', result)

    def testUint16ArrayToUint8Array(self):
        testVal = [0x5AA5, 0xA55A]
        result = DecodeFunctions.intArrayToUInt8Array(testVal, 'int16')
        self.assertEqual([0x5a, 0xA5, 0xA5, 0x5A], result)

    def testUint8ArraytoUint16Array(self):
        testVal = [0x5aa55aa5, 0xa55aa55a]
        result = DecodeFunctions.intArrayToUInt8Array(testVal, 'int32')
        self.assertEqual([0x5a, 0xa5, 0x5a, 0xa5, 0xA5, 0x5A, 0xa5, 0x5a], result)

if __name__ == "__main__":
    unittest.main()