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
	
    a.readDTC(IsoReadDTCSubfunction.reportNumberOfDTCByStatusMask, DTCStatusMask=Mask.confirmedDtc + Mask.testFailedSinceLastClear)
    a.readDTC(IsoReadDTCSubfunction.reportDTCByStatusMask, DTCStatusMask=Mask.confirmedDtc + Mask.testFailedSinceLastClear)
    a.readDTC(IsoReadDTCSubfunction.reportDTCSnapshotIdentification, DTCMaskRecord=[0xF1, 0xC8, 0x55], DTCSnapshotRecordNumber=0x34)
    a.readDTC(IsoReadDTCSubfunction.reportDTCSnapshotRecordByDTCNumber, DTCMaskRecord=[0xF1, 0xC8, 0x55], DTCSnapshotRecordNumber=0x34)
    a.readDTC(IsoReadDTCSubfunction.reportDTCSnapshotRecordByRecordNumber, DTCSnapshotRecordNumber=0x34)
    a.readDTC(IsoReadDTCSubfunction.reportDTCExtendedDataRecordByDTCNumber, DTCMaskRecord=[0xF1, 0xC8, 0x55], DTCExtendedRecordNumber=0x12)
    a.readDTC(IsoReadDTCSubfunction.reportNumberOfDTCBySeverityMaskRecord, DTCStatusMask=Mask.confirmedDtc + Mask.testFailedSinceLastClear, DTCSeverityMaskRecord=Mask.confirmedDtc)
    a.readDTC(IsoReadDTCSubfunction.reportDTCBySeverityMaskRecord, DTCStatusMask=Mask.confirmedDtc + Mask.testFailedSinceLastClear, DTCSeverityMaskRecord=Mask.confirmedDtc)
    a.readDTC(IsoReadDTCSubfunction.reportSeverityInformationOfDTC, DTCMaskRecord=[0xF1, 0xC8, 0x55])
    a.readDTC(IsoReadDTCSubfunction.reportSupportedDTC)
    a.readDTC(IsoReadDTCSubfunction.reportFirstTestFailedDTC)
    a.readDTC(IsoReadDTCSubfunction.reportFirstConfirmedDTC)
    a.readDTC(IsoReadDTCSubfunction.reportMostRecentTestFailedDTC)
    a.readDTC(IsoReadDTCSubfunction.reportMostRecentConfirmedDTC)
    a.readDTC(IsoReadDTCSubfunction.reportMirrorMemoryDTCByStatusMask, DTCStatusMask=Mask.confirmedDtc + Mask.testFailedSinceLastClear)
    a.readDTC(IsoReadDTCSubfunction.reportMirrorMemoryDTCExtendedDataRecordByDTCNumber, DTCMaskRecord=[0xF1, 0xC8, 0x55], DTCExtendedRecordNumber=0x12)
    a.readDTC(IsoReadDTCSubfunction.reportNumberOfMirrorMemoryDTCByStatusMask, DTCStatusMask=Mask.confirmedDtc + Mask.testFailedSinceLastClear)
    a.readDTC(IsoReadDTCSubfunction.reportNumberOfEmissionsRelatedOBDDTCByStatusMask, DTCStatusMask=Mask.confirmedDtc + Mask.testFailedSinceLastClear)
    a.readDTC(IsoReadDTCSubfunction.reportEmissionsRelatedOBDDTCByStatusMask, DTCStatusMask=Mask.confirmedDtc + Mask.testFailedSinceLastClear)

    """


    """ IMPORTANT NOTE: !!!!!!!!!!!!!!!!!!
	!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
	Still need to add tests for the requests that require ODX parsing to determine response length and structure for the DTC !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
	See tables 253 to 255 in the spec
	
	There are also a number of commented out tests which have not been run - in these cases, the code has been written (untested though), but the required data is not in the 
	ODX file to permit testing.
	!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    """


    # patches are inserted in reverse order
    @mock.patch('uds.TestTp.recv')
    @mock.patch('uds.TestTp.send')
    def test_readDTC_reportDTCByStatusMask(self,
                     tp_send,
                     tp_recv):

        tp_send.return_value = False
        tp_recv.return_value = [0x59, 0x02, 0x28, 0xF1, 0xC8, 0x55, 0x01, 0xF1, 0xD0, 0x56, 0x01, 0xF1, 0xD8, 0x57, 0x01]

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/EBC-Diagnostics_old.odx', 'bootloader', transportProtocol="TEST")
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __readDataByIdentifier to readDataByIdentifier in the uds object, so can now call below


        b = a.readDTC(IsoReadDTCSubfunction.reportDTCByStatusMask, DTCStatusMask=Mask.confirmedDtc + Mask.testFailedSinceLastClear)	# ... calls __readDataByIdentifier, which does the Uds.send
	
        tp_send.assert_called_with([0x19, 0x02, 0x28],False)
        self.assertEqual({'DTCStatusAvailabilityMask':[0x28],'DTCAndStatusRecord':[{'DTC':[0xF1, 0xC8, 0x55],'statusOfDTC':[0x01]},{'DTC':[0xF1, 0xD0, 0x56],'statusOfDTC':[0x01]},{'DTC':[0xF1, 0xD8, 0x57],'statusOfDTC':[0x01]}]}, b)


    # patches are inserted in reverse order
    @mock.patch('uds.TestTp.recv')
    @mock.patch('uds.TestTp.send')
    def test_readDTC_reportSupportedDTC(self,
                     tp_send,
                     tp_recv):

        tp_send.return_value = False
        tp_recv.return_value = [0x59, 0x0A, 0x28, 0xF1, 0xC8, 0x55, 0x01, 0xF1, 0xD0, 0x56, 0x01, 0xF1, 0xD8, 0x57, 0x01]

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/EBC-Diagnostics_old.odx', 'bootloader', transportProtocol="TEST")
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __readDataByIdentifier to readDataByIdentifier in the uds object, so can now call below


        b = a.readDTC(IsoReadDTCSubfunction.reportSupportedDTC)	# ... calls __readDataByIdentifier, which does the Uds.send	
        tp_send.assert_called_with([0x19, 0x0A],False)
        self.assertEqual({'DTCStatusAvailabilityMask':[0x28],'DTCAndStatusRecord':[{'DTC':[0xF1, 0xC8, 0x55],'statusOfDTC':[0x01]},{'DTC':[0xF1, 0xD0, 0x56],'statusOfDTC':[0x01]},{'DTC':[0xF1, 0xD8, 0x57],'statusOfDTC':[0x01]}]}, b)


    """
	NOTE: this Sub-Function is not supported in the current test ODX file, so test has currently not been run!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # patches are inserted in reverse order
    @mock.patch('uds.TestTp.recv')
    @mock.patch('uds.TestTp.send')
    def test_readDTC_reportFirstTestFailedDTC(self,
                     tp_send,
                     tp_recv):

        tp_send.return_value = False
        tp_recv.return_value = [0x59, 0x0B, 0x28, 0xF1, 0xC8, 0x55, 0x01, 0xF1, 0xD0, 0x56, 0x01, 0xF1, 0xD8, 0x57, 0x01]

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/EBC-Diagnostics_old.odx', 'bootloader', transportProtocol="TEST")
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __readDataByIdentifier to readDataByIdentifier in the uds object, so can now call below


        b = a.readDTC(IsoReadDTCSubfunction.reportFirstTestFailedDTC)	# ... calls __readDataByIdentifier, which does the Uds.send
	
        tp_send.assert_called_with([0x19, 0x0B],False)
        self.assertEqual({'DTCStatusAvailabilityMask':[0x28],'DTCAndStatusRecord':[{'DTC':[0xF1, 0xC8, 0x55],'statusOfDTC':[0x01]},{'DTC':[0xF1, 0xD0, 0x56],'statusOfDTC':[0x01]},{'DTC':[0xF1, 0xD8, 0x57],'statusOfDTC':[0x01]}]}, b)
    """


    """
	NOTE: this Sub-Function is not supported in the current test ODX file, so test has currently not been run!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # patches are inserted in reverse order
    @mock.patch('uds.TestTp.recv')
    @mock.patch('uds.TestTp.send')
    def test_readDTC_reportFirstConfirmedDTC(self,
                     tp_send,
                     tp_recv):

        tp_send.return_value = False
        tp_recv.return_value = [0x59, 0x0C, 0x28, 0xF1, 0xC8, 0x55, 0x01, 0xF1, 0xD0, 0x56, 0x01, 0xF1, 0xD8, 0x57, 0x01]

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/EBC-Diagnostics_old.odx', 'bootloader', transportProtocol="TEST")
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __readDataByIdentifier to readDataByIdentifier in the uds object, so can now call below


        b = a.readDTC(IsoReadDTCSubfunction.reportFirstConfirmedDTC)	# ... calls __readDataByIdentifier, which does the Uds.send
	
        tp_send.assert_called_with([0x19, 0x0C],False)
        self.assertEqual({'DTCStatusAvailabilityMask':[0x28],'DTCAndStatusRecord':[{'DTC':[0xF1, 0xC8, 0x55],'statusOfDTC':[0x01]},{'DTC':[0xF1, 0xD0, 0x56],'statusOfDTC':[0x01]},{'DTC':[0xF1, 0xD8, 0x57],'statusOfDTC':[0x01]}]}, b)
    """

    """
	NOTE: this Sub-Function is not supported in the current test ODX file, so test has currently not been run!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # patches are inserted in reverse order
    @mock.patch('uds.TestTp.recv')
    @mock.patch('uds.TestTp.send')
    def test_readDTC_reportMostRecentTestFailedDTC(self,
                     tp_send,
                     tp_recv):

        tp_send.return_value = False
        tp_recv.return_value = [0x59, 0x0D, 0x28, 0xF1, 0xC8, 0x55, 0x01, 0xF1, 0xD0, 0x56, 0x01, 0xF1, 0xD8, 0x57, 0x01]

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/EBC-Diagnostics_old.odx', 'bootloader', transportProtocol="TEST")
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __readDataByIdentifier to readDataByIdentifier in the uds object, so can now call below


        b = a.readDTC(IsoReadDTCSubfunction.reportMostRecentTestFailedDTC)	# ... calls __readDataByIdentifier, which does the Uds.send
	
        tp_send.assert_called_with([0x19, 0x0D],False)
        self.assertEqual({'DTCStatusAvailabilityMask':[0x28],'DTCAndStatusRecord':[{'DTC':[0xF1, 0xC8, 0x55],'statusOfDTC':[0x01]},{'DTC':[0xF1, 0xD0, 0x56],'statusOfDTC':[0x01]},{'DTC':[0xF1, 0xD8, 0x57],'statusOfDTC':[0x01]}]}, b)
    """

    """
	NOTE: this Sub-Function is not supported in the current test ODX file, so test has currently not been run!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # patches are inserted in reverse order
    @mock.patch('uds.TestTp.recv')
    @mock.patch('uds.TestTp.send')
    def test_readDTC_reportMostRecentConfirmedDTC(self,
                     tp_send,
                     tp_recv):

        tp_send.return_value = False
        tp_recv.return_value = [0x59, 0x0E, 0x28, 0xF1, 0xC8, 0x55, 0x01, 0xF1, 0xD0, 0x56, 0x01, 0xF1, 0xD8, 0x57, 0x01]

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/EBC-Diagnostics_old.odx', 'bootloader', transportProtocol="TEST")
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __readDataByIdentifier to readDataByIdentifier in the uds object, so can now call below


        b = a.readDTC(IsoReadDTCSubfunction.reportMostRecentConfirmedDTC)	# ... calls __readDataByIdentifier, which does the Uds.send
	
        tp_send.assert_called_with([0x19, 0x0E],False)
        self.assertEqual({'DTCStatusAvailabilityMask':[0x28],'DTCAndStatusRecord':[{'DTC':[0xF1, 0xC8, 0x55],'statusOfDTC':[0x01]},{'DTC':[0xF1, 0xD0, 0x56],'statusOfDTC':[0x01]},{'DTC':[0xF1, 0xD8, 0x57],'statusOfDTC':[0x01]}]}, b)
    """

    """
	NOTE: this Sub-Function is not supported in the current test ODX file, so test has currently not been run!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # patches are inserted in reverse order
    @mock.patch('uds.TestTp.recv')
    @mock.patch('uds.TestTp.send')
    def test_readDTC_reportMirrorMemoryDTCByStatusMask(self,
                     tp_send,
                     tp_recv):

        tp_send.return_value = False
        tp_recv.return_value = [0x59, 0x0F, 0x28, 0xF1, 0xC8, 0x55, 0x01, 0xF1, 0xD0, 0x56, 0x01, 0xF1, 0xD8, 0x57, 0x01]

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/EBC-Diagnostics_old.odx', 'bootloader', transportProtocol="TEST")
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __readDataByIdentifier to readDataByIdentifier in the uds object, so can now call below

        b = a.readDTC(IsoReadDTCSubfunction.reportMirrorMemoryDTCByStatusMask, DTCStatusMask=Mask.confirmedDtc + Mask.testFailedSinceLastClear)	# ... calls __readDataByIdentifier, which does the Uds.send
	
        tp_send.assert_called_with([0x19, 0x0F, 0x28],False)
        self.assertEqual({'DTCStatusAvailabilityMask':[0x28],'DTCAndStatusRecord':[{'DTC':[0xF1, 0xC8, 0x55],'statusOfDTC':[0x01]},{'DTC':[0xF1, 0xD0, 0x56],'statusOfDTC':[0x01]},{'DTC':[0xF1, 0xD8, 0x57],'statusOfDTC':[0x01]}]}, b)
    """	

    """
	NOTE: this Sub-Function is not supported in the current test ODX file, so test has currently not been run!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # patches are inserted in reverse order
    @mock.patch('uds.TestTp.recv')
    @mock.patch('uds.TestTp.send')
    def test_readDTC_reportEmissionsRelatedOBDDTCByStatusMask(self,
                     tp_send,
                     tp_recv):

        tp_send.return_value = False
        tp_recv.return_value = [0x59, 0x13, 0x28, 0xF1, 0xC8, 0x55, 0x01, 0xF1, 0xD0, 0x56, 0x01, 0xF1, 0xD8, 0x57, 0x01]

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/EBC-Diagnostics_old.odx', 'bootloader', transportProtocol="TEST")
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __readDataByIdentifier to readDataByIdentifier in the uds object, so can now call below


        b = a.readDTC(IsoReadDTCSubfunction.reportEmissionsRelatedOBDDTCByStatusMask, DTCStatusMask=Mask.confirmedDtc + Mask.testFailedSinceLastClear)	# ... calls __readDataByIdentifier, which does the Uds.send
	
        tp_send.assert_called_with([0x19, 0x13, 0xF1, 0xC8, 0x55, 0x12],False)
        self.assertEqual({'DTCStatusAvailabilityMask':[0x28],'DTCAndStatusRecord':[{'DTC':[0xF1, 0xC8, 0x55],'statusOfDTC':[0x01]},{'DTC':[0xF1, 0xD0, 0x56],'statusOfDTC':[0x01]},{'DTC':[0xF1, 0xD8, 0x57],'statusOfDTC':[0x01]}]}, b)
    """

	
    # patches are inserted in reverse order
    @mock.patch('uds.TestTp.recv')
    @mock.patch('uds.TestTp.send')
    def test_readDTC_reportNumberOfDTCByStatusMask(self,
                     tp_send,
                     tp_recv):

        tp_send.return_value = False
        tp_recv.return_value = [0x59, 0x01, 0x28, 0x00, 0x00, 0x03]

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/EBC-Diagnostics_old.odx', 'bootloader', transportProtocol="TEST")
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __readDataByIdentifier to readDataByIdentifier in the uds object, so can now call below


        b = a.readDTC(IsoReadDTCSubfunction.reportNumberOfDTCByStatusMask, DTCStatusMask=Mask.confirmedDtc + Mask.testFailedSinceLastClear)	# ... calls __readDataByIdentifier, which does the Uds.send
	
        tp_send.assert_called_with([0x19, 0x01, 0x28],False)
        self.assertEqual({'DTCStatusAvailabilityMask':[0x28],'DTCFormatIdentifier':[0x00],'DTCCount':[3]}, b)


    """
	NOTE: this Sub-Function is not supported in the current test ODX file, so test has currently not been run!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # patches are inserted in reverse order
    @mock.patch('uds.TestTp.recv')
    @mock.patch('uds.TestTp.send')
    def test_readDTC_reportNumberOfDTCBySeverityMaskRecord(self,
                     tp_send,
                     tp_recv):

        tp_send.return_value = False
        tp_recv.return_value = [0x59, 0x07, 0x28, 0x00, 0x00, 0x03]

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/EBC-Diagnostics_old.odx', 'bootloader', transportProtocol="TEST")
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __readDataByIdentifier to readDataByIdentifier in the uds object, so can now call below


        b = a.readDTC(IsoReadDTCSubfunction.reportNumberOfDTCBySeverityMaskRecord, DTCStatusMask=Mask.confirmedDtc + Mask.testFailedSinceLastClear, DTCSeverityMaskRecord=Mask.confirmedDtc)	# ... calls __readDataByIdentifier, which does the Uds.send
	
        tp_send.assert_called_with([0x19, 0x07, 0x28],False)
        self.assertEqual({'DTCStatusAvailabilityMask':[0x28],'DTCFormatIdentifier':[0x00],'DTCCount':[3]}, b)
    """

    """
	NOTE: this Sub-Function is not supported in the current test ODX file, so test has currently not been run!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # patches are inserted in reverse order
    @mock.patch('uds.TestTp.recv')
    @mock.patch('uds.TestTp.send')
    def test_readDTC_reportNumberOfMirrorMemoryDTCByStatusMask(self,
                     tp_send,
                     tp_recv):

        tp_send.return_value = False
        tp_recv.return_value = [0x59, 0x11, 0x28, 0x00, 0x00, 0x03]

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/EBC-Diagnostics_old.odx', 'bootloader', transportProtocol="TEST")
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __readDataByIdentifier to readDataByIdentifier in the uds object, so can now call below


        b = a.readDTC(IsoReadDTCSubfunction.reportNumberOfMirrorMemoryDTCByStatusMask, DTCStatusMask=Mask.confirmedDtc + Mask.testFailedSinceLastClear)	# ... calls __readDataByIdentifier, which does the Uds.send
	
        tp_send.assert_called_with([0x19, 0x11, 0x28],False)
        self.assertEqual({'DTCStatusAvailabilityMask':[0x28],'DTCFormatIdentifier':[0x00],'DTCCount':[3]}, b)
    """

    """
	NOTE: this Sub-Function is not supported in the current test ODX file, so test has currently not been run!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # patches are inserted in reverse order
    @mock.patch('uds.TestTp.recv')
    @mock.patch('uds.TestTp.send')
    def test_readDTC_reportNumberOfEmissionsRelatedOBDDTCByStatusMask(self,
                     tp_send,
                     tp_recv):

        tp_send.return_value = False
        tp_recv.return_value = [0x59, 0x12, 0x28, 0x00, 0x00, 0x03]

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/EBC-Diagnostics_old.odx', 'bootloader', transportProtocol="TEST")
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __readDataByIdentifier to readDataByIdentifier in the uds object, so can now call below


        b = a.readDTC(IsoReadDTCSubfunction.reportNumberOfEmissionsRelatedOBDDTCByStatusMask, DTCStatusMask=Mask.confirmedDtc + Mask.testFailedSinceLastClear)	# ... calls __readDataByIdentifier, which does the Uds.send
	
        tp_send.assert_called_with([0x19, 0x12, 0x28],False)
        self.assertEqual({'DTCStatusAvailabilityMask':[0x28],'DTCFormatIdentifier':[0x00],'DTCCount':[3]}, b)
    """


    """
	NOTE: this Sub-Function is not supported in the current test ODX file, so test has currently not been run!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # patches are inserted in reverse order
    @mock.patch('uds.TestTp.recv')
    @mock.patch('uds.TestTp.send')
    def test_readDTC_reportDTCBySeverityMaskRecord(self,
                     tp_send,
                     tp_recv):

        tp_send.return_value = False
        tp_recv.return_value = [0x59, 0x08, 0x08, 0x08, 0x01, 0xF1, 0xC8, 0x55, 0x01, 0x08, 0x02, 0xF1, 0xD0, 0x56, 0x01]

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/EBC-Diagnostics_old.odx', 'bootloader', transportProtocol="TEST")
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __readDataByIdentifier to readDataByIdentifier in the uds object, so can now call below


        b = a.readDTC(IsoReadDTCSubfunction.reportDTCBySeverityMaskRecord, DTCStatusMask=Mask.confirmedDtc + Mask.testFailedSinceLastClear, DTCSeverityMaskRecord=Mask.confirmedDtc)	# ... calls __readDataByIdentifier, which does the Uds.send
	
        tp_send.assert_called_with([0x19, 0x08, 0x28],False)
        self.assertEqual({'DTCStatusAvailabilityMask':[0x08],'DTCAndSeverityRecord':[{'DTCSeverity':[0x08],'DTCFunctionalUnit':[0x01],'DTC':[0xF1, 0xC8, 0x55],'statusOfDTC':[0x01]},{'DTCSeverity':[0x08],'DTCFunctionalUnit':[0x02],'DTC':[0xF1, 0xD0, 0x56],'statusOfDTC':[0x01]}]}, b)
    """

    """
	NOTE: this Sub-Function is not supported in the current test ODX file, so test has currently not been run!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # patches are inserted in reverse order
    @mock.patch('uds.TestTp.recv')
    @mock.patch('uds.TestTp.send')
    def test_readDTC_reportSeverityInformationOfDTC(self,
                     tp_send,
                     tp_recv):

        tp_send.return_value = False
        tp_recv.return_value = [0x59, 0x09, 0x08, 0x08, 0x01, 0xF1, 0xC8, 0x55, 0x01]

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/EBC-Diagnostics_old.odx', 'bootloader', transportProtocol="TEST")
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __readDataByIdentifier to readDataByIdentifier in the uds object, so can now call below


        b = a.readDTC(IsoReadDTCSubfunction.reportSeverityInformationOfDTC, DTCMaskRecord=[0xF1, 0xC8, 0x55])	# ... calls __readDataByIdentifier, which does the Uds.send
	
        tp_send.assert_called_with([0x19, 0x09, 0x28],False)
        self.assertEqual({'DTCStatusAvailabilityMask':[0x08],'DTCAndSeverityRecord':[{'DTCSeverity':[0x08],'DTCFunctionalUnit':[0x01],'DTC':[0xF1, 0xC8, 0x55],'statusOfDTC':[0x01]}]}, b)
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
        a = createUdsConnection('../Functional Tests/EBC-Diagnostics_old.odx', 'bootloader', transportProtocol="TEST")
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __readDTC to readDTC in the uds object, so can now call below

        try:
            b = a.readDTC(IsoReadDTCSubfunction.reportDTCByStatusMask, DTCStatusMask=Mask.confirmedDtc + Mask.testFailedSinceLastClear)	# ... calls __readDTC, which does the Uds.send
        except:
            b = traceback.format_exc().split("\n")[-2:-1][0] # ... extract the exception text
        tp_send.assert_called_with([0x19, 0x02, 0x28],False)
        self.assertEqual("Exception: Detected negative response: ['0x7f', '0x12']", b)



    # patches are inserted in reverse order
    @mock.patch('uds.TestTp.recv')
    @mock.patch('uds.TestTp.send')
    def test_readDTCNegResponse_0x13(self,
                     tp_send,
                     tp_recv):

        tp_send.return_value = False
        tp_recv.return_value = [0x7F, 0x13]

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/EBC-Diagnostics_old.odx', 'bootloader', transportProtocol="TEST")
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __readDTC to readDTC in the uds object, so can now call below

        try:
            b = a.readDTC(IsoReadDTCSubfunction.reportDTCByStatusMask, DTCStatusMask=Mask.confirmedDtc + Mask.testFailedSinceLastClear)	# ... calls __readDTC, which does the Uds.send
        except:
            b = traceback.format_exc().split("\n")[-2:-1][0] # ... extract the exception text
        tp_send.assert_called_with([0x19, 0x02, 0x28],False)
        self.assertEqual("Exception: Detected negative response: ['0x7f', '0x13']", b)


    # patches are inserted in reverse order
    @mock.patch('uds.TestTp.recv')
    @mock.patch('uds.TestTp.send')
    def test_readDTCNegResponse_0x31(self,
                     tp_send,
                     tp_recv):

        tp_send.return_value = False
        tp_recv.return_value = [0x7F, 0x31]

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/EBC-Diagnostics_old.odx', 'bootloader', transportProtocol="TEST")
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __readDTC to readDTC in the uds object, so can now call below

        try:
            b = a.readDTC(IsoReadDTCSubfunction.reportDTCByStatusMask, DTCStatusMask=Mask.confirmedDtc + Mask.testFailedSinceLastClear)	# ... calls __readDTC, which does the Uds.send
        except:
            b = traceback.format_exc().split("\n")[-2:-1][0] # ... extract the exception text
        tp_send.assert_called_with([0x19, 0x02, 0x28],False)
        self.assertEqual("Exception: Detected negative response: ['0x7f', '0x31']", b)



if __name__ == "__main__":
    unittest.main()
