========
Services
========

This section contains a list of all the currently supported services and their interfaces.

An example ODX file is available which supports at least one instance of each of these services. This has been tested against an Embed E400 using their embedded UDS stack.

Tester Present (0x3E Service)
-----------------------------
This service is used to send a heartbeat message to the ECU to keep it in a particular mode of operation. Some ECUs have timeouts on the lengh of time a session or security level is valid for after a request.

Diagnostic Session Control (0x10 Service)
-----------------------------------------
This service is used to switch between the defined sessions. Usually most ECUs support Default, Programming, Extended and Service.

ECU Reset (0x11 Service)
-------------------------
This service is used to perform software resets. Usually most ECUs support Soft, Hard, and Reset to Bootloader.

Security Access (0x27 Service)
------------------------------
This service is used to pass security seed / key messages between the tester and ECU.

Read Data By Identifier (0x22 Service)
--------------------------------------
This service is used to read data from the ECU for detailed diagnostics. E.g. Engine Speed, actuator position, coolant temperature. It varies significantly from manufacturer to manufacturer and also from the supplier of the ECU.

Write Data By Identifier (0x2E Service)
---------------------------------------
This service is used to configure ECU parameters. 

I/O Control (0x2F Service)
--------------------------
This service is used to perform temporary overrides for values in the ECU.

Routine Control (0x31 Service)
------------------------------
This service is used to perform set operations or sequences.

Request Download ()
-------------------
This service is used to set up a transfer of data to the ECU, usually for re-flashing or calibration sets.

Request Upload()
----------------
NOTE: Currently this is not tested

This service is used to transfer data from the ECU, sometimes to download calibration sets or ROM images.

Transfer Data()
----------------
This service is used to set up a transfer data to the ECU, usually for re-flashing or calibration sets.

Transfer Exit()
---------------
This service is used to signify the end of a transfer data block.

Clear DTC ()
------------
This service is used to clear DTC codes from the ECU memory.

Read DTC ()
-----------
This service is used to Read DTC information from the ECU.

To-do: 

- Decode the DTC information
- snapshots
