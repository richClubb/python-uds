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


class WDBITestCase(unittest.TestCase):
		
    # patches are inserted in reverse order
    @mock.patch('uds.CanTp.recv')
    @mock.patch('uds.CanTp.send')
    def test_wdbiAsciiRequest(self,
                     canTp_send,
                     canTp_recv):

        canTp_send.return_value = False
        #???????????we need to assert the send value
        canTp_recv.return_value = [0x22, 0xF1, 0x8C]

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/Bootloader.odx', 'bootloader')
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __readDataByIdentifier to readDataByIdentifier in the uds object, so can now call below

        b = a.writeDataByIdentifier('ECU Serial Number','??????????')	# ... calls __readDataByIdentifier, which does the Uds.send
	
        self.assertEqual(None, b)  # ... wdbi should not return a value
		
		
    # patches are inserted in reverse order
    @mock.patch('uds.CanTp.recv')
    @mock.patch('uds.CanTp.send')
    def test_wdbiMixedRequest(self,
                     canTp_send,
                     canTp_recv):

        canTp_send.return_value = False
        #???????????we need to assert the send value
        canTp_recv.return_value = [0x22, 0xF1, 0x80]



        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/Bootloader.odx', 'bootloader')
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __readDataByIdentifier to readDataByIdentifier in the uds object, so can now call below

        b = a.writeDataByIdentifier('Boot Software Identification',{'Boot Software Identification':[0x00],'numberOfModules':[0x00]})	# ... calls __readDataByIdentifier, which does the Uds.send
	
        self.assertEqual(None, b)  # ... wdbi should not return a value

"""
    # patches are inserted in reverse order
    @mock.patch('uds.CanTp.recv')
    @mock.patch('uds.CanTp.send')
    def test_rdbiMultipleDIDMixedResponse(self,
                     canTp_send,
                     canTp_recv):

        get_config_mock.return_value = mockConfig
        canTp_send.return_value = False
        canTp_recv.return_value = [0x22, 0xF1, 0x8C, 0xF1, 0x80]



        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('Bootloader.odx', 'bootloader')
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __readDataByIdentifier to readDataByIdentifier in the uds object, so can now call below

        b = a.readDataByIdentifier(['ECU Serial Number','Boot Software Identification'])	# ... calls __readDataByIdentifier, which does the Uds.send
	
        self.assertEqual([{'ECU Serial Number':[0x00]},{'Boot Software Identification':[0x00],'numberOfModules':[0x00]}], b)  # ... not set with a real return value yet!!! (returns a dict or a tuple of dicts if multiple DIDs requested)


    # patches are inserted in reverse order
    @mock.patch('uds.CanTp.recv')
    @mock.patch('uds.CanTp.send')
    def test_rdbiMultipleDIDAlternativeOrdering(self,
                     canTp_send,
                     canTp_recv):

        get_config_mock.return_value = mockConfig
        canTp_send.return_value = False
        canTp_recv.return_value = [0x22, 0xF1, 0x80, 0xF1, 0x8C]



        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('Bootloader.odx', 'bootloader')
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __readDataByIdentifier to readDataByIdentifier in the uds object, so can now call below

        b = a.readDataByIdentifier(['Boot Software Identification','ECU Serial Number'])	# ... calls __readDataByIdentifier, which does the Uds.send
	
        self.assertEqual([{'Boot Software Identification':[0x00],'numberOfModules':[0x00]},{'ECU Serial Number':[0x00]}], b)  # ... not set with a real return value yet!!! (returns a dict or a tuple of dicts if multiple DIDs requested)
"""		

if __name__ == "__main__":
    unittest.main()