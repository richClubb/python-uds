Interface
---------

These keywords can be used to configure the other object instances

Uds

- P2_CAN_Server (DEFAULT: 1)
- P2_CAN_Client (DEFAULT: 1)
- transportProtocol (DEFAULT: CAN) Currently CAN is the only supported transport protocol

CanTp

- reqId (DEFAULT: 0x600) This is just a default ID used by the author
- resId (DEFAULT: 0x650) This is just a default ID used by the author
- N_SA (DEFAULT: 0xFF) This is currently NOT SUPPORTED
- N_TA (DEFAULT: 0xFF) This is currently NOT SUPPORTED
- N_AE (DEFAULT: 0xFF) This is currently NOT SUPPORTED
- Mtype (DEFAULT: DIAGNOSTICS)

Can Interface

- interface (DEFAULT: virtual)
- baudrate (DEFAULT: 500000)

Peak

- device (DEFAULT: PCAN_USBBUS1)

Vector

- appName (DEFAULT: testApp) This is done so that a vector software licence is not required, but this does
  require some setup in the vector hardware interface
- channel (DEFAULT: 0) The channel configured for communications

Virtual

- interfaceName (DEFAULT: )(Currently STATIC)