import unittest
from CanTpMessage import CanTpMessage


class CanTpMessageTestCase(unittest.TestCase):

    def testPayloadNotInitialisedByConstructor(self):
        a = CanTpMessage()
        with self.assertRaises(Exception):
            _ = a.payload

    def testBlockPayload_smallPayload(self):
        payload = []
        for i in range(0, 20):
            payload.append(i)
        a = CanTpMessage(payload)


if __name__ == "__main__":
    unittest.main()
