#!/usr/bin/env python

__author__ = "Richard Clubb"
__copyrights__ = "Copyright 2018, the python-uds project"
__credits__ = ["Richard Clubb"]

__license__ = "MIT"
__maintainer__ = "Richard Clubb"
__email__ = "richard.clubb@embeduk.com"
__status__ = "Development"


import unittest
from Uds import Uds
from unittest import mock


class UdsTestCase(unittest.TestCase):

    # these are inserted in reverse order to what you'd expect
    @mock.patch('CanTp.CanTp.recv')
    @mock.patch('CanTp.CanTp.send')
    def test_udsSendWithResponse(self,
                     canTp_recv,
                     canTp_send):

        canTp_send.return_value = False
        canTp_recv.return_value = [0x50, 0x01]

        udsConnection = Uds()

        a = udsConnection.send([0x10, 0x01])

        self.assertEqual([0x50, 0x01], a)


if __name__ == "__main__":
    unittest.main()
