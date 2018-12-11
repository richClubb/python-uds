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


class ECUResetTestCase(unittest.TestCase):

    # patches are inserted in reverse order
    @mock.patch('uds.CanTp.recv')
    @mock.patch('uds.CanTp.send')
    def test_ecuResetRequestDfltNoSuppress(self,
                     canTp_send,
                     canTp_recv):

        canTp_send.return_value = False
        canTp_recv.return_value = [0x71, 0x01, 0xFF, 0x00, 0x30]

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/Bootloader.odx', 'bootloader')
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __readDataByIdentifier to readDataByIdentifier in the uds object, so can now call below

        b = a.routineControl('Erase Memory',[('memoryAddress',[0x00, 0x00, 0x00, 0x01]),('memorySize',[0x00, 0x00, 0xF0, 0x00])])	# ... calls __ecuReset, which does the Uds.send
	
        canTp_send.assert_called_with([0x31, 0x01, 0xFF, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0xF0, 0x00],False)
        self.assertEqual({'Type':[0x01],'Erase Memory Status':[0x30]}, b)  # ... wdbi should not return a value


    """
    # patches are inserted in reverse order
    @mock.patch('uds.CanTp.recv')
    @mock.patch('uds.CanTp.send')
    def test_ecuResetRequestNoSuppress(self,
                     canTp_send,
                     canTp_recv):

        canTp_send.return_value = False
        canTp_recv.return_value = [0x51, 0x01]

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/Bootloader.odx', 'bootloader')
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __readDataByIdentifier to readDataByIdentifier in the uds object, so can now call below

        b = a.ecuReset('Hard Reset',suppressResponse=False)	# ... calls __ecuReset, which does the Uds.send
	
        canTp_send.assert_called_with([0x11, 0x01],False)
        self.assertEqual({'Type':[0x01]}, b)  # ... wdbi should not return a value


    # patches are inserted in reverse order
    @mock.patch('uds.CanTp.send')
    def test_ecuResetRequestSuppress(self,
                     canTp_send):

        canTp_send.return_value = False

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/Bootloader.odx', 'bootloader')
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __readDataByIdentifier to readDataByIdentifier in the uds object, so can now call below

        b = a.ecuReset('Hard Reset',suppressResponse=True)	# ... calls __ecuReset, which does the Uds.send
	
        canTp_send.assert_called_with([0x11, 0x81],False)
        self.assertEqual(None, b)  # ... wdbi should not return a value
		

    # patches are inserted in reverse order
    @mock.patch('uds.CanTp.recv')
    @mock.patch('uds.CanTp.send')
    def test_ecuResetNegResponse_0x12(self,
                     canTp_send,
                     canTp_recv):

        canTp_send.return_value = False
        canTp_recv.return_value = [0x7F, 0x12]

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/Bootloader.odx', 'bootloader')
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __readDataByIdentifier to readDataByIdentifier in the uds object, so can now call below

        try:
            b = a.ecuReset('Hard Reset')	# ... calls __ecuReset, which does the Uds.send
        except:
            b = traceback.format_exc().split("\n")[-2:-1][0] # ... extract the exception text
        canTp_send.assert_called_with([0x11, 0x01],False)
        self.assertEqual("Exception: Detected negative response: ['0x7f', '0x12']", b)  # ... wdbi should not return a value

	
    # patches are inserted in reverse order
    @mock.patch('uds.CanTp.recv')
    @mock.patch('uds.CanTp.send')
    def test_ecuResetNegResponse_0x13(self,
                     canTp_send,
                     canTp_recv):

        canTp_send.return_value = False
        canTp_recv.return_value = [0x7F, 0x13]

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/Bootloader.odx', 'bootloader')
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __readDataByIdentifier to readDataByIdentifier in the uds object, so can now call below

        try:
            b = a.ecuReset('Hard Reset')	# ... calls __ecuReset, which does the Uds.send
        except:
            b = traceback.format_exc().split("\n")[-2:-1][0] # ... extract the exception text
        canTp_send.assert_called_with([0x11, 0x01],False)
        self.assertEqual("Exception: Detected negative response: ['0x7f', '0x13']", b)  # ... wdbi should not return a value


    # patches are inserted in reverse order
    @mock.patch('uds.CanTp.recv')
    @mock.patch('uds.CanTp.send')
    def test_ecuResetNegResponse_0x22(self,
                     canTp_send,
                     canTp_recv):

        canTp_send.return_value = False
        canTp_recv.return_value = [0x7F, 0x22]

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/Bootloader.odx', 'bootloader')
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __readDataByIdentifier to readDataByIdentifier in the uds object, so can now call below

        try:
            b = a.ecuReset('Hard Reset')	# ... calls __ecuReset, which does the Uds.send
        except:
            b = traceback.format_exc().split("\n")[-2:-1][0] # ... extract the exception text
        canTp_send.assert_called_with([0x11, 0x01],False)
        self.assertEqual("Exception: Detected negative response: ['0x7f', '0x22']", b)  # ... wdbi should not return a value
    """



if __name__ == "__main__":
    unittest.main()