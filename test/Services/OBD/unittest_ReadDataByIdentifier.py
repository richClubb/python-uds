import unittest
import ReadDataByIdentifier
import UdsMessage

class TestCaseReadDataByIdentifier(unittest.TestCase):

    def testEcuSerialNumber(self):
        expectedOutput = [0x22, 0xF1, 0x8C]
        RDBI = ReadDataByIdentifier.ReadDataByIdentifier()
        b = RDBI.ecuSerialNumber().payload
        self.assertEqual(b, expectedOutput)


if __name__ == "__main__":
    unittest.main()
