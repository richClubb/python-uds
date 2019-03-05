========
Services
========

This section contains a list of all the currently supported services and their interfaces

An example ODX file is available which supports at least one instance of each of these services. This has been tested against an Embed E400 using their embedded UDS stack.

Diagnostic Session Control (0x10 Service)
-----------------------------------------
This service is used to switch between the defined sessions. Usually most ECUs support Default, Programming, Extended and Service.


ECU Reset (0x11 Service)
-------------------------
This service is used to perform software resets. Usually most ECUs support Soft, Hard, and Reset to Bootloader


Read Data By Identifier (0x22 Service)
--------------------------------------
This service is used to read data from the ECU for detailed diagnostics. E.g. Engine Speed, actuator position, coolant temperature. It varies significantly from manufacturer to manufacturer and also from the supplier of the ECU.


Write Data By Identifier (0x2E Service)
---------------------------------------
This service is used to configure ECU parameters. 
