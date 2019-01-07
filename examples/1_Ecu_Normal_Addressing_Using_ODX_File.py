from uds import createUdsConnection

if __name__ == "__main__":

    a = createUdsConnection("Diagnostics.odx-d", "", reqId=0x7E0, resId=0x7E8, interface="peak", device="PCAN_USBBUS1")

    SerialNumber = a.readDataByIdentifier("ECU Serial Number")
    print(SerialNumber) # This should print the decoded serial number in the case of the E400 will be "000000000098" or similar

