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
from uds.uds_config_tool.UdsConfigTool import createUdsConnection
import sys, traceback


class WDBITestCase(unittest.TestCase):

    # patches are inserted in reverse order
    @mock.patch('uds.TestTp.recv')
    @mock.patch('uds.TestTp.send')
    def test_securityAccessKeyRequest(self,
                     tp_send,
                     tp_recv):

        tp_send.return_value = False
        tp_recv.return_value = [0x67, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/Bootloader.odx', 'bootloader', transportProtocol="TEST")

        b = a.securityAccess('Programming Request')

        tp_send.assert_called_with([0x27, 0x01], False)
        self.assertEqual([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                          0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
                         b)  # ... wdbi should not return a value

    @mock.patch('uds.TestTp.recv')
    @mock.patch('uds.TestTp.send')
    def test_securityAccessNegativeResponse(self,
                              tp_send,
                              tp_recv):
        tp_send.return_value = False
        tp_recv.return_value = [0x7F, 0x00, 0x00]

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/Bootloader.odx',
                                'bootloader',
                                transportProtocol="TEST")

        with self.assertRaises(Exception) as context:
            b = a.securityAccess('Programming Request')

        self.assertTrue("Found negative response" in str(context.exception))

    # patches are inserted in reverse order
    @mock.patch('uds.TestTp.recv')
    @mock.patch('uds.TestTp.send')
    def test_securityAccessKeyRequest(self,
                     tp_send,
                     tp_recv):

        tp_send.return_value = False
        tp_recv.return_value = [0x67, 0x02]

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/Bootloader.odx',
                                'bootloader',
                                transportProtocol="TEST")

        b = a.securityAccess('Programming Key',
                             [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                              0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

        tp_send.assert_called_with([0x27, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                                    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                                    0x00, 0x00],
                                   False)
        self.assertEqual(None,
                         b)  # ... wdbi should not return a value



if __name__ == "__main__":
    unittest.main()
