#!/usr/bin/env python

"""
This file provides an example of the different stages of the uds communication flow.
Its intention is to describe how the auto-coder would produce the code for the system

It is not intended as a piece of usable code
"""


__author__ = "Richard Clubb"
__copyrights__ = "Copyright 2018, the python-uds project"
__credits__ = ["Richard Clubb"]

__license__ = "MIT"
__maintainer__ = "Richard Clubb"
__email__ = "richard.clubb@embeduk.com"
__status__ = "Development"


from uds import DecodeFunctions


def check_Boot_Software_Identification_Read(payload):

    expectedLength = 28

    if(len(payload) != expectedLength):
        raise Exception("Unexpected length of response: Received length: " + str(len(payload)) + " Payload: " + str(payload) )

    positiveResponse = 0x62
    negativeResponse = 0x7F

    responseReceived = payload[0]

    if(responseReceived == positiveResponse):
        diagnosticIdentifier_expected = 0xF180
        diagnosticIdentifier_received = DecodeFunctions.buildIntFromList(payload[1:3])

        if(diagnosticIdentifier_expected != diagnosticIdentifier_received):
            raise Exception("Diagnostic identifier does not match expected response: Payload: " + str(payload))

        return None
    elif(responseReceived == negativeResponse):
        # needs improvement to define the exact negative response received
        raise Exception("Negative response received: Payload: " + str(payload))
    else:
        raise Exception("Unexpected response: Payload: " + str(payload))


def decode_Boot_Software_Identification_Read(payload):

    #check the response
    check_Boot_Software_Identification_Read(payload)

    # dynamic
    numberOfModules = payload[3:4]
    Boot_Software_Identification = payload[4:28]

    result = {}
    result['numberOfModules'] = numberOfModules[0]
    result['Boot Software Identification'] = DecodeFunctions.intListToString(Boot_Software_Identification, 'ISO-8859-1')

    return result


if __name__ == "__main__":

    testVal_correct = [0x62, 0xf1, 0x80, 0x03, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30,
                       0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x37]

    response = decode_Boot_Software_Identification_Read(testVal_correct)

    [print(i, response[i]) for i in response]
