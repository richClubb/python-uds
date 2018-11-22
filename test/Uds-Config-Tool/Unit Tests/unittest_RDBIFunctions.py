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
import sys


class RDBITestCase(unittest.TestCase):
		
    # patches are inserted in reverse order
    @mock.patch('uds.CanTp.recv')
    @mock.patch('uds.CanTp.send')
    def test_rdbiSingleDIDAsciiResponse(self,
                     canTp_send,
                     canTp_recv):

        canTp_send.return_value = False
        # ECU Serial Number = "ABC0011223344556"   (16 bytes as specified in "_Bootloader_87")
        canTp_recv.return_value = [0x62, 0xF1, 0x8C, 0x41, 0x42, 0x43, 0x30, 0x30, 0x31, 0x31, 0x32, 0x32, 0x33, 0x33, 0x34, 0x34, 0x35, 0x35, 0x36]

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/Bootloader.odx', 'bootloader')
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __readDataByIdentifier to readDataByIdentifier in the uds object, so can now call below

        b = a.readDataByIdentifier('ECU Serial Number')	# ... calls __readDataByIdentifier, which does the Uds.send
	
        canTp_send.assert_called_with([0x22, 0xF1, 0x8C],False)
        self.assertEqual({'ECU Serial Number':'ABC0011223344556'}, b)
		
    # patches are inserted in reverse order
    @mock.patch('uds.CanTp.recv')
    @mock.patch('uds.CanTp.send')
    def test_rdbiSingleDIDMixedResponse(self,
                     canTp_send,
                     canTp_recv):

        canTp_send.return_value = False
        canTp_recv.return_value = [0x62, 0xF1, 0x80]
        # Boot Software Identification = "SwId12345678901234567890"   (24 bytes as specified in "_Bootloader_71")
        # numberOfModules = 0x01   (1 bytes as specified in "_Bootloader_1")
        canTp_recv.return_value = [0x62, 0xF1, 0x80, 0x53, 0x77, 0x49, 0x64, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39, 0x30, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39, 0x30, 0x01]



        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/Bootloader.odx', 'bootloader')
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __readDataByIdentifier to readDataByIdentifier in the uds object, so can now call below

        b = a.readDataByIdentifier('Boot Software Identification')	# ... calls __readDataByIdentifier, which does the Uds.send
	
        canTp_send.assert_called_with([0x22, 0xF1, 0x80],False)
        self.assertEqual({'Boot Software Identification':'SwId12345678901234567890','numberOfModules':[0x01]}, b)  # ... not set with a real return value yet!!! (returns a dict or a tuple of dicts if multiple DIDs requested)

"""			

    # patches are inserted in reverse order
    @mock.patch('uds.CanTp.recv')
    @mock.patch('uds.CanTp.send')
    def test_rdbiMultipleDIDMixedResponse(self,
                     canTp_send,
                     canTp_recv):

        canTp_send.return_value = False
        canTp_recv.return_value = [0x62, 0xF1, 0x8C, 0xF1, 0x80]



        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/Bootloader.odx', 'bootloader')
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __readDataByIdentifier to readDataByIdentifier in the uds object, so can now call below

        b = a.readDataByIdentifier(['ECU Serial Number','Boot Software Identification'])	# ... calls __readDataByIdentifier, which does the Uds.send
	
        canTp_send.assert_called_with([0x22, 0xF1, 0x8C])
        self.assertEqual([{'ECU Serial Number':[0x00]},{'Boot Software Identification':[0x00],'numberOfModules':[0x00]}], b)  # ... not set with a real return value yet!!! (returns a dict or a tuple of dicts if multiple DIDs requested)


    # patches are inserted in reverse order
    @mock.patch('uds.CanTp.recv')
    @mock.patch('uds.CanTp.send')
    def test_rdbiMultipleDIDAlternativeOrdering(self,
                     canTp_send,
                     canTp_recv):

        canTp_send.return_value = False
        canTp_recv.return_value = [0x62, 0xF1, 0x80, 0xF1, 0x8C]



        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/Bootloader.odx', 'bootloader')
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __readDataByIdentifier to readDataByIdentifier in the uds object, so can now call below

        b = a.readDataByIdentifier(['Boot Software Identification','ECU Serial Number'])	# ... calls __readDataByIdentifier, which does the Uds.send
	
        canTp_send.assert_called_with([0x22, 0xF1, 0x8C])
        self.assertEqual([{'Boot Software Identification':[0x00],'numberOfModules':[0x00]},{'ECU Serial Number':[0x00]}], b)  # ... not set with a real return value yet!!! (returns a dict or a tuple of dicts if multiple DIDs requested)
"""		

if __name__ == "__main__":
    unittest.main()
