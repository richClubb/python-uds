#!/usr/bin/env python

__author__ = "Richard Clubb"
__copyrights__ = "Copyright 2018, the python-uds project"
__credits__ = ["Richard Clubb"]

__license__ = "MIT"
__maintainer__ = "Richard Clubb"
__email__ = "richard.clubb@embeduk.com"
__status__ = "Development"


import unittest
from unittest import mock

from uds import Uds


class UdsTestCase(unittest.TestCase):

    # these are inserted in reverse order to what you'd expect
    @mock.patch('uds.TestTp.recv')
    @mock.patch('uds.TestTp.send')
    def test_udsSendWithResponse(self,
                                 testTp_send,
                                 testTp_recv):

        testTp_send.return_value = False
        testTp_recv.return_value = [0x50, 0x01]

        udsConnection = Uds(transportProtocol="TEST")

        a = udsConnection.send([0x10, 0x01])

        self.assertEqual([0x50, 0x01], a)

    # these are inserted in reverse order to what you'd expect
    @mock.patch('uds.TestTp.send')  # 2
    def test_udsSendWithoutResponse(self,
                                    testTp_send):

        testTp_send.return_value = False

        udsConnection = Uds(transportProtocol="TEST")

        a = udsConnection.send([0x10, 0x01], responseRequired=False)

        self.assertEqual(None, None)

    # these are inserted in reverse order to what you'd expect
    @mock.patch('uds.TestTp.send')  # 2
    def test_udsSendFunctionalRequest(self,
                                      testTp_send):
        testTp_send.return_value = False

        udsConnection = Uds(transportProtocol="TEST")

        a = udsConnection.send([0x10, 0x01], functionalReq=True)

        self.assertEqual(None, None)

if __name__ == "__main__":
    unittest.main()
