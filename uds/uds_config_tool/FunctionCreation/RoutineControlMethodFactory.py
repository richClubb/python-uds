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

SUPPRESS_RESPONSE_BIT = 0x80

requestFuncTemplate = str("def {0}(optionRecord,suppressResponse=False):\n"
                          "    controlType = {2}\n"
                          "    suppressBit = {6} if suppressResponse else 0x00\n"
                          "    controlType[0] += suppressBit\n"
                          "    encoded = []\n"
                          "    if optionRecord is not None:\n"
                          "        if type(optionRecord) == list and type(optionRecord[0]) == tuple:\n"
                          "            drDict = dict(optionRecord)\n"
                          "            {4}\n"
                          "{5}\n"
                          "    return {1} + controlType + {3} + encoded")

# Note: we do not need to cater for response suppression checking as nothing to check if response is suppressed - always unsuppressed
checkFunctionTemplate = str("def {0}(input):\n"
                            "    serviceIdExpected = {1}\n"
                            "    controlTypeExpected = {2}\n"
                            "    routineIdExpected = {3}\n"
                            "    serviceId = DecodeFunctions.buildIntFromList(input[{4}:{5}])\n"
                            "    controlType = DecodeFunctions.buildIntFromList(input[{6}:{7}])\n"
                            "    routineId = DecodeFunctions.buildIntFromList(input[{8}:{9}])\n"
                            "    if(len(input) != {10}): raise Exception(\"Total length returned not as expected. Expected: {10}; Got {{0}}\".format(len(input)))\n"
                            "    if(serviceId != serviceIdExpected): raise Exception(\"Service Id Received not expected. Expected {{0}}; Got {{1}} \".format(serviceIdExpected, serviceId))\n"
                            "    if(controlType != controlTypeExpected): raise Exception(\"Control Type Received not expected. Expected {{0}}; Got {{1}} \".format(controlTypeExpected, controlType))\n"
                            "    if(routineId != routineIdExpected): raise Exception(\"Routine Id Received not as expected. Expected: {{0}}; Got {{1}}\".format(routineIdExpected, routineId))")

negativeResponseFuncTemplate = str("def {0}(input):\n"
                                   "    {1}")

# Note: we do not need to cater for response suppression checking as nothing to check if response is suppressed - always unsuppressed
encodePositiveResponseFuncTemplate = str("def {0}(input):\n"
                                         "    result = {{}}\n"
                                         "    {1}\n"
                                         "    return result")


