#!/usr/bin/env python

__author__ = "Richard Clubb"
__copyrights__ = "Copyright 2018, the python-uds project"
__credits__ = ["Richard Clubb"]

__license__ = "MIT"
__maintainer__ = "Richard Clubb"
__email__ = "richard.clubb@embeduk.com"
__status__ = "Development"


from uds.uds_config_tool import DecodeFunctions
import sys
from uds.uds_config_tool.FunctionCreation.iServiceMethodFactory import IServiceMethodFactory


requestFuncTemplate = str("def {0}(suppressResponse=False):\n"
                          "    zeroSubFunction = [0x80] if suppressResponse else [0x00]\n"
                          "    return {1} + zeroSubFunction")									 

# Note: we do not need to cater for response suppression checking as nothing to check if response is suppressed - always unsuppressed
checkFunctionTemplate = str("def {0}(input):\n"
                            "    # The tester present response is simple and fixed, so hardcoding here for simplicity.\n"
                            "    serviceId = DecodeFunctions.buildIntFromList(input[0:1])\n"
                            "    zeroSubFunction = DecodeFunctions.buildIntFromList(input[1:2])\n"
                            "    if(len(input) != 2): raise Exception(\"Total length returned not as expected. Expected: 2; Got {{0}}\".format(len(input)))\n"
                            "    if(serviceId != 0x7E): raise Exception(\"Service Id Received not expected. Expected {{0}}; Got {{1}} \".format(0x7E,serviceId))\n"
                            "    if(zeroSubFunction != 0x00): raise Exception(\"Zero Sub Function Received not as expected. Expected {{0}}; Got {{1}}\".format(0x00,zeroSubFunction))")

negativeResponseFuncTemplate = str("def {0}(input):\n"
                                   "    {1}")

# Note: we do not need to cater for response suppression checking as nothing to check if response is suppressed - always unsuppressed.
# For tester present there is no response data to return, so hardcoding an empty response.
encodePositiveResponseFuncTemplate = str("def {0}(input):\n"
                                         "    return {{}}")


