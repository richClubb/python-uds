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
from time import sleep


class TesterPresentTestCase(unittest.TestCase):

    # patches are inserted in reverse order
    @mock.patch('uds.TestTp.recv')
    @mock.patch('uds.TestTp.send')
    def test_testerPresentRequestDfltNoSuppress(self,
                     tp_send,
                     tp_recv):

        tp_send.return_value = False
        #tp_recv.return_value = [0x7E, 0x00]

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/Bootloader.odx', 'bootloader', transportProtocol="TEST")
        # ... creates the uds object and returns it; also parses out the testerPresent info and attaches the __testerPresent to testerPresent in the uds object, so can now call below

        b = a.testerPresent()	# ... calls __testerPresent, which does the Uds.send
	
        tp_send.assert_called_with([0x3E, 0x80],False)
        self.assertEqual(None, b)  # ... testerPresent should not return a value


    # patches are inserted in reverse order
    @mock.patch('uds.TestTp.recv')
    @mock.patch('uds.TestTp.send')
    def test_testerPresentRequestNoSuppress(self,
                     tp_send,
                     tp_recv):

        tp_send.return_value = False
        tp_recv.return_value = [0x7E, 0x00]

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/Bootloader.odx', 'bootloader', transportProtocol="TEST")
        # ... creates the uds object and returns it; also parses out the testerPresent info and attaches the __testerPresent to testerPresent in the uds object, so can now call below

        b = a.testerPresent(suppressResponse=False)	# ... calls __testerPresent, which does the Uds.send
	
        tp_send.assert_called_with([0x3E, 0x00],False)
        self.assertEqual({}, b)  # ... testerPresent should not return a value


    # patches are inserted in reverse order
    @mock.patch('uds.TestTp.send')
    def test_testerPresentRequestSuppress(self,
                     tp_send):

        tp_send.return_value = False

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/Bootloader.odx', 'bootloader', transportProtocol="TEST")
        # ... creates the uds object and returns it; also parses out the testerPresent info and attaches the __testerPresent to testerPresent in the uds object, so can now call below

        b = a.testerPresent(suppressResponse=True)	# ... calls __testerPresent, which does the Uds.send
	
        tp_send.assert_called_with([0x3E, 0x80],False)
        self.assertEqual(None, b)  # ... testerPresent should not return a value


    # patches are inserted in reverse order
    @mock.patch('uds.TestTp.recv')
    @mock.patch('uds.TestTp.send')
    def test_ecuResetNegResponse_0x12(self,
                     tp_send,
                     tp_recv):

        tp_send.return_value = False
        tp_recv.return_value = [0x7F, 0x12]

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/Bootloader.odx', 'bootloader', transportProtocol="TEST")
        # ... creates the uds object and returns it; also parses out the testerPresent info and attaches the __testerPresent to testerPresent in the uds object, so can now call below

        try:
            b = a.testerPresent(suppressResponse=False)	# ... calls __testerPresent, which does the Uds.send
        except:
            b = traceback.format_exc().split("\n")[-2:-1][0] # ... extract the exception text
        tp_send.assert_called_with([0x3E, 0x00],False)
        self.assertEqual("Exception: Detected negative response: ['0x7f', '0x12']", b)


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
        # ... creates the uds object and returns it; also parses out the testerPresent info and attaches the __testerPresent to testerPresent in the uds object, so can now call below

        try:
            b = a.testerPresent(suppressResponse=False)	# ... calls __testerPresent, which does the Uds.send
        except:
            b = traceback.format_exc().split("\n")[-2:-1][0] # ... extract the exception text
        tp_send.assert_called_with([0x3E, 0x00],False)
        self.assertEqual("Exception: Detected negative response: ['0x7f', '0x13']", b)


    # patches are inserted in reverse order
    @mock.patch('uds.CanTp.recv')
    @mock.patch('uds.CanTp.send')
    def test_testerPresentNotReqd(self,
                     canTp_send,
                     canTp_recv):

        canTp_send.return_value = False
        canTp_recv.return_value = [0x50, 0x01, 0x00, 0x05, 0x00, 0x0A] # ... can return 1 to N bytes in the sessionParameterRecord - looking into this one

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/Bootloader.odx', 'bootloader')
        # ... creates the uds object and returns it; also parses out the testerPresent info and attaches the __diagnosticSessionControl to diagnosticSessionControl in the uds object, so can now call below

        b = a.diagnosticSessionControl('Default Session')	# ... calls __diagnosticSessionControl, which does the Uds.send
        canTp_send.assert_called_with([0x10, 0x01],False)
        self.assertEqual({'Type':[0x01], 'P3':[0x00, 0x05], 'P3Ex':[0x00, 0x0A]}, b)  # ... diagnosticSessionControl should not return a value
        b = a.testerPresentSessionRecord()
        self.assertEqual({'reqd':False, 'timeout':None}, b)  # ... diagnosticSessionControl should not return a value


    # patches are inserted in reverse order
    @mock.patch('uds.CanTp.recv')
    @mock.patch('uds.CanTp.send')
    def test_testerPresentReqdDfltTO(self,
                     canTp_send,
                     canTp_recv):

        canTp_send.return_value = False
        canTp_recv.return_value = [0x50, 0x01, 0x00, 0x05, 0x00, 0x0A] # ... can return 1 to N bytes in the sessionParameterRecord - looking into this one

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/Bootloader.odx', 'bootloader')
        # ... creates the uds object and returns it; also parses out the testerPresent info and attaches the __diagnosticSessionControl to diagnosticSessionControl in the uds object, so can now call below

        b = a.diagnosticSessionControl('Default Session',testerPresent=True)	# ... calls __diagnosticSessionControl, which does the Uds.send
        canTp_send.assert_called_with([0x10, 0x01],False)
        self.assertEqual({'Type':[0x01], 'P3':[0x00, 0x05], 'P3Ex':[0x00, 0x0A]}, b)  # ... diagnosticSessionControl should not return a value
        b = a.testerPresentSessionRecord()
        self.assertEqual({'reqd':True, 'timeout':10}, b)  # ... diagnosticSessionControl should not return a value


    # patches are inserted in reverse order
    @mock.patch('uds.CanTp.recv')
    @mock.patch('uds.CanTp.send')
    def test_testerPresentReqdUpdatedTO(self,
                     canTp_send,
                     canTp_recv):

        canTp_send.return_value = False
        canTp_recv.return_value = [0x50, 0x01, 0x00, 0x05, 0x00, 0x0A] # ... can return 1 to N bytes in the sessionParameterRecord - looking into this one

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/Bootloader.odx', 'bootloader')
        # ... creates the uds object and returns it; also parses out the testerPresent info and attaches the __diagnosticSessionControl to diagnosticSessionControl in the uds object, so can now call below

        b = a.diagnosticSessionControl('Default Session',testerPresent=True,tpTimeout=250)	# ... calls __diagnosticSessionControl, which does the Uds.send
        canTp_send.assert_called_with([0x10, 0x01],False)
        self.assertEqual({'Type':[0x01], 'P3':[0x00, 0x05], 'P3Ex':[0x00, 0x0A]}, b)  # ... diagnosticSessionControl should not return a value
        b = a.testerPresentSessionRecord()
        self.assertEqual({'reqd':True, 'timeout':250}, b)  # ... diagnosticSessionControl should not return a value


    # patches are inserted in reverse order
    @mock.patch('uds.CanTp.recv')
    @mock.patch('uds.CanTp.send')
    def test_testerPresentSessionSwitching(self,
                     canTp_send,
                     canTp_recv):

        canTp_send.return_value = False

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/Bootloader.odx', 'bootloader')
        # ... creates the uds object and returns it; also parses out the testerPresent info and attaches the __diagnosticSessionControl to diagnosticSessionControl in the uds object, so can now call below

        # Confirm initial default session with no tester present handling ...
        canTp_recv.return_value = [0x50, 0x01, 0x00, 0x05, 0x00, 0x0A] # ... can return 1 to N bytes in the sessionParameterRecord - looking into this one
        b = a.diagnosticSessionControl('Default Session')	# ... calls __diagnosticSessionControl, which does the Uds.send
        canTp_send.assert_called_with([0x10, 0x01],False)
        self.assertEqual({'Type':[0x01], 'P3':[0x00, 0x05], 'P3Ex':[0x00, 0x0A]}, b)  # ... diagnosticSessionControl should not return a value
        b = a.testerPresentSessionRecord()
        self.assertEqual({'reqd':False, 'timeout':None}, b)  # ... diagnosticSessionControl should not return a value

        # Create a non-default session with tester present, and confirm the case ...
        canTp_recv.return_value = [0x50, 0x02, 0x00, 0x06, 0x00, 0x09] # ... can return 1 to N bytes in the sessionParameterRecord - looking into this one
        b = a.diagnosticSessionControl('Programming Session',testerPresent=True)	# ... calls __diagnosticSessionControl, which does the Uds.send
        canTp_send.assert_called_with([0x10, 0x02],False)
        self.assertEqual({'Type':[0x02], 'P3':[0x00, 0x06], 'P3Ex':[0x00, 0x09]}, b)  # ... diagnosticSessionControl should not return a value
        # Check that session record for tester present is set up correctly ...
        b = a.testerPresentSessionRecord()
        self.assertEqual({'reqd':True, 'timeout':10}, b)  # ... diagnosticSessionControl should not return a value

        # Check the time evaluation since the last message send is of the correct order ...
        t1 = a.sessionTimeSinceLastSend()
        #print(("time since last send (1)",b))
        sleep(1.0)
        t2 = a.sessionTimeSinceLastSend()
        #print(("time since last send (1)",b))
        self.assertEqual((t1 >= 0 and t1 < 0.1), True)
        self.assertEqual((t2 >= 1 and t1 < 1.1), True)
        #sleep(20.0)  # ... this was used for manual testing of "automated" testerPresent sending (required the above two asserts to be commented out, and the other tests as well as they add unwanted targets to the threads target list)
        # Note: the manual test for automated repeat sending worked ok.

        # Confirm that tester present disablling operates correctly ...
        a.testerPresent(disable=True)
        b = a.testerPresentSessionRecord()
        self.assertEqual({'reqd':False, 'timeout':None}, b)  # ... diagnosticSessionControl should not return a value

        # Return to the default session, and ensure that tester present handling is still off ...
        canTp_recv.return_value = [0x50, 0x01, 0x00, 0x05, 0x00, 0x0A] # ... can return 1 to N bytes in the sessionParameterRecord - looking into this one
        b = a.diagnosticSessionControl('Default Session')	# ... calls __diagnosticSessionControl, which does the Uds.send
        canTp_send.assert_called_with([0x10, 0x01],False)
        self.assertEqual({'Type':[0x01], 'P3':[0x00, 0x05], 'P3Ex':[0x00, 0x0A]}, b)  # ... diagnosticSessionControl should not return a value
        b = a.testerPresentSessionRecord()
        self.assertEqual({'reqd':False, 'timeout':None}, b)  # ... diagnosticSessionControl should not return a value



if __name__ == "__main__":
    unittest.main()