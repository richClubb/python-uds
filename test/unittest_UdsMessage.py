import unittest
from UdsMessage import UdsMessage


class UdsMessageTestCase(unittest.TestCase):

    """
        Unit test for the payload not initialised
        Negative test case, expected to produce an exception
    """
    def testMessagePayloadNotInit(self):
        a = UdsMessage()
        with self.assertRaises(TypeError):
            _ = a.payload

    """
        Test of the payload with a simple list entry
        Positive test case, expected to produce a correct result
    """
    def testMessagePayloadSimple(self):
        testVal = [1]
        a = UdsMessage()
        a.payload = testVal
        self.assertEqual(a.payload, testVal)

    """
        Test of the service id not initialised
        Negative test acse, expected to produce an exception
    """
    def testLengthNotInit(self):
        a = UdsMessage()
        with self.assertRaises(TypeError):
            _ = a.length

    """
        Test of the serviceId with a simple int
    """
    def testMessageServiceIdSimple(self):
        testVal = [0x01, 0x02, 0x03]
        testVal_length = len(testVal)
        a = UdsMessage()
        a.payload = testVal
        self.assertEqual(a.length, testVal_length)

    def testMessageDecodeNotImplemented(self):
        a = UdsMessage()
        with self.assertRaises(NotImplementedError):
            _ = a.decode


if __name__ == "__main__":
    unittest.main()
