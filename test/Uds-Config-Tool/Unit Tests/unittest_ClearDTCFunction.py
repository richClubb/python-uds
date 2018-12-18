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
from uds.uds_config_tool.ISOStandard.ISOStandard import IsoInputOutputControlOptionRecord as IsoOptionRecord
import sys, traceback


class IOControlTestCase(unittest.TestCase):

    # patches are inserted in reverse order
    @mock.patch('uds.TestTp.recv')
    @mock.patch('uds.TestTp.send')
    def test_ioControlRequest_adjust(self,
                     tp_send,
                     tp_recv):

        tp_send.return_value = False	
        tp_recv.return_value = [0x54]

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/EBC-Diagnostics_old.odx', 'bootloader', transportProtocol="TEST")
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __inputOutputControl to inputOutputControl in the uds object, so can now call below

        b = a.clearDTC([0xF1, 0xC8, 0x55])	# ... calls __clearDTC, which does the Uds.send

        tp_send.assert_called_with([0x14, 0xF1, 0xC8, 0x55],False)
        self.assertEqual(None, b)



    # patches are inserted in reverse order
    @mock.patch('uds.TestTp.recv')
    @mock.patch('uds.TestTp.send')
    def test_ecuResetNegResponse_0x13(self,
                     tp_send,
                     tp_recv):

        tp_send.return_value = False
        tp_recv.return_value = [0x7F, 0x13]

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/EBC-Diagnostics_old.odx', 'bootloader', transportProtocol="TEST")
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __inputOutputControl to inputOutputControl in the uds object, so can now call below

        try:
            b = a.clearDTC([0xF1, 0xC8, 0x55])	# ... calls __clearDTC, which does the Uds.send
        except:
            b = traceback.format_exc().split("\n")[-2:-1][0] # ... extract the exception text
        tp_send.assert_called_with([0x14, 0xF1, 0xC8, 0x55],False)
        self.assertEqual("Exception: Detected negative response: ['0x7f', '0x13']", b)


    # patches are inserted in reverse order
    @mock.patch('uds.TestTp.recv')
    @mock.patch('uds.TestTp.send')
    def test_ecuResetNegResponse_0x22(self,
                     tp_send,
                     tp_recv):

        tp_send.return_value = False
        tp_recv.return_value = [0x7F, 0x22]

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/EBC-Diagnostics_old.odx', 'bootloader', transportProtocol="TEST")
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __inputOutputControl to inputOutputControl in the uds object, so can now call below

        try:
            b = a.clearDTC([0xF1, 0xC8, 0x55])	# ... calls __clearDTC, which does the Uds.send
        except:
            b = traceback.format_exc().split("\n")[-2:-1][0] # ... extract the exception text
        tp_send.assert_called_with([0x14, 0xF1, 0xC8, 0x55],False)
        self.assertEqual("Exception: Detected negative response: ['0x7f', '0x22']", b)


    # patches are inserted in reverse order
    @mock.patch('uds.TestTp.recv')
    @mock.patch('uds.TestTp.send')
    def test_ecuResetNegResponse_0x31(self,
                     tp_send,
                     tp_recv):

        tp_send.return_value = False
        tp_recv.return_value = [0x7F, 0x31]

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/EBC-Diagnostics_old.odx', 'bootloader', transportProtocol="TEST")
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __inputOutputControl to inputOutputControl in the uds object, so can now call below

        try:
            b = a.clearDTC([0xF1, 0xC8, 0x55])	# ... calls __clearDTC, which does the Uds.send
        except:
            b = traceback.format_exc().split("\n")[-2:-1][0] # ... extract the exception text
        tp_send.assert_called_with([0x14, 0xF1, 0xC8, 0x55],False)
        self.assertEqual("Exception: Detected negative response: ['0x7f', '0x31']", b)



if __name__ == "__main__":
    unittest.main()