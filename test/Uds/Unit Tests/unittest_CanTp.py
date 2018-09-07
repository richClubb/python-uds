#!/usr/bin/env python

__author__ = "Richard Clubb"
__copyrights__ = "Copyright 2018, the python-uds project"
__credits__ = ["Richard Clubb"]

__license__ = "MIT"
__maintainer__ = "Richard Clubb"
__email__ = "richard.clubb@embeduk.com"
__status__ = "Development"


import unittest
import CanTp
from unittest.mock import patch


class CanTpTestCase(unittest.TestCase):

    def test_canTpRaiseExceptionOnTooLargePayload(self):
        payload = []
        for i in range(0, 4096):
            payload.append(0)

        tpConnection = CanTp.CanTp(0x600, 0x650)
        with self.assertRaises(Exception):
            tpConnection.send(payload)

    @patch('can.interfaces.virtual.VirtualBus.send')
    def test_canTpSendSingleFrame(self, sendMock):

        result = []

        def msgData(msg):
            nonlocal result
            result = msg.data

        sendMock.side_effect = msgData

        tpConnection = CanTp.CanTp(0x600, 0x650)

        payload = [0x01, 0x02, 0x03]
        tpConnection.send(payload)

        self.assertEqual(result, [0x03, 0x01, 0x02, 0x03, 0x00, 0x00, 0x00, 0x00])

    @patch('can.interfaces.virtual.VirtualBus.send')
    @patch('CanTp.CanTp.getNextBufferedMessage')
    def test_smallMultiFrameSend(self, getNextMessageMock, canSendMock):

        result = []
        count = 1

        fcSent = False

        def msgData(msg):

            nonlocal getNextMessageMock
            nonlocal result

            getNextMessageMock.side_effect = getNextMessageFunc
            result += msg.data

        def getNextMessageFunc():

            nonlocal fcSent

            if fcSent is True:
                return None

            if fcSent is False:
                fcSent = True
                return [0x30, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00]


        getNextMessageMock.return_value = None
        canSendMock.side_effect = msgData

        tpConnection = CanTp.CanTp(0x600, 0x650)

        tpConnection.send([0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08])

        self.assertEqual([0x10, 0x08, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x20, 0x07, 0x08, 0x00, 0x00, 0x00, 0x00,
                          0x00],
                         result)

    @patch('can.interfaces.virtual.VirtualBus.send')
    @patch('CanTp.CanTp.getNextBufferedMessage')
    def test_largerMultiFrameSend(self, getNextMessageMock, canSendMock):

        result = []
        count = 1

        fcSent = False

        def msgData(msg):

            nonlocal getNextMessageMock
            nonlocal result

            getNextMessageMock.side_effect = getNextMessageFunc
            result += msg.data

        def getNextMessageFunc():

            nonlocal fcSent

            if fcSent is True:
                return None

            if fcSent is False:
                fcSent = True
                return [0x30, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00]


        getNextMessageMock.return_value = None
        canSendMock.side_effect = msgData

        tpConnection = CanTp.CanTp(0x600, 0x650)

        payload = []
        for i in range(1, 41):
            payload.append(i)

        tpConnection.send(payload)

        print(result)

        self.assertEqual([0x10, 0x28, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06,
                          0x20, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D,
                          0x21, 0x0E, 0x0F, 0x10, 0x11, 0x12, 0x13, 0x14,
                          0x22, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1A, 0x1B,
                          0x23, 0x1C, 0x1D, 0x1E, 0x1F, 0x20, 0x21, 0x22,
                          0x24, 0x23, 0x24, 0x25, 0x26, 0x27, 0x28, 0x00],
                         result)

    def test_canTpCreateBlock_oneBlockSinglePduNotFull(self):

        testVal = []
        for i in range(0, 6):
            testVal.append(0xFF)

        tpConnection = CanTp.CanTp(0x600, 0x650)

        a = tpConnection.create_blockList(testVal, 1)

        # print(a)

        self.assertEqual(a, [[[0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x00]]])

    def test_canTpCreateBlock_oneBlockSinglePduFullSameAsBlockSize(self):

        testVal = []
        for i in range(0, 7):
            testVal.append(0xFF)

        tpConnection = CanTp.CanTp(0x600, 0x650)

        a = tpConnection.create_blockList(testVal, 1)

        # print(a)

        self.assertEqual(a, [[[0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]]])

    def test_canTpCreateBlock_oneBlockSinglePduFullSmallerThanBlockSize(self):

        testVal = []
        for i in range(0, 7):
            testVal.append(0xFF)

        tpConnection = CanTp.CanTp(0x600, 0x650)

        a = tpConnection.create_blockList(testVal, 2)

        # print(a)

        self.assertEqual(a, [[[0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]]])

    def test_canTpCreateBlock_oneBlockTwoPduNotFull(self):
        testVal = []
        for i in range(0, 13):
            testVal.append(0xFF)

        tpConnection = CanTp.CanTp(0x600, 0x650)

        a = tpConnection.create_blockList(testVal, 2)

        # print(a)

        self.assertEqual(a, [[[0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF],[0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x00]]])

    def test_canTpCreateBlock_oneBlockTwoPduFull(self):
        testVal = []
        for i in range(0, 14):
            testVal.append(0xFF)

        tpConnection = CanTp.CanTp(0x600, 0x650)

        a = tpConnection.create_blockList(testVal, 2)

        # print(a)

        self.assertEqual(a, [[[0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF],[0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]]])

    def test_canTpCreateBlock_twoBlockTwoPduNotFull(self):
        testVal = []
        for i in range(0, 27):
            testVal.append(0xFF)

        tpConnection = CanTp.CanTp(0x600, 0x650)

        a = tpConnection.create_blockList(testVal, 2)

        # print(a)

        self.assertEqual(a,
                         [
                            [[0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]],
                            [[0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x00]]
        ])

    def test_canTpCreateBlock_twoBlockTwoPduFull(self):
        testVal = []
        for i in range(0, 28):
            testVal.append(0xFF)

        tpConnection = CanTp.CanTp(0x600, 0x650)

        a = tpConnection.create_blockList(testVal, 2)

        # print(a)

        self.assertEqual(a,
                         [
                            [[0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]],
                            [[0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]]
        ])

    def test_canTpCreateBlock_noBlockSizePdu(self):
        testVal = []
        for i in range(0, 4089):
            testVal.append(0xFF)

        result = []
        for i in range(584):
            result.append([0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])

        result.append([0xFF, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

        tpConnection = CanTp.CanTp(0x600, 0x650)

        a = tpConnection.create_blockList(testVal, 585)

        # print(a)

        self.assertEqual(a[0],
                         result)


if __name__ == "__main__":
    unittest.main()
