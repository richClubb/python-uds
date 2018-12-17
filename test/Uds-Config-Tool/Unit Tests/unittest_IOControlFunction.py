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


#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# NOTE: these tests cannot currently be run with the existing ODX, as it does not contain an IO Ctrl service
# For now, I've simply run a regression of the wdbi and routine ctrl tests to ensure I've not broken anything.
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
class IOControlTestCase(unittest.TestCase):

    # patches are inserted in reverse order
    @mock.patch('uds.TestTp.recv')
    @mock.patch('uds.TestTp.send')
    def test_ioControlRequest(self,
                     tp_send,
                     tp_recv):

        tp_send.return_value = False
        # ... WHERE 0xXX, 0xXX needs to be the DID used in the ODX!!!!!		
        tp_recv.return_value = [0x6F, 0xXX, 0xXX, 0xA1, 0xB2, 0xC3, 0xD4]

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/Bootloader.odx', 'bootloader', transportProtocol="TEST")
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __inputOutputControl to inputOutputControl in the uds object, so can now call below

        # NOT FINAL DATA!!! ... assumes a service def in the ODX requiring 4 bytes for each of the parameters (1 to N required for each).
        b = a.inputOutputControl('<DID Name>',[('controlOptionRecord',[0x01, 0x02, 0x03, 0x04]),('controlEnableMaskRecord',[0xFF, 0x0F, 0x0F, 0xFF])])	# ... calls __inputOutputControl, which does the Uds.send

        # ... WHERE 0xXX, 0xXX needs to be the DID used in the ODX!!!!!		
        tp_send.assert_called_with([0x2F, 0xXX, 0xXX, 0x01, 0x02, 0x03, 0x04, 0xFF, 0x0F, 0x0F, 0xFF],False)
        self.assertEqual({'controlStatusRecord':[0xA1, 0xB2, 0xC3, 0xD4]}, b)


		

    # patches are inserted in reverse order
    @mock.patch('uds.TestTp.recv')
    @mock.patch('uds.TestTp.send')
    def test_ecuResetNegResponse_0x13(self,
                     tp_send,
                     tp_recv):

        tp_send.return_value = False
        tp_recv.return_value = [0x7F, 0x13]

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/Bootloader.odx', 'bootloader', transportProtocol="TEST")
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __inputOutputControl to inputOutputControl in the uds object, so can now call below

        try:
            # NOT FINAL DATA!!! ... assumes a service def in the ODX requiring 4 bytes for each of the parameters (1 to N required for each).
            b = a.inputOutputControl('<DID Name>',[('controlOptionRecord',[0x01,0x02,0x03,0x04]),('controlEnableMaskRecord',[0xFF,0x0F,0x0F,0xFF])])	# ... calls __inputOutputControl, which does the Uds.send
        except:
            b = traceback.format_exc().split("\n")[-2:-1][0] # ... extract the exception text
        tp_send.assert_called_with([0x2F, 0xXX, 0xXX, 0x01, 0x02, 0x03, 0x04, 0xFF, 0x0F, 0x0F, 0xFF],False)
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
        a = createUdsConnection('../Functional Tests/Bootloader.odx', 'bootloader', transportProtocol="TEST")
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __inputOutputControl to inputOutputControl in the uds object, so can now call below

        try:
            # NOT FINAL DATA!!! ... assumes a service def in the ODX requiring 4 bytes for each of the parameters (1 to N required for each).
            a.inputOutputControl('<DID Name>',[('controlOptionRecord',[0x01,0x02,0x03,0x04]),('controlEnableMaskRecord',[0xFF,0x0F,0x0F,0xFF])])	# ... calls __inputOutputControl, which does the Uds.send
        except:
            b = traceback.format_exc().split("\n")[-2:-1][0] # ... extract the exception text
        tp_send.assert_called_with([0x2F, 0xXX, 0xXX, 0x01, 0x02, 0x03, 0x04, 0xFF, 0x0F, 0x0F, 0xFF],False)
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
        a = createUdsConnection('../Functional Tests/Bootloader.odx', 'bootloader', transportProtocol="TEST")
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __inputOutputControl to inputOutputControl in the uds object, so can now call below

        try:
            # NOT FINAL DATA!!! ... assumes a service def in the ODX requiring 4 bytes for each of the parameters (1 to N required for each).
            a.inputOutputControl('<DID Name>',[('controlOptionRecord',[0x01,0x02,0x03,0x04]),('controlEnableMaskRecord',[0xFF,0x0F,0x0F,0xFF])])	# ... calls __inputOutputControl, which does the Uds.send
        except:
            b = traceback.format_exc().split("\n")[-2:-1][0] # ... extract the exception text
        tp_send.assert_called_with([0x2F, 0xXX, 0xXX, 0x01, 0x02, 0x03, 0x04, 0xFF, 0x0F, 0x0F, 0xFF],False)
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
        a = createUdsConnection('../Functional Tests/Bootloader.odx', 'bootloader', transportProtocol="TEST")
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __inputOutputControl to inputOutputControl in the uds object, so can now call below

        try:
            # NOT FINAL DATA!!! ... assumes a service def in the ODX requiring 4 bytes for each of the parameters (1 to N required for each).
            a.inputOutputControl('<DID Name>',[('controlOptionRecord',[0x01,0x02,0x03,0x04]),('controlEnableMaskRecord',[0xFF,0x0F,0x0F,0xFF])])	# ... calls __inputOutputControl, which does the Uds.send
        except:
            b = traceback.format_exc().split("\n")[-2:-1][0] # ... extract the exception text
        tp_send.assert_called_with([0x2F, 0xXX, 0xXX, 0x01, 0x02, 0x03, 0x04, 0xFF, 0x0F, 0x0F, 0xFF],False)
        self.assertEqual("Exception: Detected negative response: ['0x7f', '0x33']", b)

	



if __name__ == "__main__":
    unittest.main()