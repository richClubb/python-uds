#!/usr/bin/env python

__author__ = "Richard Clubb"
__copyrights__ = "Copyright 2018, the python-uds project"
__credits__ = ["Richard Clubb"]

__license__ = "MIT"
__maintainer__ = "Richard Clubb"
__email__ = "richard.clubb@embeduk.com"
__status__ = "Development"

import xml.etree.ElementTree as ET
from uds.uds_config_tool import DecodeFunctions
import sys
from uds.uds_config_tool.FunctionCreation.iServiceMethodFactory import IServiceMethodFactory

SUPPRESS_RESPONSE_BIT = 0x80
									 
requestFuncTemplate = str("def {0}(suppressResponse=False):\n"
                          "    sessionType = {2}\n"
                          "    suppressBit = {3} if suppressResponse else 0x00\n"
                          "    sessionType[0] += suppressBit\n"
                          "    return {1} + sessionType")	

# Note: we do not need to cater for response suppression checking as nothing to check if response is suppressed - always unsuppressed
checkFunctionTemplate = str("def {0}(input):\n"
                            "    serviceIdExpected = {1}\n"
                            "    sessionTypeExpected = {2}\n"
                            "    serviceId = DecodeFunctions.buildIntFromList(input[{3}:{4}])\n"
                            "    sessionType = DecodeFunctions.buildIntFromList(input[{5}:{6}])\n"
                            "    if(len(input) != {7}): raise Exception(\"Total length returned not as expected. Expected: {7}; Got {{0}}\".format(len(input)))\n"
                            "    if(serviceId != serviceIdExpected): raise Exception(\"Service Id Received not expected. Expected {{0}}; Got {{1}} \".format(serviceIdExpected, serviceId))\n"
                            "    if(sessionType != sessionTypeExpected): raise Exception(\"Session Type Received not as expected. Expected: {{0}}; Got {{1}}\".format(sessionTypeExpected, sessionType))")

negativeResponseFuncTemplate = str("def {0}(input):\n"
                                   "    result = {{}}\n"
                                   "    nrcList = {5}\n"
                                   "    if input[{1}:{2}] == [{3}]:\n"
                                   "        result['NRC'] = input[{4}]\n"
                                   "        result['NRC_Label'] = nrcList.get(result['NRC'])\n"
                                   "    return result")

# Note: we do not need to cater for response suppression checking as nothing to check if response is suppressed - always unsuppressed
encodePositiveResponseFuncTemplate = str("def {0}(input):\n"
                                         "    result = {{}}\n"
                                         "    {1}\n"
                                         "    return result")


