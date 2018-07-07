import unittest
from CanTpMessage import CanTpMessage, PayloadTooLargeForSfError, CanTpMessageType


class CanTpMessageTestCase(unittest.TestCase):

    def testPayloadNotInitialisedByConstructor(self):
        a = CanTpMessage()
        with self.assertRaises(TypeError):
            _ = a.payload

    def testPayloadSetByConstructor(self):
        testPayload = [1,2,3,4]
        a = CanTpMessage(testPayload)
        self.assertEqual(a.payload, testPayload)

    def testPayloadSetBySetter(self):
        testPayload = [5,4,3,2,1]
        a = CanTpMessage()
        a.payload = testPayload
        self.assertEqual(a.payload, testPayload)

    def testLengthNotInitialisedByConstructor(self):
        a = CanTpMessage()
        with self.assertRaises(TypeError):
            _ = a.length

    def testLengthSetByConstructor(self):
        testPayload = [7,6,5,4,3,2,1]
        testPayloadLength = len(testPayload)
        a = CanTpMessage(testPayload)
        self.assertEqual(a.length, testPayloadLength)

    def testLengthSetBySetter(self):
        testPayload = [10,9,8,7,6,5,4,3,2,1]
        testPayloadLength = len(testPayload)
        a = CanTpMessage()
        a.payload = testPayload
        self.assertEqual(a.length, testPayloadLength)

    def testSf(self):
        testPayload = [6,5,4,3,2,1]
        testResponse = [6, 6, 5, 4, 3, 2, 1, 0]
        a = CanTpMessage(testPayload)
        self.assertEqual(a.sf, testResponse)


    def testSfPayloadTooLarge(self):
        testPayload = [10,9,8,7,6,5,4,3,2,1]
        a = CanTpMessage(testPayload)
        with self.assertRaises(PayloadTooLargeForSfError):
            _ = a.sf

    def testMsgTypeSingleFrame(self):
        testPayload = [7,6,5,4,3,2,1]
        a = CanTpMessage(testPayload)
        self.assertEqual(a.msgType, CanTpMessageType.SINGLE_FRAME)

    def testMsgTypeMultiFrame(self):
        testPayload = [11,10,9,8,7,6,5,4,3,2,1,0]
        a = CanTpMessage(testPayload)
        self.assertEqual(a.msgType, CanTpMessageType.MULTI_FRAME)


if __name__ == "__main__":
    unittest.main()
