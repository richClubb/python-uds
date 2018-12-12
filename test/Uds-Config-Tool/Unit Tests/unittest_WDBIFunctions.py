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
    def test_wdbiAsciiRequest(self,
                     tp_send,
                     tp_recv):

        tp_send.return_value = False
        tp_recv.return_value = [0x6E, 0xF1, 0x8C]

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/Bootloader.odx', 'bootloader', transportProtocol="TEST")
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __readDataByIdentifier to readDataByIdentifier in the uds object, so can now call below

        b = a.writeDataByIdentifier('ECU Serial Number','ABC0011223344556')	# ... calls __readDataByIdentifier, which does the Uds.send

        tp_send.assert_called_with([0x2E, 0xF1, 0x8C, 0x41, 0x42, 0x43, 0x30, 0x30, 0x31, 0x31, 0x32, 0x32, 0x33, 0x33, 0x34, 0x34, 0x35, 0x35, 0x36],False)
        self.assertEqual(None, b)  # ... wdbi should not return a value
		
		

    # patches are inserted in reverse order
    @mock.patch('uds.TestTp.recv')
    @mock.patch('uds.TestTp.send')
    def test_wdbiMixedRequest(self,
                     tp_send,
                     tp_recv):

        tp_send.return_value = False
        tp_recv.return_value = [0x6E, 0xF1, 0x80]

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/Bootloader.odx', 'bootloader', transportProtocol="TEST")
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __readDataByIdentifier to readDataByIdentifier in the uds object, so can now call below

        b = a.writeDataByIdentifier('Boot Software Identification',[('Boot Software Identification','SwId12345678901234567890'),('numberOfModules',[0x01])])	# ... calls __readDataByIdentifier, which does the Uds.send

        tp_send.assert_called_with([0x2E, 0xF1, 0x80, 0x00, 0x00, 0x00, 0x01, 0x53, 0x77, 0x49, 0x64, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39, 0x30, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39, 0x30],False)
        self.assertEqual(None, b)  # ... wdbi should not return a value

		

    # patches are inserted in reverse order
    @mock.patch('uds.TestTp.recv')
    @mock.patch('uds.TestTp.send')
    def test_wdbiMixedRequestReverseOrder(self,
                     tp_send,
                     tp_recv):

        tp_send.return_value = False
        tp_recv.return_value = [0x6E, 0xF1, 0x80]

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/Bootloader.odx', 'bootloader', transportProtocol="TEST")
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __readDataByIdentifier to readDataByIdentifier in the uds object, so can now call below

        b = a.writeDataByIdentifier('Boot Software Identification',[('numberOfModules',[0x01]),('Boot Software Identification','SwId12345678901234567890')])	# ... calls __readDataByIdentifier, which does the Uds.send

        tp_send.assert_called_with([0x2E, 0xF1, 0x80, 0x00, 0x00, 0x00, 0x01, 0x53, 0x77, 0x49, 0x64, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39, 0x30, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39, 0x30],False)
        self.assertEqual(None, b)  # ... wdbi should not return a value



    # patches are inserted in reverse order
    @mock.patch('uds.TestTp.recv')
    @mock.patch('uds.TestTp.send')
    def test_wdbiNegResponse_0x13(self,
                     tp_send,
                     tp_recv):

        tp_send.return_value = False
        tp_recv.return_value = [0x7F, 0x13]

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/Bootloader.odx', 'bootloader', transportProtocol="TEST")
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __readDataByIdentifier to readDataByIdentifier in the uds object, so can now call below

        try:
            b = a.writeDataByIdentifier('ECU Serial Number','ABC0011223344556')	# ... calls __readDataByIdentifier, which does the Uds.send
        except:
            b = traceback.format_exc().split("\n")[-2:-1][0] # ... extract the exception text
        tp_send.assert_called_with([0x2E, 0xF1, 0x8C, 0x41, 0x42, 0x43, 0x30, 0x30, 0x31, 0x31, 0x32, 0x32, 0x33, 0x33, 0x34, 0x34, 0x35, 0x35, 0x36],False)
        self.assertEqual("Exception: Detected negative response: ['0x7f', '0x13']", b)  # ... wdbi should not return a value


    # patches are inserted in reverse order
    @mock.patch('uds.TestTp.recv')
    @mock.patch('uds.TestTp.send')
    def test_wdbiNegResponse_0x22(self,
                     tp_send,
                     tp_recv):

        tp_send.return_value = False
        tp_recv.return_value = [0x7F, 0x22]

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/Bootloader.odx', 'bootloader', transportProtocol="TEST")
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __readDataByIdentifier to readDataByIdentifier in the uds object, so can now call below

        try:
            b = a.writeDataByIdentifier('ECU Serial Number','ABC0011223344556')	# ... calls __readDataByIdentifier, which does the Uds.send
        except:
            b = traceback.format_exc().split("\n")[-2:-1][0] # ... extract the exception text
        tp_send.assert_called_with([0x2E, 0xF1, 0x8C, 0x41, 0x42, 0x43, 0x30, 0x30, 0x31, 0x31, 0x32, 0x32, 0x33, 0x33, 0x34, 0x34, 0x35, 0x35, 0x36],False)
        self.assertEqual("Exception: Detected negative response: ['0x7f', '0x22']", b)  # ... wdbi should not return a value



    # patches are inserted in reverse order
    @mock.patch('uds.TestTp.recv')
    @mock.patch('uds.TestTp.send')
    def test_wdbiNegResponse_0x31(self,
                     tp_send,
                     tp_recv):

        tp_send.return_value = False
        tp_recv.return_value = [0x7F, 0x31]

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/Bootloader.odx', 'bootloader', transportProtocol="TEST")
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __readDataByIdentifier to readDataByIdentifier in the uds object, so can now call below

        try:
            b = a.writeDataByIdentifier('ECU Serial Number','ABC0011223344556')	# ... calls __readDataByIdentifier, which does the Uds.send
        except:
            b = traceback.format_exc().split("\n")[-2:-1][0] # ... extract the exception text
        tp_send.assert_called_with([0x2E, 0xF1, 0x8C, 0x41, 0x42, 0x43, 0x30, 0x30, 0x31, 0x31, 0x32, 0x32, 0x33, 0x33, 0x34, 0x34, 0x35, 0x35, 0x36],False)
        self.assertEqual("Exception: Detected negative response: ['0x7f', '0x31']", b)  # ... wdbi should not return a value


    # patches are inserted in reverse order
    @mock.patch('uds.TestTp.recv')
    @mock.patch('uds.TestTp.send')
    def test_wdbiNegResponse_0x33(self,
                     tp_send,
                     tp_recv):

        tp_send.return_value = False
        tp_recv.return_value = [0x7F, 0x33]

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/Bootloader.odx', 'bootloader', transportProtocol="TEST")
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __readDataByIdentifier to readDataByIdentifier in the uds object, so can now call below

        try:
            b = a.writeDataByIdentifier('ECU Serial Number','ABC0011223344556')	# ... calls __readDataByIdentifier, which does the Uds.send
        except:
            b = traceback.format_exc().split("\n")[-2:-1][0] # ... extract the exception text
        tp_send.assert_called_with([0x2E, 0xF1, 0x8C, 0x41, 0x42, 0x43, 0x30, 0x30, 0x31, 0x31, 0x32, 0x32, 0x33, 0x33, 0x34, 0x34, 0x35, 0x35, 0x36],False)
        self.assertEqual("Exception: Detected negative response: ['0x7f', '0x33']", b)  # ... wdbi should not return a value


    # patches are inserted in reverse order
    @mock.patch('uds.TestTp.recv')
    @mock.patch('uds.TestTp.send')
    def test_wdbiNegResponse_0x72(self,
                     tp_send,
                     tp_recv):

        tp_send.return_value = False
        tp_recv.return_value = [0x7F, 0x72]

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/Bootloader.odx', 'bootloader', transportProtocol="TEST")
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __readDataByIdentifier to readDataByIdentifier in the uds object, so can now call below

        try:
            b = a.writeDataByIdentifier('ECU Serial Number','ABC0011223344556')	# ... calls __readDataByIdentifier, which does the Uds.send
        except:
            b = traceback.format_exc().split("\n")[-2:-1][0] # ... extract the exception text
        tp_send.assert_called_with([0x2E, 0xF1, 0x8C, 0x41, 0x42, 0x43, 0x30, 0x30, 0x31, 0x31, 0x32, 0x32, 0x33, 0x33, 0x34, 0x34, 0x35, 0x35, 0x36],False)
        self.assertEqual("Exception: Detected negative response: ['0x7f', '0x72']", b)  # ... wdbi should not return a value


if __name__ == "__main__":
    unittest.main()