class TesterPresentMethodFactory(IServiceMethodFactory):

    ##
    # @brief method to create the request function for the service element
    @staticmethod
    def create_requestFunction(diagServiceElement, xmlElements):
        # Some services are present in the ODX in both response and send only versions (with the same short name, so one will overwrite the other).
        # Avoiding the overwrite by ignoring the send-only versions, i.e. these are identical other than postivie response details being missing.
        try:
            if diagServiceElement.attrib['TRANSMISSION-MODE'] == 'SEND-ONLY':
                return None
        except:
            pass

        serviceId = 0
        resetType = 0

        shortName = "request_{0}".format(diagServiceElement.find('SHORT-NAME').text)
        requestElement = xmlElements[diagServiceElement.find('REQUEST-REF').attrib['ID-REF']]
        paramsElement = requestElement.find('PARAMS')

        encodeFunctions = []
        encodeFunction = "None"

        for param in paramsElement:
            semantic = None
            try:
                semantic = param.attrib['SEMANTIC']
            except AttributeError:
                pass

            if(semantic == 'SERVICE-ID'):
                serviceId = [int(param.find('CODED-VALUE').text)]

        funcString = requestFuncTemplate.format(shortName,
                                                serviceId)
        exec(funcString)
        return locals()[shortName]

    ##
    # @brief method to create the function to check the positive response for validity
    # Note: the response for tester present is simplistic, so the details have been hardcoded;
    # this function is really just checking that the service is supported before creating the 
    # the hardcoded check function.
    @staticmethod
    def create_checkPositiveResponseFunction(diagServiceElement, xmlElements):
        # Some services are present in the ODX in both response and send only versions (with the same short name, so one will overwrite the other).
        # Avoiding the overwrite by ignoring the send-only versions, i.e. these are identical other than positive response details being missing.
        try:
            if diagServiceElement.attrib['TRANSMISSION-MODE'] == 'SEND-ONLY':
                return None
        except:
            pass

        responseId = 0

        shortName = diagServiceElement.find('SHORT-NAME').text
        checkFunctionName = "check_{0}".format(shortName)
        positiveResponseElement = xmlElements[(diagServiceElement.find('POS-RESPONSE-REFS')).find('POS-RESPONSE-REF').attrib['ID-REF']]

        checkFunctionString = checkFunctionTemplate.format(checkFunctionName) # 0
        exec(checkFunctionString)
        return locals()[checkFunctionName]


    ##
    # @brief method to encode the positive response from the raw type to it physical representation
    @staticmethod
    def create_encodePositiveResponseFunction(diagServiceElement, xmlElements):
        # Some services are present in the ODX in both response and send only versions (with the same short name, so one will overwrite the other).
        # Avoiding the overwrite by ignoring the send-only versions, i.e. these are identical other than postivie response details being missing.
        try:
            if diagServiceElement.attrib['TRANSMISSION-MODE'] == 'SEND-ONLY':
                return None
        except:
            pass

        # The values in the response are SID, resetType, and optionally the powerDownTime (only for resetType 0x04). Checking is handled in the check function, 
        # so must be present and ok. This function is only required to return the resetType and powerDownTime (if present).

        positiveResponseElement = xmlElements[(diagServiceElement.find('POS-RESPONSE-REFS')).find('POS-RESPONSE-REF').attrib['ID-REF']]
		
        shortName = diagServiceElement.find('SHORT-NAME').text
        encodePositiveResponseFunctionName = "encode_{0}".format(shortName)

        encodeFunctionString = encodePositiveResponseFuncTemplate.format(encodePositiveResponseFunctionName)
        exec(encodeFunctionString)
        return locals()[encodePositiveResponseFunctionName]



    ##
    # @brief method to create the negative response function for the service element
    @staticmethod
    def create_checkNegativeResponseFunction(diagServiceElement, xmlElements):
        # Some services are present in the ODX in both response and send only versions (with the same short name, so one will overwrite the other).
        # Avoiding the overwrite by ignoring the send-only versions, i.e. these are identical other than postivie response details being missing.
        try:
            if diagServiceElement.attrib['TRANSMISSION-MODE'] == 'SEND-ONLY':
                return None
        except:
            pass

        shortName = diagServiceElement.find('SHORT-NAME').text
        check_negativeResponseFunctionName = "check_negResponse_{0}".format(shortName)

        negativeResponsesElement = diagServiceElement.find('NEG-RESPONSE-REFS')

        negativeResponseChecks = []

        for negativeResponse in negativeResponsesElement:
            negativeResponseRef = xmlElements[negativeResponse.attrib['ID-REF']]

            negativeResponseParams = negativeResponseRef.find('PARAMS')

            for param in negativeResponseParams:

                semantic = None
                try:
                    semantic = param.attrib['SEMANTIC']
                except:
                    semantic = None

                if semantic == 'SERVICE-ID':
                    serviceId = param.find('CODED-VALUE').text
                    start = int(param.find('BYTE-POSITION').text)
                    diagCodedType = param.find('DIAG-CODED-TYPE')
                    bitLength = int((param.find('DIAG-CODED-TYPE')).find('BIT-LENGTH').text)
                    listLength = int(bitLength/8)
                    end = start + listLength

                    checkString = "if input[{0}:{1}] == [{2}]: raise Exception(\"Detected negative response: {{0}}\".format(str([hex(n) for n in input])))".format(start,
                                                                                                                                                                   end,
                                                                                                                                                                   serviceId)
                    negativeResponseChecks.append(checkString)

                    pass
                pass

        negativeResponseFunctionString = negativeResponseFuncTemplate.format(check_negativeResponseFunctionName,
                                                                             "\n....".join(negativeResponseChecks))
        exec(negativeResponseFunctionString)
        return locals()[check_negativeResponseFunctionName]
