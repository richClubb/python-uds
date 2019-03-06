========
Examples
========

Example 1 - Simple Peak
----------------

This example sets up the connection using CAN with the Peak-USB Interface. This is using an E400 with the standard Embed bootloader which supports ISO-14229 UDS. The serial number of the ECU is an ASCII encoded string, in this case "0000000000000001".

::

    E400 = Uds(resId=0x600, reqId=0x650, transportProtocol="can", interface="peak", device="PCAN_USBBUS1")
    try:
        response = E400.send([0x22, 0xF1, 0x8C]) # gets the entire response from the ECU
    except:
        print("Send did not complete")
    if(serialNumberArary[0] = 0x7F):
        print("Negative response")
    else:
        serialNumberArray = response[3:] # cuts the response down to just the serial number
        serialNumberString = "" # initialises the string
        for i in serialNumberArray: serialNumberString += chr(i) # Iterates over each element and converts the array element into an ASCII string
        print(serialNumberString) # prints the ASCII string

As the send function can produce exceptions this needs to be checked before continuing. After this it needs to check for a negative response and then can begin decoding the response.

Example 2 - Simple Vector
----------------

This example sets up the connection using CAN with the Vector Interface. This is similar to example 1 so it only includes the initialisation.

It assumes that the Vector hardware has been set up with the application name "pythonUds", this bypasses the licencing for a particular software suite (CANalyser, CANoe. etc)

::

    E400 = Uds(resId=0x600, reqId=0x650, transportProtocol="can", interface="vector", appName="pythonUds", channel=0)

Once this is initialised then the communication with the ECU is the same as Example 1

Example 3 - Simple LIN using Peak-USB Pro
-----------------------------------------

This example sets up a connection over LIN

::

    LightModule = Uds(nodeAddress=0x10, transportProtocol="LIN")

Once this is initialised then the communication with the ECU is the same as Example 1

Example 4 - Using the ODX Parser
--------------------------------

CAN using Peak Interface with Bootloader Example ODX file



Example 5 - Using the ODX Parser
--------------------------------

CAN using Peak Interface with Bootloader Example ODX file

Programming Sequence 1
----------------------

This sequence is part of the standard programming sequence for an ECU over CAN. It includes a dummy seed-key exchange
