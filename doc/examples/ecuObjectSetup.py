import uds
from uds import Uds

if __name__ == "__main__":

    # Using the ODX file to create the Uds object
    ECU = uds.createUdsConnection('Bootloader.odx', '')

    # This will send a Read Data By Identifier service request for the DID defined as ECU Serial Number (0xF18C)
    esn = ECU.readDataByIdentifier("ECU Serial Number")

    # This prints the decoded ASCII string as it is defined in the Bootloader.odx file
    print(esn)

    # This creates a Uds object but does not create any of the service methods
    plainECU = Uds(redId=0x7E0, resId=0x7E8)

    # This sends a Read Data By Identifier request but using the raw DID, but is still getting the ECU Serial Number
    a = plainECU.send([0x22, 0xF1, 0x8C])

    # This prints the raw returned byte payload from the request
    print(a)
