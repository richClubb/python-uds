=========
Interface
=========

The Uds object allows for raw sending of Uds Payloads with no checking on the validity of the returned value.

The createUdsConnection method creates a Uds object but also creates a series of methods providing access to the services defined in the associated ODX file.

Uds Raw Communication
---------------------

Using the raw send command is very simple:

::

   PCM = Uds(transportProtocol="can", reqId=0x7E0, resId=0x7E8)
   a = PCM.send([0x22, 0xF1, 0x8C])

This will set up a connection to PCM (Typically Powertrain Control Module, also called an ECM in some companies) with the given parameters, and request the ECU Serial Number (As defined in the ISO-14229 standard, 0x22 is read data by identifier service, and the did 0xF18C is the ECU Serial Number DID)

For a correct response, "a" will be of the format:

::

   [0x62, 0xf1, 0x8C, 0xXX, 0xXX ..... ] 
   
depending on how long the serial number is (this is not defined in the standard)

For a negative response "a" will be of the format:
   
::

   [0x7F, 0x22, 0xXX]

Where 0xXX will be the response code.

Using the createUdsConnection method
------------------------------------

UDS is a simple enough protocol, but it relies on using a lot of magic numbers and these can change from manufacturer to manufacturer. There are some standardised DIDs, but most are specific to both the manufacturer and the model, and even the model year.

the createUdsConnection method provides the ability to parse an ODX file which defines the diagnostic interface into a more human readable format.

::

   bootloader = createUdsConnection("Bootloader.odx", "", transportProtocol="can", reqId=0x600, resId=0x650)
   a = bootloader.readDataByIdentifier("ECU Serial Number")
   
For a positive response, a will be of the format "0000000000000000" which is an encoded form of the Serial number rather than a raw array of bytes. This is because the ODX definition for ECU serial number is coded as an ASCII string of 16 bytes.

It is still possible to interface with the bootloader instance using the .send method to send raw packets, but it loses the benefits of encoding the request and response
