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
        tp_recv.return_value = [0x6F, 0xFE, 0x16, 0x03, 0x00, 0x00, 0x1F, 0x40]

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/EBC-Diagnostics_old.odx', 'bootloader', transportProtocol="TEST")
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __inputOutputControl to inputOutputControl in the uds object, so can now call below

        b = a.inputOutputControl('Booster Target Speed',IsoOptionRecord.adjust,[8000])	# ... calls __inputOutputControl, which does the Uds.send

        tp_send.assert_called_with([0x2F, 0xFE, 0x16, 0x03, 0x00, 0x00, 0x1F, 0x40],False)
        self.assertEqual({'Identifier':[0xFE, 0x16],'ControlOptionRecord':[IsoOptionRecord.adjust],'TargetSpeed':[0x00, 0x00, 0x1F, 0x40]}, b)


    # patches are inserted in reverse order
    @mock.patch('uds.TestTp.recv')
    @mock.patch('uds.TestTp.send')
    def test_ioControlRequest_returnControl(self,
                     tp_send,
                     tp_recv):

        tp_send.return_value = False	
        tp_recv.return_value = [0x6F, 0xFE, 0x16, 0x00, 0x00, 0x00, 0x1F, 0x40]

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/EBC-Diagnostics_old.odx', 'bootloader', transportProtocol="TEST")
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __inputOutputControl to inputOutputControl in the uds object, so can now call below

        b = a.inputOutputControl('Booster Target Speed',IsoOptionRecord.returnControl,None)	# ... calls __inputOutputControl, which does the Uds.send

        tp_send.assert_called_with([0x2F, 0xFE, 0x16, 0x00],False)
        self.assertEqual({'Identifier':[0xFE, 0x16],'ControlOptionRecord':[IsoOptionRecord.returnControl],'TargetSpeed':[0x00, 0x00, 0x1F, 0x40]}, b)
		

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
            b = a.inputOutputControl('Booster Target Speed',IsoOptionRecord.adjust,[8000])	# ... calls __inputOutputControl, which does the Uds.send
        except:
            b = traceback.format_exc().split("\n")[-2:-1][0] # ... extract the exception text
        tp_send.assert_called_with([0x2F, 0xFE, 0x16, 0x03, 0x00, 0x00, 0x1F, 0x40],False)
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
            b = a.inputOutputControl('Booster Target Speed',IsoOptionRecord.adjust,[8000])	# ... calls __inputOutputControl, which does the Uds.send
        except:
            b = traceback.format_exc().split("\n")[-2:-1][0] # ... extract the exception text
        tp_send.assert_called_with([0x2F, 0xFE, 0x16, 0x03, 0x00, 0x00, 0x1F, 0x40],False)
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
            b = a.inputOutputControl('Booster Target Speed',IsoOptionRecord.adjust,[8000])	# ... calls __inputOutputControl, which does the Uds.send
        except:
            b = traceback.format_exc().split("\n")[-2:-1][0] # ... extract the exception text
        tp_send.assert_called_with([0x2F, 0xFE, 0x16, 0x03, 0x00, 0x00, 0x1F, 0x40],False)
        self.assertEqual("Exception: Detected negative response: ['0x7f', '0x31']", b)



    # patches are inserted in reverse order
    @mock.patch('uds.TestTp.recv')
    @mock.patch('uds.TestTp.send')
    def test_ecuResetNegResponse_0x33(self,
                     tp_send,
                     tp_recv):

        tp_send.return_value = False
        tp_recv.return_value = [0x7F, 0x33]

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/EBC-Diagnostics_old.odx', 'bootloader', transportProtocol="TEST")
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __inputOutputControl to inputOutputControl in the uds object, so can now call below

        try:
            b = a.inputOutputControl('Booster Target Speed',IsoOptionRecord.adjust,[8000])	# ... calls __inputOutputControl, which does the Uds.send
        except:
            b = traceback.format_exc().split("\n")[-2:-1][0] # ... extract the exception text
        tp_send.assert_called_with([0x2F, 0xFE, 0x16, 0x03, 0x00, 0x00, 0x1F, 0x40],False)
        self.assertEqual("Exception: Detected negative response: ['0x7f', '0x33']", b)

	



if __name__ == "__main__":
    unittest.main()