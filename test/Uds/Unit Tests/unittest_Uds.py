import unittest
from Uds import Uds
from UdsMessage import UdsMessage
from CanTp import CanTp
from unittest import mock

class UdsTestCase(unittest.TestCase):

    # these are inserted in reverse order to what you'd expect
    @mock.patch('CanTp.CanTp.recv')
    @mock.patch('CanTp.CanTp.send')
    def test_udsSend(self, canTp_send, canTp_recv):

        canTp_send.return_value = False
        canTp_recv.return_value = [0x50, 0x01]

        a = Uds(0x600, 0x650)
        b = UdsMessage([0x10, 0x01])
        a.send(b)
        self.assertEqual([0x50, 0x01], b.response_raw)

    

if __name__ == "__main__":
    unittest.main()