class DiagnosticSessionControlMethodFactory(IServiceMethodFactory):

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
        sessionType = 0

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
            elif(semantic == 'SUBFUNCTION'):
                sessionType = [int(param.find('CODED-VALUE').text)]
                if sessionType[0] >= SUPPRESS_RESPONSE_BIT:
                    pass
                    #raise ValueError("Diagnostic Session Control:session type exceeds maximum value (received {0})".format(sessionType[0]))

        funcString = requestFuncTemplate.format(shortName,
                                                serviceId,
                                                sessionType,
                                                SUPPRESS_RESPONSE_BIT)
        exec(funcString)
        return locals()[shortName]


    ##
    # @brief method to create the function to check the positive response for validity
    @staticmethod
    def create_checkPositiveResponseFunction(diagServiceElement, xmlElements):

        # Some services are present in the ODX in both response and send only versions (with the same short name, so one will overwrite the other).
        # Avoiding the overwrite by ignoring the send-only versions, i.e. these are identical other than postivie response details being missing.
        try:
            if diagServiceElement.attrib['TRANSMISSION-MODE'] == 'SEND-ONLY':
                return None
        except:
            pass

        responseId = 0
        sessionType = 0

        responseIdStart = 0
        responseIdEnd = 0
        sessionTypeStart = 0
        sessionTypeEnd = 0

        shortName = "request_{0}".format(diagServiceElement.find('SHORT-NAME').text)
        checkFunctionName = "check_{0}".format(shortName)
        positiveResponseElement = xmlElements[(diagServiceElement.find('POS-RESPONSE-REFS')).find('POS-RESPONSE-REF').attrib['ID-REF']]

        paramsElement = positiveResponseElement.find('PARAMS')

        totalLength = 0
        paramCnt = 0

        for param in paramsElement:
            try:
                semantic = None
                try:
                    semantic = param.attrib['SEMANTIC']
                except AttributeError:
                    pass

                startByte = int(param.find('BYTE-POSITION').text)

                if(semantic == 'SERVICE-ID'):
                    responseId = int(param.find('CODED-VALUE').text)
                    bitLength = int((param.find('DIAG-CODED-TYPE')).find('BIT-LENGTH').text)
                    listLength = int(bitLength / 8)
                    responseIdStart = startByte
                    responseIdEnd = startByte + listLength
                    totalLength += listLength
                elif(semantic == 'SUBFUNCTION'):
                    sessionType = int(param.find('CODED-VALUE').text)
                    bitLength = int((param.find('DIAG-CODED-TYPE')).find('BIT-LENGTH').text)
                    listLength = int(bitLength / 8)
                    sessionTypeStart = startByte
                    sessionTypeEnd = startByte + listLength
                    totalLength += listLength
                elif(semantic == 'DATA'):
                    dataObjectElement = xmlElements[(param.find('DOP-REF')).attrib['ID-REF']]
                    if(dataObjectElement.tag == "DATA-OBJECT-PROP"):
                        start = int(param.find('BYTE-POSITION').text)
                        bitLength = int(dataObjectElement.find('DIAG-CODED-TYPE').find('BIT-LENGTH').text)
                        listLength = int(bitLength/8)
                        totalLength += listLength
                    elif(dataObjectElement.tag == "STRUCTURE"):
                        start = int(param.find('BYTE-POSITION').text)
                        listLength = int(dataObjectElement.find('BYTE-SIZE').text)
                        totalLength += listLength
                    else:
                        pass
                else:
                    pass
            except:
                #print(sys.exc_info())
                pass


        checkFunctionString = checkFunctionTemplate.format(checkFunctionName, # 0
                                                           responseId, # 1
                                                           sessionType, # 2
                                                           responseIdStart, # 3
                                                           responseIdEnd, # 4
                                                           sessionTypeStart, # 5
                                                           sessionTypeEnd, # 6
                                                           totalLength) # 7
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

        # The values in the response are SID, diagnosticSessionType, and session parameters. Checking is handled in the check function, 
        # so must be present and ok. This function is only required to return the diagnosticSessionType, and session parameters.
        positiveResponseElement = xmlElements[(diagServiceElement.find('POS-RESPONSE-REFS')).find('POS-RESPONSE-REF').attrib['ID-REF']]
		
        shortName = diagServiceElement.find('SHORT-NAME').text
        encodePositiveResponseFunctionName = "encode_{0}".format(shortName)

        params = positiveResponseElement.find('PARAMS')

        encodeFunctions = []

        for param in params:
            try:
                semantic = None
                try:
                    semantic = param.attrib['SEMANTIC']
                except AttributeError:
                    pass

                if semantic == 'SUBFUNCTION':
                    longName = param.find('LONG-NAME').text
                    bytePosition = int(param.find('BYTE-POSITION').text)
                    bitLength = int(param.find('DIAG-CODED-TYPE').find('BIT-LENGTH').text)
                    listLength = int(bitLength / 8)
                    endPosition = bytePosition + listLength
                    encodingType = param.find('DIAG-CODED-TYPE').attrib['BASE-DATA-TYPE']
                    if(encodingType) == "A_ASCIISTRING":
                        functionString = "DecodeFunctions.intListToString(input[{0}:{1}], None)".format(bytePosition,
                                                                                                        endPosition)
                    else:
                        functionString = "input[{1}:{2}]".format(longName,
                                                                 bytePosition,
                                                                 endPosition)
                    encodeFunctions.append("result['{0}'] = {1}".format(longName,
                                                                        functionString))
                if semantic == 'DATA':
                    dataObjectElement = xmlElements[(param.find('DOP-REF')).attrib['ID-REF']]
                    longName = param.find('LONG-NAME').text
                    bytePosition = int(param.find('BYTE-POSITION').text)
                    bitLength = int(dataObjectElement.find('DIAG-CODED-TYPE').find('BIT-LENGTH').text)
                    listLength = int(bitLength / 8)
                    endPosition = bytePosition + listLength
                    encodingType = dataObjectElement.find('DIAG-CODED-TYPE').attrib['BASE-DATA-TYPE']
                    if(encodingType) == "A_ASCIISTRING":
                        functionString = "DecodeFunctions.intListToString(input[{0}:{1}], None)".format(bytePosition,
                                                                                                        endPosition)
                    elif(encodingType == "A_UINT32"):
                        functionString = "input[{1}:{2}]".format(longName,
                                                                 bytePosition,
                                                                 endPosition)
                    else:
                        functionString = "input[{1}:{2}]".format(longName,
                                                                 bytePosition,
                                                                 endPosition)
                    encodeFunctions.append("result['{0}'] = {1}".format(longName,
                                                                        functionString))

            except:
                pass

        encodeFunctionString = encodePositiveResponseFuncTemplate.format(encodePositiveResponseFunctionName,
                                                                         "\n    ".join(encodeFunctions))
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

                bytePosition = int(param.find('BYTE-POSITION').text)

                if semantic == 'SERVICE-ID':
                    serviceId = param.find('CODED-VALUE').text
                    start = int(param.find('BYTE-POSITION').text)
                    diagCodedType = param.find('DIAG-CODED-TYPE')
                    bitLength = int((param.find('DIAG-CODED-TYPE')).find('BIT-LENGTH').text)
                    listLength = int(bitLength/8)
                    end = start + listLength
                elif bytePosition == 2:
                    nrcPos = bytePosition
                    expectedNrcDict = {}
                    try:
                        dataObjectElement = xmlElements[(param.find('DOP-REF')).attrib['ID-REF']]
                        nrcList = dataObjectElement.find('COMPU-METHOD').find('COMPU-INTERNAL-TO-PHYS').find('COMPU-SCALES')
                        for nrcElem in nrcList:
                            expectedNrcDict[int(nrcElem.find('UPPER-LIMIT').text)] = nrcElem.find('COMPU-CONST').find('VT').text
                    except:
                        pass
                pass

        negativeResponseFunctionString = negativeResponseFuncTemplate.format(check_negativeResponseFunctionName, start, end, serviceId, nrcPos, expectedNrcDict)

        exec(negativeResponseFunctionString)
        return locals()[check_negativeResponseFunctionName]
