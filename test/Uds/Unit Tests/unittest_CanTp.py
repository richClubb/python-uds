import unittest
import CanTp
import CanTpMessage
from unittest.mock import patch

import can

class CanTpTestCase(unittest.TestCase):

    @patch('can.send')
    def test_canTpSingleFrameSend(self, mock_send):
        tpConnection = CanTp(0x600, 0x650)

        msg = CanTpMessage.CanTpMessage([0x22, 0xf1, 0x8c])

        tpConnection.send(msg)


if __name__ == "__main__":
    unittest.main()
