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
from uds.uds_config_tool.IHexFunctions import ihexFile
import sys, traceback


class TransferDataTestCase(unittest.TestCase):

    """ Note: this has been run with a modified Uds.py transferIHexFile() function to skip the reqDownload and transExit (I couldn't figure out how to mock these here)  
    # patches are inserted in reverse order
    @mock.patch('uds.CanTp.recv')
    @mock.patch('uds.CanTp.send')
    def test_transDataRequest_ihex(self,
                     canTp_send,
                     canTp_recv,
                     reqDownload,
                     transExit):

        canTp_send.return_value = False
        canTp_recv.return_value = [0x76, 0x01, 0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF]

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/Bootloader.odx', 'bootloader')
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __transferData to transferData in the uds object, so can now call below

        b = a.transferFile("./unitTest01.hex",1280)	# ... calls __transferData, which does the Uds.send - takes blockSequenceCounter and parameterRecord
	
        canTp_send.assert_called_with([0x36, 0x01, 0x00, 0x08, 0x00, 0x70, 0x00, 0x09, 0x4E, 0x80, 0x45, 0x34, 0x30, 0x30, 0x2D, 0x55, 0x44, 0x53],False)
        self.assertEqual({'blockSequenceCounter':[0x01],'transferResponseParameterRecord':[0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF]}, b)  # ... (returns a dict)
    """
		

    """ REMOVING THIS TEST AS "block" list is no longer exposed this way ...
    # patches are inserted in reverse order
    @mock.patch('uds.CanTp.recv')
    @mock.patch('uds.CanTp.send')
    def test_transDataRequest_ihex01(self,
                     canTp_send,
                     canTp_recv):

        canTp_send.return_value = False
        canTp_recv.return_value = [0x76, 0x01, 0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF]

        app_blocks = ihexFile("./unitTest01.hex")
        app_blocks.transmitChunksize = 1280

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/Bootloader.odx', 'bootloader')
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __transferData to transferData in the uds object, so can now call below

        b = a.transferData(transferBlock=app_blocks.block[0])	# ... calls __transferData, which does the Uds.send - takes blockSequenceCounter and parameterRecord
	
        canTp_send.assert_called_with([0x36, 0x01, 0x00, 0x08, 0x00, 0x70, 0x00, 0x09, 0x4E, 0x80, 0x45, 0x34, 0x30, 0x30, 0x2D, 0x55, 0x44, 0x53],False)
        self.assertEqual({'blockSequenceCounter':[0x01],'transferResponseParameterRecord':[0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF]}, b)  # ... (returns a dict)
    """


    # patches are inserted in reverse order
    @mock.patch('uds.CanTp.recv')
    @mock.patch('uds.CanTp.send')
    def test_transDataRequest_ihex02(self,
                     canTp_send,
                     canTp_recv):

        canTp_send.return_value = False
        canTp_recv.return_value = [0x76, 0x01, 0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF]

        app_blocks = ihexFile("./unitTest01.hex")
        app_blocks.transmitChunksize = 1280

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/Bootloader.odx', 'bootloader')
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __transferData to transferData in the uds object, so can now call below

        b = a.transferData(transferBlocks=app_blocks)	# ... calls __transferData, which does the Uds.send - takes blockSequenceCounter and parameterRecord
	
        canTp_send.assert_called_with([0x36, 0x01, 0x00, 0x08, 0x00, 0x70, 0x00, 0x09, 0x4E, 0x80, 0x45, 0x34, 0x30, 0x30, 0x2D, 0x55, 0x44, 0x53],False)
        self.assertEqual({'blockSequenceCounter':[0x01],'transferResponseParameterRecord':[0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF]}, b)  # ... (returns a dict)


    """ REMOVING THIS TEST AS "block" list is no longer exposed this way ...
    # patches are inserted in reverse order
    @mock.patch('uds.CanTp.recv')
    @mock.patch('uds.CanTp.send')
    def test_transDataRequest_ihex03(self,
                     canTp_send,
                     canTp_recv):

        canTp_send.return_value = False
        canTp_recv.return_value = [0x76, 0x01, 0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF]

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/Bootloader.odx', 'bootloader',ihexFile="./unitTest01.hex")
        a.ihexFile.transmitChunksize = 1280
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __transferData to transferData in the uds object, so can now call below

        b = a.transferData(transferBlock=a.ihexFile.block[0])	# ... calls __transferData, which does the Uds.send - takes blockSequenceCounter and parameterRecord
	
        canTp_send.assert_called_with([0x36, 0x01, 0x00, 0x08, 0x00, 0x70, 0x00, 0x09, 0x4E, 0x80, 0x45, 0x34, 0x30, 0x30, 0x2D, 0x55, 0x44, 0x53],False)
        self.assertEqual({'blockSequenceCounter':[0x01],'transferResponseParameterRecord':[0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF]}, b)  # ... (returns a dict)
    """


    # patches are inserted in reverse order
    @mock.patch('uds.CanTp.recv')
    @mock.patch('uds.CanTp.send')
    def test_transDataRequest_ihex04(self,
                     canTp_send,
                     canTp_recv):

        canTp_send.return_value = False
        canTp_recv.return_value = [0x76, 0x01, 0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF]

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/Bootloader.odx', 'bootloader',ihexFile="./unitTest01.hex")
        a.ihexFile.transmitChunksize = 1280
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __transferData to transferData in the uds object, so can now call below

        b = a.transferData(transferBlocks=a.ihexFile)	# ... calls __transferData, which does the Uds.send - takes blockSequenceCounter and parameterRecord
	
        canTp_send.assert_called_with([0x36, 0x01, 0x00, 0x08, 0x00, 0x70, 0x00, 0x09, 0x4E, 0x80, 0x45, 0x34, 0x30, 0x30, 0x2D, 0x55, 0x44, 0x53],False)
        self.assertEqual({'blockSequenceCounter':[0x01],'transferResponseParameterRecord':[0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF]}, b)  # ... (returns a dict)


    # patches are inserted in reverse order
    @mock.patch('uds.CanTp.recv')
    @mock.patch('uds.CanTp.send')
    def test_transDataRequest_ihex05(self,
                     canTp_send,
                     canTp_recv):

        canTp_send.return_value = False
        canTp_recv.return_value = [0x76, 0x01, 0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF]

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/Bootloader.odx', 'bootloader')
        a.ihexFile = "./unitTest01.hex"
        a.ihexFile.transmitChunksize = 1280
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __transferData to transferData in the uds object, so can now call below

        b = a.transferData(transferBlocks=a.ihexFile)	# ... calls __transferData, which does the Uds.send - takes blockSequenceCounter and parameterRecord
	
        canTp_send.assert_called_with([0x36, 0x01, 0x00, 0x08, 0x00, 0x70, 0x00, 0x09, 0x4E, 0x80, 0x45, 0x34, 0x30, 0x30, 0x2D, 0x55, 0x44, 0x53],False)
        self.assertEqual({'blockSequenceCounter':[0x01],'transferResponseParameterRecord':[0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF]}, b)  # ... (returns a dict)


    # patches are inserted in reverse order
    @mock.patch('uds.CanTp.recv')
    @mock.patch('uds.CanTp.send')
    def test_transDataRequest(self,
                     canTp_send,
                     canTp_recv):

        canTp_send.return_value = False
        canTp_recv.return_value = [0x76, 0x01, 0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF]

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/Bootloader.odx', 'bootloader')
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __transferData to transferData in the uds object, so can now call below

        b = a.transferData(0x01,[0xF1,0xF2,0xF3,0xF4,0xF5,0xF6,0xF7,0xF8,0xF9,0xFA,0xFB,0xFC,0xFD,0xFE,0xFF])	# ... calls __transferData, which does the Uds.send - takes blockSequenceCounter and parameterRecord
	
        canTp_send.assert_called_with([0x36, 0x01, 0xF1,0xF2,0xF3,0xF4,0xF5,0xF6,0xF7,0xF8,0xF9,0xFA,0xFB,0xFC,0xFD,0xFE,0xFF],False)
        self.assertEqual({'blockSequenceCounter':[0x01],'transferResponseParameterRecord':[0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF]}, b)  # ... (returns a dict)


    # patches are inserted in reverse order
    @mock.patch('uds.CanTp.recv')
    @mock.patch('uds.CanTp.send')
    def test_transDataRequestSeq02(self,
                     canTp_send,
                     canTp_recv):

        canTp_send.return_value = False
        canTp_recv.return_value = [0x76, 0x02, 0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF]

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/Bootloader.odx', 'bootloader')
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __transferData to transferData in the uds object, so can now call below

        b = a.transferData(0x02,[0xF1,0xF2,0xF3,0xF4,0xF5,0xF6,0xF7,0xF8,0xF9,0xFA,0xFB,0xFC,0xFD,0xFE,0xFF])	# ... calls __transferData, which does the Uds.send - takes blockSequenceCounter and parameterRecord
	
        canTp_send.assert_called_with([0x36, 0x02, 0xF1,0xF2,0xF3,0xF4,0xF5,0xF6,0xF7,0xF8,0xF9,0xFA,0xFB,0xFC,0xFD,0xFE,0xFF],False)
        self.assertEqual({'blockSequenceCounter':[0x02],'transferResponseParameterRecord':[0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF]}, b)  # ... (returns a dict)




    # patches are inserted in reverse order
    @mock.patch('uds.CanTp.recv')
    @mock.patch('uds.CanTp.send')
    def test_transDataNegResponse_0x13(self,
                     canTp_send,
                     canTp_recv):

        canTp_send.return_value = False
        canTp_recv.return_value = [0x7F, 0x13]

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/Bootloader.odx', 'bootloader')
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __transferData to transferData in the uds object, so can now call below

        try:
            b = a.transferData(0x01,[0xF1,0xF2,0xF3,0xF4,0xF5,0xF6,0xF7,0xF8,0xF9,0xFA,0xFB,0xFC,0xFD,0xFE,0xFF])	# ... calls __transferData, which does the Uds.send
        except:
            b = traceback.format_exc().split("\n")[-2:-1][0] # ... extract the exception text
        canTp_send.assert_called_with([0x36, 0x01, 0xF1,0xF2,0xF3,0xF4,0xF5,0xF6,0xF7,0xF8,0xF9,0xFA,0xFB,0xFC,0xFD,0xFE,0xFF],False)
        self.assertEqual("Exception: Detected negative response: ['0x7f', '0x13']", b)  # ... transferData should not return a value


    # patches are inserted in reverse order
    @mock.patch('uds.CanTp.recv')
    @mock.patch('uds.CanTp.send')
    def test_transDataNegResponse_0x24(self,
                     canTp_send,
                     canTp_recv):

        canTp_send.return_value = False
        canTp_recv.return_value = [0x7F, 0x24]

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/Bootloader.odx', 'bootloader')
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __transferData to transferData in the uds object, so can now call below

        try:
            b = a.transferData(0x01,[0xF1,0xF2,0xF3,0xF4,0xF5,0xF6,0xF7,0xF8,0xF9,0xFA,0xFB,0xFC,0xFD,0xFE,0xFF])	# ... calls __transferData, which does the Uds.send
        except:
            b = traceback.format_exc().split("\n")[-2:-1][0] # ... extract the exception text
        canTp_send.assert_called_with([0x36, 0x01, 0xF1,0xF2,0xF3,0xF4,0xF5,0xF6,0xF7,0xF8,0xF9,0xFA,0xFB,0xFC,0xFD,0xFE,0xFF],False)
        self.assertEqual("Exception: Detected negative response: ['0x7f', '0x24']", b)  # ... transferData should not return a value


    # patches are inserted in reverse order
    @mock.patch('uds.CanTp.recv')
    @mock.patch('uds.CanTp.send')
    def test_transDataNegResponse_0x31(self,
                     canTp_send,
                     canTp_recv):

        canTp_send.return_value = False
        canTp_recv.return_value = [0x7F, 0x31]

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/Bootloader.odx', 'bootloader')
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __transferData to transferData in the uds object, so can now call below

        try:
            b = a.transferData(0x01,[0xF1,0xF2,0xF3,0xF4,0xF5,0xF6,0xF7,0xF8,0xF9,0xFA,0xFB,0xFC,0xFD,0xFE,0xFF])	# ... calls __transferData, which does the Uds.send
        except:
            b = traceback.format_exc().split("\n")[-2:-1][0] # ... extract the exception text
        canTp_send.assert_called_with([0x36, 0x01, 0xF1,0xF2,0xF3,0xF4,0xF5,0xF6,0xF7,0xF8,0xF9,0xFA,0xFB,0xFC,0xFD,0xFE,0xFF],False)
        self.assertEqual("Exception: Detected negative response: ['0x7f', '0x31']", b)  # ... transferData should not return a value


    # patches are inserted in reverse order
    @mock.patch('uds.CanTp.recv')
    @mock.patch('uds.CanTp.send')
    def test_transDataNegResponse_0x71(self,
                     canTp_send,
                     canTp_recv):

        canTp_send.return_value = False
        canTp_recv.return_value = [0x7F, 0x71]

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/Bootloader.odx', 'bootloader')
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __transferData to transferData in the uds object, so can now call below

        try:
            b = a.transferData(0x01,[0xF1,0xF2,0xF3,0xF4,0xF5,0xF6,0xF7,0xF8,0xF9,0xFA,0xFB,0xFC,0xFD,0xFE,0xFF])	# ... calls __transferData, which does the Uds.send
        except:
            b = traceback.format_exc().split("\n")[-2:-1][0] # ... extract the exception text
        canTp_send.assert_called_with([0x36, 0x01, 0xF1,0xF2,0xF3,0xF4,0xF5,0xF6,0xF7,0xF8,0xF9,0xFA,0xFB,0xFC,0xFD,0xFE,0xFF],False)
        self.assertEqual("Exception: Detected negative response: ['0x7f', '0x71']", b)  # ... transferData should not return a value


    # patches are inserted in reverse order
    @mock.patch('uds.CanTp.recv')
    @mock.patch('uds.CanTp.send')
    def test_transDataNegResponse_0x72(self,
                     canTp_send,
                     canTp_recv):

        canTp_send.return_value = False
        canTp_recv.return_value = [0x7F, 0x72]

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/Bootloader.odx', 'bootloader')
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __transferData to transferData in the uds object, so can now call below

        try:
            b = a.transferData(0x01,[0xF1,0xF2,0xF3,0xF4,0xF5,0xF6,0xF7,0xF8,0xF9,0xFA,0xFB,0xFC,0xFD,0xFE,0xFF])	# ... calls __transferData, which does the Uds.send
        except:
            b = traceback.format_exc().split("\n")[-2:-1][0] # ... extract the exception text
        canTp_send.assert_called_with([0x36, 0x01, 0xF1,0xF2,0xF3,0xF4,0xF5,0xF6,0xF7,0xF8,0xF9,0xFA,0xFB,0xFC,0xFD,0xFE,0xFF],False)
        self.assertEqual("Exception: Detected negative response: ['0x7f', '0x72']", b)  # ... transferData should not return a value


    # patches are inserted in reverse order
    @mock.patch('uds.CanTp.recv')
    @mock.patch('uds.CanTp.send')
    def test_transDataNegResponse_0x73(self,
                     canTp_send,
                     canTp_recv):

        canTp_send.return_value = False
        canTp_recv.return_value = [0x7F, 0x73]

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/Bootloader.odx', 'bootloader')
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __transferData to transferData in the uds object, so can now call below

        try:
            b = a.transferData(0x01,[0xF1,0xF2,0xF3,0xF4,0xF5,0xF6,0xF7,0xF8,0xF9,0xFA,0xFB,0xFC,0xFD,0xFE,0xFF])	# ... calls __transferData, which does the Uds.send
        except:
            b = traceback.format_exc().split("\n")[-2:-1][0] # ... extract the exception text
        canTp_send.assert_called_with([0x36, 0x01, 0xF1,0xF2,0xF3,0xF4,0xF5,0xF6,0xF7,0xF8,0xF9,0xFA,0xFB,0xFC,0xFD,0xFE,0xFF],False)
        self.assertEqual("Exception: Detected negative response: ['0x7f', '0x73']", b)  # ... transferData should not return a value


    # patches are inserted in reverse order
    @mock.patch('uds.CanTp.recv')
    @mock.patch('uds.CanTp.send')
    def test_transDataNegResponse_0x92(self,
                     canTp_send,
                     canTp_recv):

        canTp_send.return_value = False
        canTp_recv.return_value = [0x7F, 0x92]

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/Bootloader.odx', 'bootloader')
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __transferData to transferData in the uds object, so can now call below

        try:
            b = a.transferData(0x01,[0xF1,0xF2,0xF3,0xF4,0xF5,0xF6,0xF7,0xF8,0xF9,0xFA,0xFB,0xFC,0xFD,0xFE,0xFF])	# ... calls __transferData, which does the Uds.send
        except:
            b = traceback.format_exc().split("\n")[-2:-1][0] # ... extract the exception text
        canTp_send.assert_called_with([0x36, 0x01, 0xF1,0xF2,0xF3,0xF4,0xF5,0xF6,0xF7,0xF8,0xF9,0xFA,0xFB,0xFC,0xFD,0xFE,0xFF],False)
        self.assertEqual("Exception: Detected negative response: ['0x7f', '0x92']", b)  # ... transferData should not return a value


    # patches are inserted in reverse order
    @mock.patch('uds.CanTp.recv')
    @mock.patch('uds.CanTp.send')
    def test_transDataNegResponse_0x93(self,
                     canTp_send,
                     canTp_recv):

        canTp_send.return_value = False
        canTp_recv.return_value = [0x7F, 0x93]

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/Bootloader.odx', 'bootloader')
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __transferData to transferData in the uds object, so can now call below

        try:
            b = a.transferData(0x01,[0xF1,0xF2,0xF3,0xF4,0xF5,0xF6,0xF7,0xF8,0xF9,0xFA,0xFB,0xFC,0xFD,0xFE,0xFF])	# ... calls __transferData, which does the Uds.send
        except:
            b = traceback.format_exc().split("\n")[-2:-1][0] # ... extract the exception text
        canTp_send.assert_called_with([0x36, 0x01, 0xF1,0xF2,0xF3,0xF4,0xF5,0xF6,0xF7,0xF8,0xF9,0xFA,0xFB,0xFC,0xFD,0xFE,0xFF],False)
        self.assertEqual("Exception: Detected negative response: ['0x7f', '0x93']", b)  # ... transferData should not return a value


if __name__ == "__main__":
    unittest.main()