from uds import Uds

if __name__ == "__main__":

    a = Uds(reqId=0x7E0, resId=0x7E8, interface="peak", device="PCAN_USBBUS1")

    ## transmit a standard tester present
    TesterPresent = a.send([0x3E, 0x00])
    print(TesterPresent)  # This should be [0x7E, 0x00]

    ## transmit a request for ECU Serial Number
    SerialNumber = a.send([0x22, 0xF1, 0x8C])
    print(SerialNumber) # this will vary depending on the ECU, but should start with [0x6E, 0xF1, 0x8C]
