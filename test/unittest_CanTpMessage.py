import unittest
from CanTpMessage import CanTpMessage


class CanTpMessageTestCase(unittest.TestCase):

    def testPayloadNotInitialisedByConstructor(self):
        a = CanTpMessage()
        with self.assertRaises(NotImplementedError):
            _ = a.payload

    def testPayloadInitialisedByConstructor(self):
        testPayload = [1,2,3,4]
        a = CanTpMessage(testPayload)
        self.assertEqual(a.payload, testPayload)

    def testPayloadSetBySetter(self):
        testPayload = [1, 2, 3, 4]
        a = CanTpMessage()
        a.payload = testPayload
        self.assertEqual(a.payload, testPayload)

    def testGetNextSegmentSingleFrame(self):
        testPayload = [1, 2, 3, 4]
        expectedOutput = [4, 1, 2, 3, 4, 0, 0, 0]
        a = CanTpMessage(testPayload)
        self.assertEqual(a.get_next_frame(), expectedOutput)

    # def testGetNextSegmentFirstFrame(self):
    #     testPayload = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    #     expectedOutput = [0x10, 10, 1, 2, 3, 4, 5, 6]
    #     a = CanTpMessage(testPayload)
    #     self.assertEqual(a.get_next_frame(), expectedOutput)

if __name__ == "__main__":
    unittest.main()
