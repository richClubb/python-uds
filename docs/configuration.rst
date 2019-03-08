=============
Configuration
=============

Currently the objects have the following hierarchy.

::

  Uds -> Tp -> Device

For CAN this would be

::

  Uds -> CanTp -> CanInterface

Each class has its own config file which includes parameters relevant to that scope,
however these can be passed "down the chain" from an upper level object to initialise
the lower level classes.

E.g.

- Uds() will use the default values as defined in the local config.ini
- Uds(reqId=0x600, resId=0x650, interface="peak", baudrate=500000) would initialse a connection
  using Request Id of 0x600, Response Id of 0x650 using the peak interface and a baudrate of 500 kbps

Keyword Arguments
-----------------
To configure a UDS connection instance the kwargs are passed down to each called object down the chain. The configuration can be passed down either by a config file, or by manually typing the keyword into the function call. The precidence is as follows:

- Default Config
- Config File
- Keyword argument

The following sections detail the different keywords for each class.

Uds
---
These keywords are used to configure the UDS instance:

- P2_CAN_Server (DEFAULT: 1)
- P2_CAN_Client (DEFAULT: 1)
- transportProtocol (DEFAULT: CAN) Currently CAN is the only supported transport protocol

CanTp
-----
These keywords are used to configure the CAN Transport Protocol Instance (ISO 14229):

- addressingType (DEFAULT: NORMAL)
- reqId (DEFAULT: 0x600) This is just a default ID used by the author
- resId (DEFAULT: 0x650) This is just a default ID used by the author
- N_SA (DEFAULT: 0xFF) This is currently NOT SUPPORTED
- N_TA (DEFAULT: 0xFF) This is currently NOT SUPPORTED
- N_AE (DEFAULT: 0xFF) This is currently NOT SUPPORTED
- Mtype (DEFAULT: DIAGNOSTICS)

LinTp
-----
These keywords are used to configure the CAN Transport Protocol Instance:

- nodeAddress (DEFAULT: 1)
- STMin (DEFAULT: 0.001)


Can Interface
-------------
These keywords are used to configure the CAN interface:

- interface (DEFAULT: virtual)
- baudrate (DEFAULT: 500000)

Peak
----
These keywords are specific to PEAK devices and bus configuration:

- device (DEFAULT: PCAN_USBBUS1)

Vector
------
These keywords are specific to Vector devices and bus configuration:

- appName (DEFAULT: testApp) This is done so that a vector software licence is not required, but this does
  require some setup in the vector hardware interface
- channel (DEFAULT: 0) The channel configured for communications

Virtual
-------
These keywords are specific to the python-can virtual loopback interface:

- interfaceName (DEFAULT: virtualInterface) This needs to be the same attempting to interface using the loopback interface with Python-CAN.
