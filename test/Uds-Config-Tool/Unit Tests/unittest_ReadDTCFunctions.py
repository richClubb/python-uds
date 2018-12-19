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
from uds.uds_config_tool.ISOStandard.ISOStandard import IsoReadDTCSubfunction, IsoReadDTCStatusMask as Mask
import sys, traceback


class ReadDTCTestCase(unittest.TestCase):
		
    """
	Example calls (the tests only include options present in the ODX test file):
	
    a.readDTC(IsoReadDTCSubfunction.reportNumberOfDTCByStatusMask, DTCStatusMask=Mask.confirmedDtc & Mask.testFailedSinceLastClear)
    a.readDTC(IsoReadDTCSubfunction.reportDTCByStatusMask, DTCStatusMask=Mask.confirmedDtc & Mask.testFailedSinceLastClear)
    a.readDTC(IsoReadDTCSubfunction.reportDTCSnapshotIdentification, DTCMaskRecord=[0xF1, 0xC8, 0x55], DTCSnapshotRecordNumber=0x34)
    a.readDTC(IsoReadDTCSubfunction.reportDTCSnapshotRecordByDTCNumber, DTCMaskRecord=[0xF1, 0xC8, 0x55], DTCSnapshotRecordNumber=0x34)
    a.readDTC(IsoReadDTCSubfunction.reportDTCSnapshotRecordByRecordNumber, DTCSnapshotRecordNumber=0x34)
    a.readDTC(IsoReadDTCSubfunction.reportDTCExtendedDataRecordByDTCNumber, DTCMaskRecord=[0xF1, 0xC8, 0x55], DTCExtendedRecordNumber=0x12)
    a.readDTC(IsoReadDTCSubfunction.reportNumberOfDTCBySeverityMaskRecord, DTCStatusMask=Mask.confirmedDtc & Mask.testFailedSinceLastClear, DTCSeverityMaskRecord=Mask.confirmedDtc)
    a.readDTC(IsoReadDTCSubfunction.reportDTCBySeverityMaskRecord, DTCStatusMask=Mask.confirmedDtc & Mask.testFailedSinceLastClear, DTCSeverityMaskRecord=Mask.confirmedDtc)
    a.readDTC(IsoReadDTCSubfunction.reportSeverityInformationOfDTC, DTCMaskRecord=[0xF1, 0xC8, 0x55])
    a.readDTC(IsoReadDTCSubfunction.reportSupportedDTC)
    a.readDTC(IsoReadDTCSubfunction.reportFirstTestFailedDTC)
    a.readDTC(IsoReadDTCSubfunction.reportFirstConfirmedDTC)
    a.readDTC(IsoReadDTCSubfunction.reportMostRecentTestFailedDTC)
    a.readDTC(IsoReadDTCSubfunction.reportMostRecentConfirmedDTC)
    a.readDTC(IsoReadDTCSubfunction.reportMirrorMemoryDTCByStatusMask, DTCStatusMask=Mask.confirmedDtc & Mask.testFailedSinceLastClear)
    a.readDTC(IsoReadDTCSubfunction.reportMirrorMemoryDTCExtendedDataRecordByDTCNumber, DTCMaskRecord=[0xF1, 0xC8, 0x55], DTCExtendedRecordNumber=0x12)
    a.readDTC(IsoReadDTCSubfunction.reportNumberOfMirrorMemoryDTCByStatusMask, DTCStatusMask=Mask.confirmedDtc & Mask.testFailedSinceLastClear)
    a.readDTC(IsoReadDTCSubfunction.reportNumberOfEmissionsRelatedOBDDTCByStatusMask, DTCStatusMask=Mask.confirmedDtc & Mask.testFailedSinceLastClear)
    a.readDTC(IsoReadDTCSubfunction.reportEmissionsRelatedOBDDTCByStatusMask, DTCStatusMask=Mask.confirmedDtc & Mask.testFailedSinceLastClear)

    """

		# patches are inserted in reverse order
    @mock.patch('uds.TestTp.recv')
    @mock.patch('uds.TestTp.send')
    def test_readDTC_reportDTCByStatusMask(self,
                     tp_send,
                     tp_recv):

        tp_send.return_value = False
        # ECU Serial Number = "ABC0011223344556"   (16 bytes as specified in "_Bootloader_87")
        tp_recv.return_value = [0x59, 0x02, 0x28, 0xF1, 0xC8, 0x55, 0x01, 0xF1, 0xD0, 0x56, 0x01, 0xF1, 0xD8, 0x57, 0x01]

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/Bootloader.odx', 'bootloader', transportProtocol="TEST")
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __readDataByIdentifier to readDataByIdentifier in the uds object, so can now call below


        b = a.readDTC(IsoReadDTCSubfunction.reportDTCByStatusMask, Mask=StatusMask.confirmedDtc & Mask.testFailedSinceLastClear)	# ... calls __readDataByIdentifier, which does the Uds.send
	
        tp_send.assert_called_with([0x19, 0x02, 0x28],False)
        self.assertEqual({'DTCStatusAvailabilityMask':[0x28],'DTCAndStatusRecord':[{'DTC':[0xF1, 0xC8, 0x55],'statusOfDTC':[0x01]},{'DTC':[0xF1, 0xD0, 0x56],'statusOfDTC':[0x01]},{'DTC':[0xF1, 0xD8, 0x57],'statusOfDTC':[0x01]}]}, b)


    """
    # patches are inserted in reverse order
    @mock.patch('uds.TestTp.recv')
    @mock.patch('uds.TestTp.send')
    def test_rdbiSingleDIDMixedResponse(self,
                     tp_send,
                     tp_recv):

        tp_send.return_value = False
        # numberOfModules = 0x01   (1 bytes as specified in "_Bootloader_1")
        # Boot Software Identification = "SwId12345678901234567890"   (24 bytes as specified in "_Bootloader_71")
        tp_recv.return_value = [0x62, 0xF1, 0x80, 0x01, 0x53, 0x77, 0x49, 0x64, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39, 0x30, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39, 0x30]


        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/Bootloader.odx', 'bootloader', transportProtocol="TEST")
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __readDataByIdentifier to readDataByIdentifier in the uds object, so can now call below

        b = a.readDataByIdentifier('Boot Software Identification')	# ... calls __readDataByIdentifier, which does the Uds.send

        tp_send.assert_called_with([0x22, 0xF1, 0x80],False)
        self.assertEqual({'Boot Software Identification': 'SwId12345678901234567890','numberOfModules': [0x01]}, b)

		
    # patches are inserted in reverse order
    @mock.patch('uds.TestTp.recv')
    @mock.patch('uds.TestTp.send')
    def test_rdbiMultipleDIDMixedResponse(self,
                     tp_send,
                     tp_recv):

        tp_send.return_value = False
        tp_recv.return_value = [0x62, 0xF1, 0x8C, 0xF1, 0x80]
        # ECU Serial Number = "ABC0011223344556"   (16 bytes as specified in "_Bootloader_87")
        # numberOfModules = 0x01   (1 bytes as specified in "_Bootloader_1")
        # Boot Software Identification = "SwId12345678901234567890"   (24 bytes as specified in "_Bootloader_71")
        tp_recv.return_value = [0x62, 0xF1, 0x8C, 0x41, 0x42, 0x43, 0x30, 0x30, 0x31, 0x31, 0x32, 0x32, 0x33, 0x33, 0x34, 0x34, 0x35, 0x35, 0x36, 0xF1, 0x80, 0x01, 0x53, 0x77, 0x49, 0x64, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39, 0x30, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39, 0x30]



        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/Bootloader.odx', 'bootloader', transportProtocol="TEST")
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __readDataByIdentifier to readDataByIdentifier in the uds object, so can now call below

        b = a.readDataByIdentifier(['ECU Serial Number','Boot Software Identification'])	# ... calls __readDataByIdentifier, which does the Uds.send
	
        tp_send.assert_called_with([0x22, 0xF1, 0x8C, 0xF1, 0x80],False)
        self.assertEqual(({'ECU Serial Number':'ABC0011223344556'},{'Boot Software Identification':'SwId12345678901234567890','numberOfModules':[0x01]}), b)


    # patches are inserted in reverse order
    @mock.patch('uds.TestTp.recv')
    @mock.patch('uds.TestTp.send')
    def test_rdbiMultipleDIDAlternativeOrdering(self,
                     tp_send,
                     tp_recv):

        tp_send.return_value = False
        tp_recv.return_value = [0x62, 0xF1, 0x80, 0xF1, 0x8C]
        # numberOfModules = 0x01   (1 bytes as specified in "_Bootloader_1")
        # Boot Software Identification = "SwId12345678901234567890"   (24 bytes as specified in "_Bootloader_71")
        # ECU Serial Number = "ABC0011223344556"   (16 bytes as specified in "_Bootloader_87")
        tp_recv.return_value = [0x62, 0xF1, 0x80, 0x01, 0x53, 0x77, 0x49, 0x64, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39, 0x30, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39, 0x30, 0xF1, 0x8C, 0x41, 0x42, 0x43, 0x30, 0x30, 0x31, 0x31, 0x32, 0x32, 0x33, 0x33, 0x34, 0x34, 0x35, 0x35, 0x36]



        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/Bootloader.odx', 'bootloader', transportProtocol="TEST")
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __readDataByIdentifier to readDataByIdentifier in the uds object, so can now call below

        b = a.readDataByIdentifier(['Boot Software Identification','ECU Serial Number'])	# ... calls __readDataByIdentifier, which does the Uds.send
	
        tp_send.assert_called_with([0x22, 0xF1, 0x80, 0xF1, 0x8C],False)
        self.assertEqual(({'Boot Software Identification':'SwId12345678901234567890','numberOfModules':[0x01]},{'ECU Serial Number':'ABC0011223344556'}), b)  # ... not set with a real return value yet!!! (returns a dict or a tuple of dicts if multiple DIDs requested)

    """
    """
    # patches are inserted in reverse order
    @mock.patch('uds.TestTp.recv')
    @mock.patch('uds.TestTp.send')
    def test_readDTCNegResponse_0x12(self,
                     tp_send,
                     tp_recv):

        tp_send.return_value = False
        tp_recv.return_value = [0x7F, 0x12]

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/Bootloader.odx', 'bootloader', transportProtocol="TEST")
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __readDataByIdentifier to readDataByIdentifier in the uds object, so can now call below

        try:
            b = a.readDTC([ReadDTCSubfunc.reportDTCByStatusMask],[("????????":[0x??])])	# ... calls __readDTC, which does the Uds.send
        except:
            b = traceback.format_exc().split("\n")[-2:-1][0] # ... extract the exception text
        tp_send.assert_called_with([0x19, 0x02, 0x???],False)
        self.assertEqual("Exception: Detected negative response: ['0x7f', '0x12']", b)  # ... wdbi should not return a value



    # patches are inserted in reverse order
    @mock.patch('uds.TestTp.recv')
    @mock.patch('uds.TestTp.send')
    def test_readDTCNegResponse_0x13(self,
                     tp_send,
                     tp_recv):

        tp_send.return_value = False
        tp_recv.return_value = [0x7F, 0x13]

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/Bootloader.odx', 'bootloader', transportProtocol="TEST")
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __readDataByIdentifier to readDataByIdentifier in the uds object, so can now call below

        try:
            b = a.readDTC([ReadDTCSubfunc.reportDTCByStatusMask],[("????????":[0x??])])	# ... calls __readDTC, which does the Uds.send
        except:
            b = traceback.format_exc().split("\n")[-2:-1][0] # ... extract the exception text
        tp_send.assert_called_with([0x19, 0x02, 0x???],False)
        self.assertEqual("Exception: Detected negative response: ['0x7f', '0x13']", b)  # ... wdbi should not return a value


    # patches are inserted in reverse order
    @mock.patch('uds.TestTp.recv')
    @mock.patch('uds.TestTp.send')
    def test_readDTCNegResponse_0x31(self,
                     tp_send,
                     tp_recv):

        tp_send.return_value = False
        tp_recv.return_value = [0x7F, 0x31]

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/Bootloader.odx', 'bootloader', transportProtocol="TEST")
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __readDataByIdentifier to readDataByIdentifier in the uds object, so can now call below

        try:
            b = a.readDTC([ReadDTCSubfunc.reportDTCByStatusMask],[("????????":[0x??])])	# ... calls __readDTC, which does the Uds.send
        except:
            b = traceback.format_exc().split("\n")[-2:-1][0] # ... extract the exception text
        tp_send.assert_called_with([0x19, 0x02, 0x???],False)
        self.assertEqual("Exception: Detected negative response: ['0x7f', '0x31']", b)  # ... wdbi should not return a value
    """





if __name__ == "__main__":
    unittest.main()
