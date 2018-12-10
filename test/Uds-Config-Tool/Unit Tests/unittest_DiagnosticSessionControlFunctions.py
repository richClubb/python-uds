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


class DiagnosticSessionControlTestCase(unittest.TestCase):

    # patches are inserted in reverse order
    @mock.patch('uds.CanTp.recv')
    @mock.patch('uds.CanTp.send')
    def test_diagSessCtrlRequestDfltNoSuppress(self,
                     canTp_send,
                     canTp_recv):

        canTp_send.return_value = False
        canTp_recv.return_value = [0x50, 0x01, 0x00, 0x05, 0x00, 0x0A] # ... can return 1 to N bytes in the sessionParameterRecord - looking into this one

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/Bootloader.odx', 'bootloader')
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __diagnosticSessionControl to diagnosticSessionControl in the uds object, so can now call below

        b = a.diagnosticSessionControl('Default Session')	# ... calls __diagnosticSessionControl, which does the Uds.send
        canTp_send.assert_called_with([0x10, 0x01],False)
        self.assertEqual({'Type':[0x01], 'P3':[0x00, 0x05], 'P3Ex':[0x00, 0x0A]}, b)  # ... diagnosticSessionControl should not return a value


    # patches are inserted in reverse order
    @mock.patch('uds.CanTp.recv')
    @mock.patch('uds.CanTp.send')
    def test_diagSessCtrlRequestNoSuppress(self,
                     canTp_send,
                     canTp_recv):

        canTp_send.return_value = False
        canTp_recv.return_value = [0x50, 0x01, 0x00, 0x05, 0x00, 0x0A] # ... can return 1 to N bytes in the sessionParameterRecord - looking into this one

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/Bootloader.odx', 'bootloader')
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __diagnosticSessionControl to diagnosticSessionControl in the uds object, so can now call below

        b = a.diagnosticSessionControl('Default Session',suppressResponse=False)	# ... calls __diagnosticSessionControl, which does the Uds.send
        canTp_send.assert_called_with([0x10, 0x01],False)
        self.assertEqual({'Type':[0x01], 'P3':[0x00, 0x05], 'P3Ex':[0x00, 0x0A]}, b)  # ... diagnosticSessionControl should not return a value


    # patches are inserted in reverse order
    @mock.patch('uds.CanTp.send')
    def test_diagSessCtrlRequestSuppress(self,
                     canTp_send):

        canTp_send.return_value = False

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/Bootloader.odx', 'bootloader')
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __diagnosticSessionControl to diagnosticSessionControl in the uds object, so can now call below

        b = a.diagnosticSessionControl('Default Session',suppressResponse=True)	# ... calls __diagnosticSessionControl, which does the Uds.send
        canTp_send.assert_called_with([0x10, 0x81],False)
        self.assertEqual(None, b)  # ... diagnosticSessionControl should not return a value




    # patches are inserted in reverse order
    @mock.patch('uds.CanTp.recv')
    @mock.patch('uds.CanTp.send')
    def test_diagSessCtrlRequestProgrammingSession(self,
                     canTp_send,
                     canTp_recv):

        canTp_send.return_value = False
        canTp_recv.return_value = [0x50, 0x02, 0x00, 0x06, 0x00, 0x09] # ... can return 1 to N bytes in the sessionParameterRecord - looking into this one

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/Bootloader.odx', 'bootloader')
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __diagnosticSessionControl to diagnosticSessionControl in the uds object, so can now call below

        b = a.diagnosticSessionControl('Programming Session')	# ... calls __diagnosticSessionControl, which does the Uds.send
        canTp_send.assert_called_with([0x10, 0x02],False)
        self.assertEqual({'Type':[0x02], 'P3':[0x00, 0x06], 'P3Ex':[0x00, 0x09]}, b)  # ... diagnosticSessionControl should not return a value


    # patches are inserted in reverse order
    @mock.patch('uds.CanTp.recv')
    @mock.patch('uds.CanTp.send')
    def test_diagSessCtrlRequestExtendedDiagnosticSession(self,
                     canTp_send,
                     canTp_recv):

        canTp_send.return_value = False
        canTp_recv.return_value = [0x50, 0x03, 0x00, 0x07, 0x00, 0x08] # ... can return 1 to N bytes in the sessionParameterRecord - looking into this one

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/Bootloader.odx', 'bootloader')
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __diagnosticSessionControl to diagnosticSessionControl in the uds object, so can now call below

        b = a.diagnosticSessionControl('Extended Diagnostic Session')	# ... calls __diagnosticSessionControl, which does the Uds.send
        canTp_send.assert_called_with([0x10, 0x03],False)
        self.assertEqual({'Type':[0x03], 'P3':[0x00, 0x07], 'P3Ex':[0x00, 0x08]}, b)  # ... diagnosticSessionControl should not return a value



    # patches are inserted in reverse order
    @mock.patch('uds.CanTp.recv')
    @mock.patch('uds.CanTp.send')
    def test_diagSessCtrlNegResponse_0x12(self,
                     canTp_send,
                     canTp_recv):

        canTp_send.return_value = False
        canTp_recv.return_value = [0x7F, 0x12]

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/Bootloader.odx', 'bootloader')
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __diagnosticSessionControl to diagnosticSessionControl in the uds object, so can now call below

        try:
            b = a.diagnosticSessionControl('Default Session',suppressResponse=False)	# ... calls __diagnosticSessionControl, which does the Uds.send
        except:
            b = traceback.format_exc().split("\n")[-2:-1][0] # ... extract the exception text
        canTp_send.assert_called_with([0x10, 0x01],False)
        self.assertEqual("Exception: Detected negative response: ['0x7f', '0x12']", b)  # ... diagnosticSessionControl should not return a value


    # patches are inserted in reverse order
    @mock.patch('uds.CanTp.recv')
    @mock.patch('uds.CanTp.send')
    def test_diagSessCtrlNegResponse_0x13(self,
                     canTp_send,
                     canTp_recv):

        canTp_send.return_value = False
        canTp_recv.return_value = [0x7F, 0x13]

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/Bootloader.odx', 'bootloader')
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __diagnosticSessionControl to diagnosticSessionControl in the uds object, so can now call below

        try:
            b = a.diagnosticSessionControl('Default Session',suppressResponse=False)	# ... calls __diagnosticSessionControl, which does the Uds.send
        except:
            b = traceback.format_exc().split("\n")[-2:-1][0] # ... extract the exception text
        canTp_send.assert_called_with([0x10, 0x01],False)
        self.assertEqual("Exception: Detected negative response: ['0x7f', '0x13']", b)  # ... diagnosticSessionControl should not return a value


    # patches are inserted in reverse order
    @mock.patch('uds.CanTp.recv')
    @mock.patch('uds.CanTp.send')
    def test_diagSessCtrlNegResponse_0x22(self,
                     canTp_send,
                     canTp_recv):

        canTp_send.return_value = False
        canTp_recv.return_value = [0x7F, 0x22]

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/Bootloader.odx', 'bootloader')
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __diagnosticSessionControl to diagnosticSessionControl in the uds object, so can now call below

        try:
            b = a.diagnosticSessionControl('Default Session',suppressResponse=False)	# ... calls __diagnosticSessionControl, which does the Uds.send
        except:
            b = traceback.format_exc().split("\n")[-2:-1][0] # ... extract the exception text
        canTp_send.assert_called_with([0x10, 0x01],False)
        self.assertEqual("Exception: Detected negative response: ['0x7f', '0x22']", b)  # ... diagnosticSessionControl should not return a value




if __name__ == "__main__":
    unittest.main()