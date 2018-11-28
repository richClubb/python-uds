Configuration
-------------

Currently the objects have the following hierarchy.

Uds -> Tp -> Device

For CAN this would be

Uds -> CanTp -> CanInterface

Each class has its own config file which includes parameters relevant to that scope,
however these can be passed "down the chain" from an upper level object to initialise
the lower level classes.

E.g.

- Uds() will use the default values as defined in the local config.ini
- Uds(reqId=0x600, resId=0x650, interface="peak", baudrate=500000) would initialse a connection
  using Request Id of 0x600, Response Id of 0x650 using the peak interface and a baudrate of 500 kbps

