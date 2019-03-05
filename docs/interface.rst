Interface
---------

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   uds
   tpFactory
   canTp
   can

   
Keyword Arguments
-----------------
To configure a UDS connection instance the kwargs are passed down to each called object down the chain. The configuration can be passed down either by a config file, or by manually typing the keyword into the function call. The precidence is as follows:
Default Config
Config File
Keyword argument

These keywords can be used to configure the other object instances

Uds
These keywords are used to configure the UDS instance
- P2_CAN_Server (DEFAULT: 1)
- P2_CAN_Client (DEFAULT: 1)
- transportProtocol (DEFAULT: CAN) Currently CAN is the only supported transport protocol

CanTp
These keywords are used to configure the CAN Transport Protocol Instance (ISO 14229)
- reqId (DEFAULT: 0x600) This is just a default ID used by the author
- resId (DEFAULT: 0x650) This is just a default ID used by the author
- N_SA (DEFAULT: 0xFF) This is currently NOT SUPPORTED
- N_TA (DEFAULT: 0xFF) This is currently NOT SUPPORTED
- N_AE (DEFAULT: 0xFF) This is currently NOT SUPPORTED
- Mtype (DEFAULT: DIAGNOSTICS)

LinTp
These keywords are used to configure the CAN Transport Protocol Instance 
- nodeAddress (DEFAULT: 1)


Can Interface
These keywords are used to configure the CAN interface
- interface (DEFAULT: virtual)
- baudrate (DEFAULT: 500000)

Peak
These keywords are specific to PEAK devices and bus configuration
- device (DEFAULT: PCAN_USBBUS1)

Vector
These keywords are specific to Vector devices and bus configuration
- appName (DEFAULT: testApp) This is done so that a vector software licence is not required, but this does
  require some setup in the vector hardware interface
- channel (DEFAULT: 0) The channel configured for communications

Virtual
These keywords are specific to the python-can virtual loopback interface
- interfaceName (DEFAULT: )(Currently STATIC)

