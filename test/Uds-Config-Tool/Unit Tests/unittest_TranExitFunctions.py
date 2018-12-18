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


class TransferExitTestCase(unittest.TestCase):

    # patches are inserted in reverse order
    @mock.patch('uds.CanTp.recv')
    @mock.patch('uds.CanTp.send')
    def test_transExitRequest(self,
                     canTp_send,
                     canTp_recv):

        canTp_send.return_value = False
        canTp_recv.return_value = [0x77, 0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF]

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/Bootloader.odx', 'bootloader')
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __transferExit to transferExit in the uds object, so can now call below

        b = a.transferExit([0xF1,0xF2,0xF3,0xF4,0xF5,0xF6,0xF7,0xF8,0xF9,0xFA,0xFB,0xFC,0xFD,0xFE,0xFF])	# ... calls __transferExit, which does the Uds.send - takes blockSequenceCounter and parameterRecord
        canTp_send.assert_called_with([0x37, 0xF1,0xF2,0xF3,0xF4,0xF5,0xF6,0xF7,0xF8,0xF9,0xFA,0xFB,0xFC,0xFD,0xFE,0xFF],False)
        self.assertEqual({'transferResponseParameterRecord':[0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF]}, b)  # ... (returns a dict)


    # patches are inserted in reverse order
    @mock.patch('uds.CanTp.recv')
    @mock.patch('uds.CanTp.send')
    def test_transExitNegResponse_0x13(self,
                     canTp_send,
                     canTp_recv):

        canTp_send.return_value = False
        canTp_recv.return_value = [0x7F, 0x13]

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/Bootloader.odx', 'bootloader')
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __transferExit to transferExit in the uds object, so can now call below

        try:
            b = a.transferExit([0xF1,0xF2,0xF3,0xF4,0xF5,0xF6,0xF7,0xF8,0xF9,0xFA,0xFB,0xFC,0xFD,0xFE,0xFF])	# ... calls __transferExit, which does the Uds.send
        except:
            b = traceback.format_exc().split("\n")[-2:-1][0] # ... extract the exception text
        canTp_send.assert_called_with([0x37, 0xF1,0xF2,0xF3,0xF4,0xF5,0xF6,0xF7,0xF8,0xF9,0xFA,0xFB,0xFC,0xFD,0xFE,0xFF],False)
        self.assertEqual("Exception: Detected negative response: ['0x7f', '0x13']", b)  # ... transferExit should not return a value


    # patches are inserted in reverse order
    @mock.patch('uds.CanTp.recv')
    @mock.patch('uds.CanTp.send')
    def test_transExitNegResponse_0x22(self,
                     canTp_send,
                     canTp_recv):

        canTp_send.return_value = False
        canTp_recv.return_value = [0x7F, 0x22]

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/Bootloader.odx', 'bootloader')
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __transferExit to transferExit in the uds object, so can now call below

        try:
            b = a.transferExit([0xF1,0xF2,0xF3,0xF4,0xF5,0xF6,0xF7,0xF8,0xF9,0xFA,0xFB,0xFC,0xFD,0xFE,0xFF])	# ... calls __transferExit, which does the Uds.send
        except:
            b = traceback.format_exc().split("\n")[-2:-1][0] # ... extract the exception text
        canTp_send.assert_called_with([0x37, 0xF1,0xF2,0xF3,0xF4,0xF5,0xF6,0xF7,0xF8,0xF9,0xFA,0xFB,0xFC,0xFD,0xFE,0xFF],False)
        self.assertEqual("Exception: Detected negative response: ['0x7f', '0x22']", b)  # ... transferExit should not return a value


    # patches are inserted in reverse order
    @mock.patch('uds.CanTp.recv')
    @mock.patch('uds.CanTp.send')
    def test_transExitNegResponse_0x24(self,
                     canTp_send,
                     canTp_recv):

        canTp_send.return_value = False
        canTp_recv.return_value = [0x7F, 0x24]

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/Bootloader.odx', 'bootloader')
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __transferExit to transferExit in the uds object, so can now call below

        try:
            b = a.transferExit([0xF1,0xF2,0xF3,0xF4,0xF5,0xF6,0xF7,0xF8,0xF9,0xFA,0xFB,0xFC,0xFD,0xFE,0xFF])	# ... calls __transferExit, which does the Uds.send
        except:
            b = traceback.format_exc().split("\n")[-2:-1][0] # ... extract the exception text
        canTp_send.assert_called_with([0x37, 0xF1,0xF2,0xF3,0xF4,0xF5,0xF6,0xF7,0xF8,0xF9,0xFA,0xFB,0xFC,0xFD,0xFE,0xFF],False)
        self.assertEqual("Exception: Detected negative response: ['0x7f', '0x24']", b)  # ... transferExit should not return a value




if __name__ == "__main__":
    unittest.main()