class RoutineControlMethodFactory(IServiceMethodFactory):

    ##
    # @brief method to create the request function for the service element
    @staticmethod
    def create_requestFunction(diagServiceElement, xmlElements):
        # Some services are present in the ODX in both response and send only versions (with the same short name, so one will overwrite the other).
        # Avoiding the overwrite by ignoring the send-only versions, i.e. these are identical other than positive response details being missing.
        try:
            if diagServiceElement.attrib['TRANSMISSION-MODE'] == 'SEND-ONLY':
                return (None, "")
        except:
            pass

        serviceId = 0
        controlType = 0
        routineId = 0

        shortName = "request_{0}".format(diagServiceElement.find('SHORT-NAME').text)
        requestElement = xmlElements[diagServiceElement.find('REQUEST-REF').attrib['ID-REF']]
        paramsElement = requestElement.find('PARAMS')

        encodeFunctions = []
        encodeFunction = ""

        for param in paramsElement:
            try:
                semantic = None
                try:
                    semantic = param.attrib['SEMANTIC']
                except AttributeError:
                    pass

                if (semantic == 'SERVICE-ID'):
                    serviceId = [int(param.find('CODED-VALUE').text)]
                elif (semantic == 'SUBFUNCTION'):
                    controlType = [int(param.find('CODED-VALUE').text)]
                    if controlType[0] >= SUPPRESS_RESPONSE_BIT:
                        pass
                        # raise ValueError("ECU Reset:reset type exceeds maximum value (received {0})".format(resetType[0]))
                elif (semantic == 'ID'):
                    routineId = DecodeFunctions.intArrayToIntArray([int(param.find('CODED-VALUE').text)], 'int16',
                                                                   'int8')
                elif semantic == 'DATA':
                    dataObjectElement = xmlElements[(param.find('DOP-REF')).attrib['ID-REF']]
                    longName = param.find('LONG-NAME').text
                    bytePosition = int(param.find('BYTE-POSITION').text)
                    # Catching any exceptions where we don't know the type - these will fail elsewhere, but at least we can test what does work.
                    try:
                        encodingType = dataObjectElement.find('DIAG-CODED-TYPE').attrib['BASE-DATA-TYPE']
                    except:
                        encodingType = "unknown"  # ... for now just drop into the "else" catch-all ???????!!!!!!!

                    # We need to always respect given bit lengths!
                    try:
                        bitLength = int(dataObjectElement.find('DIAG-CODED-TYPE').find('BIT-LENGTH').text)
                    except:
                        bitLength = 32  # just assume maximum length when in doubt

                    if (encodingType) == "A_ASCIISTRING":
                        functionStringList = "DecodeFunctions.stringToIntList(drDict['{0}'], None)".format(longName)
                        functionStringSingle = "DecodeFunctions.stringToIntList(optionRecord, None)"
                    elif (encodingType) == "A_INT8":
                        functionStringList = "DecodeFunctions.intArrayToIntArray(drDict['{0}'], 'int8', 'int8')".format(
                            longName)
                        functionStringSingle = "DecodeFunctions.intArrayToIntArray(optionRecord, 'int8', 'int8')"
                    elif (encodingType) == "A_INT16":
                        functionStringList = "DecodeFunctions.intArrayToIntArray(drDict['{0}'], 'int16', 'int8')".format(
                            longName)
                        functionStringSingle = "DecodeFunctions.intArrayToIntArray(optionRecord, 'int16', 'int8')"
                        if bitLength < 16:
                            functionStringList = functionStringList + "[1:]"
                            functionStringSingle = functionStringSingle + "[1:]"
                    elif (encodingType) == "A_INT32":
                        functionStringList = "DecodeFunctions.intArrayToIntArray(drDict['{0}'], 'int32', 'int8')".format(
                            longName)
                        functionStringSingle = "DecodeFunctions.intArrayToIntArray(optionRecord, 'int32', 'int8')"
                        if bitLength == 8:
                            functionStringList = functionStringList + "[3:]"
                            functionStringSingle = functionStringSingle + "[3:]"
                        elif bitLength == 16:
                            functionStringList = functionStringList + "[2:]"
                            functionStringSingle = functionStringSingle + "[2:]"
                        elif bitLength == 24:
                            functionStringList = functionStringList + "[1:]"
                            functionStringSingle = functionStringSingle + "[1:]"
                    elif (encodingType) == "A_UINT8":
                        functionStringList = "DecodeFunctions.intArrayToIntArray(drDict['{0}'], 'uint8', 'int8')".format(
                            longName)
                        functionStringSingle = "DecodeFunctions.intArrayToIntArray(optionRecord, 'uint8', 'int8')"
                    elif (encodingType) == "A_UINT16":
                        functionStringList = "DecodeFunctions.intArrayToIntArray(drDict['{0}'], 'uint16', 'int8')".format(
                            longName)
                        functionStringSingle = "DecodeFunctions.intArrayToIntArray(optionRecord, 'uint16', 'int8')"
                        if bitLength < 16:
                            functionStringList = functionStringList + "[1:]"
                            functionStringSingle = functionStringSingle + "[1:]"
                    elif (encodingType) == "A_UINT32":
                        functionStringList = "DecodeFunctions.intArrayToIntArray(drDict['{0}'], 'uint32', 'int8')".format(
                            longName)
                        functionStringSingle = "DecodeFunctions.intArrayToIntArray(optionRecord, 'uint32', 'int8')"
                        if bitLength == 8:
                            functionStringList = functionStringList + "[3:]"
                            functionStringSingle = functionStringSingle + "[3:]"
                        elif bitLength == 16:
                            functionStringList = functionStringList + "[2:]"
                            functionStringSingle = functionStringSingle + "[2:]"
                        elif bitLength == 24:
                            functionStringList = functionStringList + "[1:]"
                            functionStringSingle = functionStringSingle + "[1:]"
                    else:
                        functionStringList = "drDict['{0}']".format(longName)
                        functionStringSingle = "optionRecord"
                    """
The following encoding types may be required at some stage, but are not currently supported by any functions in the DecodeFunctions.py module ...

    A_VOID: pseudo type for non-existing elements
    A_BIT: one bit
    A_INT64: signed integer 64-bit, two's complement
    A_FLOAT32: IEEE 754 single precision
    A_FLOAT64: IEEE 754 double precision
    A_ASCIISTRING: string, ISO-8859-1 encoded
    A_UTF8STRING: string, UTF-8 encoded
    A_UNICODE2STRING: string, UCS-2 encoded
    A_BYTEFIELD: Field of bytes
	
Also, we will most need to handle scaling at some stage within DecodeFunctions.py (for RDBI at the very least)
                    """

                    # 
                    encodeFunctions.append("encoded += {}".format(functionStringList))
                    encodeFunction = "    else:\n" \
                                     "      if type(optionRecord) == list:\n" \
                                     "          for elem in dataRecord:\n" \
                                     "              encoded += {0}\n" \
                                     "      else:\n" \
                                     "          encoded = {1}".format(
                        functionStringSingle.replace("optionRecord", "elem"),
                        functionStringSingle)


            except:
                pass

        funcString = requestFuncTemplate.format(shortName,  # 0
                                                serviceId,  # 1
                                                controlType,  # 2
                                                routineId,  # 3
                                                "\n            ".join(encodeFunctions),
                                                # ... handles input via list # 4
                                                encodeFunction,  # ... handles input via single value # 5
                                                SUPPRESS_RESPONSE_BIT)  # 6
        exec(funcString)
        return (locals()[shortName], str(controlType))

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
        controlType = 0
        routineId = 0

        responseIdStart = 0
        responseIdEnd = 0
        controlTypeStart = 0
        controlTypeEnd = 0
        routineIdStart = 0
        routineIdEnd = 0

        shortName = diagServiceElement.find('SHORT-NAME').text
        checkFunctionName = "check_{0}".format(shortName)
        positiveResponseElement = xmlElements[
            (diagServiceElement.find('POS-RESPONSE-REFS')).find('POS-RESPONSE-REF').attrib['ID-REF']]

        paramsElement = positiveResponseElement.find('PARAMS')

        totalLength = 0
        powerDownTimeLen = 0

        for param in paramsElement:
            try:
                semantic = None
                try:
                    semantic = param.attrib['SEMANTIC']
                except AttributeError:
                    pass

                startByte = int(param.find('BYTE-POSITION').text)

                if (semantic == 'SERVICE-ID'):
                    responseId = int(param.find('CODED-VALUE').text)
                    bitLength = int((param.find('DIAG-CODED-TYPE')).find('BIT-LENGTH').text)
                    listLength = int(bitLength / 8)
                    responseIdStart = startByte
                    responseIdEnd = startByte + listLength
                    totalLength += listLength
                elif (semantic == 'SUBFUNCTION'):
                    controlType = int(param.find('CODED-VALUE').text)
                    bitLength = int((param.find('DIAG-CODED-TYPE')).find('BIT-LENGTH').text)
                    listLength = int(bitLength / 8)
                    controlTypeStart = startByte
                    controlTypeEnd = startByte + listLength
                    totalLength += listLength
                elif (semantic == 'ID'):
                    routineId = int(param.find('CODED-VALUE').text)
                    bitLength = int((param.find('DIAG-CODED-TYPE')).find('BIT-LENGTH').text)
                    listLength = int(bitLength / 8)
                    routineIdStart = startByte
                    routineIdEnd = startByte + listLength
                    totalLength += listLength
                elif (semantic == 'DATA'):
                    dataObjectElement = xmlElements[(param.find('DOP-REF')).attrib['ID-REF']]
                    if (dataObjectElement.tag == "DATA-OBJECT-PROP"):
                        start = int(param.find('BYTE-POSITION').text)
                        bitLength = int(dataObjectElement.find('DIAG-CODED-TYPE').find('BIT-LENGTH').text)
                        listLength = int(bitLength / 8)
                        totalLength += listLength
                    else:
                        pass
                else:
                    pass
            except:
                # print(sys.exc_info())
                pass

        checkFunctionString = checkFunctionTemplate.format(checkFunctionName,  # 0
                                                           responseId,  # 1
                                                           controlType,  # 2
                                                           routineId,  # 3
                                                           responseIdStart,  # 4
                                                           responseIdEnd,  # 5
                                                           controlTypeStart,  # 6
                                                           controlTypeEnd,  # 7
                                                           routineIdStart,  # 8
                                                           routineIdEnd,  # 9
                                                           totalLength)  # 10
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

        positiveResponseElement = xmlElements[
            (diagServiceElement.find('POS-RESPONSE-REFS')).find('POS-RESPONSE-REF').attrib['ID-REF']]

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
                    if (encodingType) == "A_ASCIISTRING":
                        functionString = "DecodeFunctions.intListToString(input[{0}:{1}], None)".format(bytePosition,
                                                                                                        endPosition)
                    else:
                        functionString = "input[{1}:{2}]".format(longName,
                                                                 bytePosition,
                                                                 endPosition)
                    encodeFunctions.append("result['{0}'] = {1}".format(longName,
                                                                        functionString))
                if semantic == 'ID':
                    longName = param.find('LONG-NAME').text
                    bytePosition = int(param.find('BYTE-POSITION').text)
                    bitLength = int(param.find('DIAG-CODED-TYPE').find('BIT-LENGTH').text)
                    listLength = int(bitLength / 8)
                    endPosition = bytePosition + listLength
                    encodingType = param.find('DIAG-CODED-TYPE').attrib['BASE-DATA-TYPE']
                    if (encodingType) == "A_ASCIISTRING":
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
                    if (encodingType) == "A_ASCIISTRING":
                        functionString = "DecodeFunctions.intListToString(input[{0}:{1}], None)".format(bytePosition,
                                                                                                        endPosition)
                    elif (encodingType == "A_UINT32"):
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

                if semantic == 'SERVICE-ID':
                    serviceId = param.find('CODED-VALUE').text
                    start = int(param.find('BYTE-POSITION').text)
                    diagCodedType = param.find('DIAG-CODED-TYPE')
                    bitLength = int((param.find('DIAG-CODED-TYPE')).find('BIT-LENGTH').text)
                    listLength = int(bitLength / 8)
                    end = start + listLength

                    checkString = "if input[{0}:{1}] == [{2}]: raise Exception(\"Detected negative response: {{0}}\".format(str([hex(n) for n in input])))".format(
                        start,
                        end,
                        serviceId)
                    negativeResponseChecks.append(checkString)

                    pass
                pass

        negativeResponseFunctionString = negativeResponseFuncTemplate.format(check_negativeResponseFunctionName,
                                                                             "\n....".join(negativeResponseChecks))
        exec(negativeResponseFunctionString)
        return locals()[check_negativeResponseFunctionName]
