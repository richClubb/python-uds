import unittest
from BusFactory import BusFactory
import can


class BusFactoryTestCase(unittest.TestCase):

    def testIfNotPresent(self):
        with self.assertRaises(NotImplementedError):
            _ = BusFactory.createBus(hwIf='Test')

    def testPcan(self):
        a = BusFactory.createBus(hwIf='PEAK_CAN_USB')
        self.assertEqual(isinstance(a), can.interfaces.pcan.PcanBus)

if __name__ == "__main__":
    unittest.main()
