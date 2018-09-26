#!/usr/bin/env python

__author__ = "Richard Clubb"
__copyrights__ = "Copyright 2018, the python-uds project"
__credits__ = ["Richard Clubb"]

__license__ = "MIT"
__maintainer__ = "Richard Clubb"
__email__ = "richard.clubb@embeduk.com"
__status__ = "Development"


import unittest
from uds.uds_communications.Uds import Uds
from unittest import mock

mockConfig = {
    'connection': {
        "defaultReqId": 0x600,
        "defaultResId": 0x650,
        "P2_Client": 1,
        "P2_Server": 1
    }
}


class UdsTestCase(unittest.TestCase):

    # these are inserted in reverse order to what you'd expect
    @mock.patch('ConfigSingleton.get_config')
    @mock.patch('CanTp.CanTp.recv')
    @mock.patch('CanTp.CanTp.send')
    def test_udsSendWithResponse(self,
                     get_config_mock,
                     canTp_recv,
                     canTp_send):

        get_config_mock.return_value = mockConfig
        canTp_send.return_value = False
        canTp_recv.return_value = [0x50, 0x01]

        udsConnection = Uds()

        a = udsConnection.send([0x10, 0x01])

        self.assertEqual([0x50, 0x01], a)

    # these are inserted in reverse order to what you'd expect
    @mock.patch('ConfigSingleton.get_config')  # 0
    @mock.patch('CanTp.CanTp.send')  # 2
    def test_udsSendWithoutResponse(self,
                     get_config_mock,
                     canTp_send):

        get_config_mock.return_value = mockConfig
        canTp_send.return_value = False

        udsConnection = Uds()

        a = udsConnection.send([0x10, 0x01], responseRequired=False)

        self.assertEqual(None, None)

    # these are inserted in reverse order to what you'd expect
    @mock.patch('ConfigSingleton.get_config')  # 0
    @mock.patch('CanTp.CanTp.send')  # 2
    def test_udsSendFunctionalRequest(self,
                                    get_config_mock,
                                    canTp_send):
        get_config_mock.return_value = mockConfig
        canTp_send.return_value = False

        udsConnection = Uds()

        a = udsConnection.send([0x10, 0x01], functionalReq=True)

        self.assertEqual(None, None)

if __name__ == "__main__":
    unittest.main()
