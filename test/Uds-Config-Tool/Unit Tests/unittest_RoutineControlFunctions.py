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
from uds.uds_config_tool.ISOStandard.ISOStandard import IsoRoutineControlType

class ECUResetTestCase(unittest.TestCase):

    # patches are inserted in reverse order
    @mock.patch('uds.CanTp.recv')
    @mock.patch('uds.CanTp.send')
    def test_routineControlRequestDfltNoSuppress(self,
                     canTp_send,
                     canTp_recv):

        canTp_send.return_value = False
        canTp_recv.return_value = [0x71, 0x01, 0xFF, 0x00, 0x30]

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/Bootloader.odx', 'bootloader')
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __routineControl to routineControl in the uds object, so can now call below

        b = a.routineControl('Erase Memory',IsoRoutineControlType.startRoutine,[('memoryAddress',[0x01]),('memorySize',[0xF000])])	# ... calls __routineControl, which does the Uds.send
	
        canTp_send.assert_called_with([0x31, 0x01, 0xFF, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0xF0, 0x00],False)
        self.assertEqual({'Erase Memory Status':[0x30],'RoutineControlType':[0x01],'Identifier':[0xFF, 0x00]}, b) 


    # patches are inserted in reverse order
    @mock.patch('uds.CanTp.recv')
    @mock.patch('uds.CanTp.send')
    def test_routineControlRequestNoSuppress(self,
                     canTp_send,
                     canTp_recv):

        canTp_send.return_value = False
        canTp_recv.return_value = [0x71, 0x01, 0xFF, 0x00, 0x30]

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/Bootloader.odx', 'bootloader')
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __routineControl to routineControl in the uds object, so can now call below

        b = a.routineControl('Erase Memory',IsoRoutineControlType.startRoutine,[('memoryAddress',[0x01]),('memorySize',[0xF000])],suppressResponse=False)	# ... calls __routineControl, which does the Uds.send
	
        canTp_send.assert_called_with([0x31, 0x01, 0xFF, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0xF0, 0x00],False)
        self.assertEqual({'Erase Memory Status':[0x30],'RoutineControlType':[0x01],'Identifier':[0xFF, 0x00]}, b) 

		
    # patches are inserted in reverse order
    @mock.patch('uds.CanTp.send')
    def test_routineControlRequestSuppress(self,
                     canTp_send):

        canTp_send.return_value = False

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/Bootloader.odx', 'bootloader')
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __routineControl to routineControl in the uds object, so can now call below

        b = a.routineControl('Erase Memory',IsoRoutineControlType.startRoutine,[('memoryAddress',[0x01]),('memorySize',[0xF000])],suppressResponse=True)	# ... calls __routineControl, which does the Uds.send
	
        canTp_send.assert_called_with([0x31, 0x81, 0xFF, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0xF0, 0x00],False)
        self.assertEqual(None, b)  # ... routineControl should not return a value


    # patches are inserted in reverse order
    @mock.patch('uds.CanTp.recv')
    @mock.patch('uds.CanTp.send')
    def test_routineControlRequestStop(self,
                     canTp_send,
                     canTp_recv):

        canTp_send.return_value = False
        canTp_recv.return_value = [0x71, 0x02, 0xFF, 0x00]

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/Bootloader.odx', 'bootloader')
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __routineControl to routineControl in the uds object, so can now call below

        b = a.routineControl('Erase Memory',IsoRoutineControlType.stopRoutine)	# ... calls __routineControl, which does the Uds.send
	
        canTp_send.assert_called_with([0x31, 0x02, 0xFF, 0x00],False)
        self.assertEqual({'RoutineControlType':[0x02],'Identifier':[0xFF, 0x00]}, b) 


    # patches are inserted in reverse order
    @mock.patch('uds.CanTp.recv')
    @mock.patch('uds.CanTp.send')
    def test_routineControlRequestRequestResult(self,
                     canTp_send,
                     canTp_recv):

        canTp_send.return_value = False
        canTp_recv.return_value = [0x71, 0x03, 0xFF, 0x00, 0x30]

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/Bootloader.odx', 'bootloader')
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __routineControl to routineControl in the uds object, so can now call below

        b = a.routineControl('Erase Memory',IsoRoutineControlType.requestRoutineResults)	# ... calls __routineControl, which does the Uds.send
	
        canTp_send.assert_called_with([0x31, 0x03, 0xFF, 0x00],False)
        self.assertEqual({'Erase Memory Status':[0x30],'RoutineControlType':[0x03],'Identifier':[0xFF, 0x00]}, b) 


    # patches are inserted in reverse order
    @mock.patch('uds.CanTp.recv')
    @mock.patch('uds.CanTp.send')
    def test_routineControlRequestCheckAppStart(self,
                     canTp_send,
                     canTp_recv):

        canTp_send.return_value = False
        canTp_recv.return_value = [0x71, 0x01, 0x03, 0x04, 0x30, 0x02]

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/Bootloader.odx', 'bootloader')
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __routineControl to routineControl in the uds object, so can now call below

        b = a.routineControl('Check Valid Application',IsoRoutineControlType.startRoutine)	# ... calls __routineControl, which does the Uds.send
        canTp_send.assert_called_with([0x31, 0x01, 0x03, 0x04],False)
        self.assertEqual({'Valid Application Status':[0x30],'Valid Application Present':[0x02],'RoutineControlType':[0x01],'Identifier':[0x03, 0x04]}, b)


    # patches are inserted in reverse order
    @mock.patch('uds.CanTp.recv')
    @mock.patch('uds.CanTp.send')
    def test_routineControlRequestCheckAppStartResult(self,
                     canTp_send,
                     canTp_recv):

        canTp_send.return_value = False
        canTp_recv.return_value = [0x71, 0x03, 0x03, 0x04, 0x30, 0x02]

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/Bootloader.odx', 'bootloader')
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __routineControl to routineControl in the uds object, so can now call below

        b = a.routineControl('Check Valid Application',IsoRoutineControlType.requestRoutineResults)	# ... calls __routineControl, which does the Uds.send
	
        canTp_send.assert_called_with([0x31, 0x03, 0x03, 0x04],False)
        self.assertEqual({'Valid Application Status':[0x30],'Valid Application Present':[0x02],'RoutineControlType':[0x03],'Identifier':[0x03, 0x04]}, b)

	
	
    # patches are inserted in reverse order
    @mock.patch('uds.CanTp.recv')
    @mock.patch('uds.CanTp.send')
    def test_routineControlRequestSBLStart(self,
                     canTp_send,
                     canTp_recv):

        canTp_send.return_value = False
        canTp_recv.return_value = [0x71, 0x01, 0x03, 0x01, 0xA7]

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/Bootloader.odx', 'bootloader')
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __routineControl to routineControl in the uds object, so can now call below

        b = a.routineControl('Start Secondary Bootloader',IsoRoutineControlType.startRoutine,[0xFF])	# ... calls __routineControl, which does the Uds.send
        canTp_send.assert_called_with([0x31, 0x01, 0x03, 0x01, 0x00, 0x00, 0x00, 0xFF],False)
        self.assertEqual({'strSBLRoutineInfo':[0xA7],'RoutineControlType':[0x01],'Identifier':[0x03, 0x01]}, b)



    # patches are inserted in reverse order
    @mock.patch('uds.CanTp.recv')
    @mock.patch('uds.CanTp.send')
    def test_routineControlRequestProgDepStart(self,
                     canTp_send,
                     canTp_recv):

        canTp_send.return_value = False
        canTp_recv.return_value = [0x71, 0x01, 0xFF, 0x01, 0x30, 0xB9, 0x2E]

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/Bootloader.odx', 'bootloader')
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __routineControl to routineControl in the uds object, so can now call below

        b = a.routineControl('Check Programming Dependencies',IsoRoutineControlType.startRoutine,[('memoryAddress',[0x01]),('memorySize',[0xF000])])	# ... calls __routineControl, which does the Uds.send
        canTp_send.assert_called_with([0x31, 0x01, 0xFF, 0x01, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0xF0, 0x00],False)
        self.assertEqual({'RoutineStatusInfo':[0x30],'Check Sum Value':[0xB9, 0x2E],'RoutineControlType':[0x01],'Identifier':[0xFF, 0x01]}, b)


    # patches are inserted in reverse order
    @mock.patch('uds.CanTp.recv')
    @mock.patch('uds.CanTp.send')
    def test_routineControlRequestProgDepResult(self,
                     canTp_send,
                     canTp_recv):

        canTp_send.return_value = False
        canTp_recv.return_value = [0x71, 0x03, 0xFF, 0x01, 0x30, 0xB9, 0x2E]

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/Bootloader.odx', 'bootloader')
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __routineControl to routineControl in the uds object, so can now call below

        b = a.routineControl('Check Programming Dependencies',IsoRoutineControlType.requestRoutineResults)	# ... calls __routineControl, which does the Uds.send
        canTp_send.assert_called_with([0x31, 0x03, 0xFF, 0x01],False)
        self.assertEqual({'RoutineStatusInfo':[0x30],'Check Sum Value':[0xB9, 0x2E],'RoutineControlType':[0x03],'Identifier':[0xFF, 0x01]}, b)



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
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __routineControl to routineControl in the uds object, so can now call below

        try:
            b = a.routineControl('Erase Memory',IsoRoutineControlType.startRoutine,[('memoryAddress',[0x01]),('memorySize',[0xF000])])	# ... calls __routineControl, which does the Uds.send
        except:
            b = traceback.format_exc().split("\n")[-2:-1][0] # ... extract the exception text
        canTp_send.assert_called_with([0x31, 0x01, 0xFF, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0xF0, 0x00],False)
        self.assertEqual("Exception: Detected negative response: ['0x7f', '0x12']", b)

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
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __routineControl to routineControl in the uds object, so can now call below

        try:
            b = a.routineControl('Erase Memory',IsoRoutineControlType.startRoutine,[('memoryAddress',[0x01]),('memorySize',[0xF000])])	# ... calls __routineControl, which does the Uds.send
        except:
            b = traceback.format_exc().split("\n")[-2:-1][0] # ... extract the exception text
        canTp_send.assert_called_with([0x31, 0x01, 0xFF, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0xF0, 0x00],False)
        self.assertEqual("Exception: Detected negative response: ['0x7f', '0x13']", b)


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
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __routineControl to routineControl in the uds object, so can now call below

        try:
            b = a.routineControl('Erase Memory',IsoRoutineControlType.startRoutine,[('memoryAddress',[0x01]),('memorySize',[0xF000])])	# ... calls __routineControl, which does the Uds.send
        except:
            b = traceback.format_exc().split("\n")[-2:-1][0] # ... extract the exception text
        canTp_send.assert_called_with([0x31, 0x01, 0xFF, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0xF0, 0x00],False)
        self.assertEqual("Exception: Detected negative response: ['0x7f', '0x22']", b)


    # patches are inserted in reverse order
    @mock.patch('uds.CanTp.recv')
    @mock.patch('uds.CanTp.send')
    def test_ecuResetNegResponse_0x24(self,
                     canTp_send,
                     canTp_recv):

        canTp_send.return_value = False
        canTp_recv.return_value = [0x7F, 0x24]

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/Bootloader.odx', 'bootloader')
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __routineControl to routineControl in the uds object, so can now call below

        try:
            b = a.routineControl('Erase Memory',IsoRoutineControlType.startRoutine,[('memoryAddress',[0x01]),('memorySize',[0xF000])])	# ... calls __routineControl, which does the Uds.send
        except:
            b = traceback.format_exc().split("\n")[-2:-1][0] # ... extract the exception text
        canTp_send.assert_called_with([0x31, 0x01, 0xFF, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0xF0, 0x00],False)
        self.assertEqual("Exception: Detected negative response: ['0x7f', '0x24']", b)



    # patches are inserted in reverse order
    @mock.patch('uds.CanTp.recv')
    @mock.patch('uds.CanTp.send')
    def test_ecuResetNegResponse_0x31(self,
                     canTp_send,
                     canTp_recv):

        canTp_send.return_value = False
        canTp_recv.return_value = [0x7F, 0x31]

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/Bootloader.odx', 'bootloader')
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __routineControl to routineControl in the uds object, so can now call below

        try:
            b = a.routineControl('Erase Memory',IsoRoutineControlType.startRoutine,[('memoryAddress',[0x01]),('memorySize',[0xF000])])	# ... calls __routineControl, which does the Uds.send
        except:
            b = traceback.format_exc().split("\n")[-2:-1][0] # ... extract the exception text
        canTp_send.assert_called_with([0x31, 0x01, 0xFF, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0xF0, 0x00],False)
        self.assertEqual("Exception: Detected negative response: ['0x7f', '0x31']", b)


    # patches are inserted in reverse order
    @mock.patch('uds.CanTp.recv')
    @mock.patch('uds.CanTp.send')
    def test_ecuResetNegResponse_0x33(self,
                     canTp_send,
                     canTp_recv):

        canTp_send.return_value = False
        canTp_recv.return_value = [0x7F, 0x33]

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/Bootloader.odx', 'bootloader')
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __routineControl to routineControl in the uds object, so can now call below

        try:
            b = a.routineControl('Erase Memory',IsoRoutineControlType.startRoutine,[('memoryAddress',[0x01]),('memorySize',[0xF000])])	# ... calls __routineControl, which does the Uds.send
        except:
            b = traceback.format_exc().split("\n")[-2:-1][0] # ... extract the exception text
        canTp_send.assert_called_with([0x31, 0x01, 0xFF, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0xF0, 0x00],False)
        self.assertEqual("Exception: Detected negative response: ['0x7f', '0x33']", b)


    # patches are inserted in reverse order
    @mock.patch('uds.CanTp.recv')
    @mock.patch('uds.CanTp.send')
    def test_ecuResetNegResponse_0x72(self,
                     canTp_send,
                     canTp_recv):

        canTp_send.return_value = False
        canTp_recv.return_value = [0x7F, 0x72]

        # Parameters: xml file (odx file), ecu name (not currently used) ...
        a = createUdsConnection('../Functional Tests/Bootloader.odx', 'bootloader')
        # ... creates the uds object and returns it; also parses out the rdbi info and attaches the __routineControl to routineControl in the uds object, so can now call below

        try:
            b = a.routineControl('Erase Memory',IsoRoutineControlType.startRoutine,[('memoryAddress',[0x01]),('memorySize',[0xF000])])	# ... calls __routineControl, which does the Uds.send
        except:
            b = traceback.format_exc().split("\n")[-2:-1][0] # ... extract the exception text
        canTp_send.assert_called_with([0x31, 0x01, 0xFF, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0xF0, 0x00],False)
        self.assertEqual("Exception: Detected negative response: ['0x7f', '0x72']", b)





if __name__ == "__main__":
    unittest.main()