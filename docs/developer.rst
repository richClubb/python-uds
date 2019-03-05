====================
Developer's Overview
====================

The code is separated into three main areas:
 - Uds Communications - This is the main communications interface for the system
 - Uds Config Tool - This is the ODX parser and service configuration system
 - Uds Configuration - This is to do with the config set for each of the components and passing configurations around the code
 
 
Uds Communications
------------------
This sub-module contains all the code related to the communications interface, it includes the Transport Protocol code for CanTp and LinTp


Uds Config Tool
---------------
This contains the ODX parser code to create the methods which attach to the UDS instance.

 
Uds Configuration
-----------------
Primarily this is a utility for the rest of the code to unify how the system passes configuration items around. 

The intention is also to extend this to provide logging functionality,
