#!/usr/bin/env python

__author__ = "Richard Clubb"
__copyrights__ = "Copyright 2018, the python-uds project"
__credits__ = ["Richard Clubb"]

__license__ = "MIT"
__maintainer__ = "Richard Clubb"
__email__ = "richard.clubb@embeduk.com"
__status__ = "Development"


import unittest
from uds import Uds
from unittest import mock


class UdsTestCase(unittest.TestCase):

    # these are inserted in reverse order to what you'd expect
    @mock.patch('uds.TestTp.send')
    @mock.patch('uds.TestTp.recv')
    def test_udsSendWithResponse(self,
                     tp_recv,
                     tp_send):

        tp_send.return_value = False
        tp_recv.return_value = [0x50, 0x01]

        udsConnection = Uds()

        a = udsConnection.send([0x10, 0x01])

        self.assertEqual([0x50, 0x01], a)


if __name__ == "__main__":
    unittest.main()
