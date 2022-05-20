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


# When encode the dataRecord for transmission we allow for multiple elements in the data record,
# i.e. IO Ctrl always has the option and mask records in the request
requestFuncTemplate = str("def {0}(dataRecord):\n"
                          "    encoded = []\n"
                          "    if type(dataRecord) == list and type(dataRecord[0]) == tuple:\n"
                          "        drDict = dict(dataRecord)\n"
                          "        {4}\n"
                          "{5}\n"
                          "    return {1} + {2} + {3} + encoded")											 

checkFunctionTemplate = str("def {0}(input):\n"
                            "    serviceIdExpected = {1}\n"
                            "    diagnosticIdExpected = {2}\n"
                            "    optionRecordExpected = {3}\n"
                            "    serviceId = DecodeFunctions.buildIntFromList(input[{4}:{5}])\n"
                            "    diagnosticId = DecodeFunctions.buildIntFromList(input[{6}:{7}])\n"
                            "    optionRecord = DecodeFunctions.buildIntFromList(input[{8}:{9}])\n"
                            "    if(len(input) != {10}): raise Exception(\"Total length returned not as expected. Expected: {10}; Got {{0}}\".format(len(input)))\n"
                            "    if(serviceId != serviceIdExpected): raise Exception(\"Service Id Received not expected. Expected {{0}}; Got {{1}} \".format(serviceIdExpected, serviceId))\n"
                            "    if(diagnosticId != diagnosticIdExpected): raise Exception(\"Diagnostic Id Received not as expected. Expected: {{0}}; Got {{1}}\".format(diagnosticIdExpected, diagnosticId))\n"
                            "    if(optionRecord != optionRecordExpected): raise Exception(\"Option Record Received not as expected. Expected: {{0}}; Got {{1}}\".format(optionRecordExpected, optionRecord))")

negativeResponseFuncTemplate = str("def {0}(input):\n"
                                   "    {1}")

encodePositiveResponseFuncTemplate = str("def {0}(input):\n"
                                         "    result = {{}}\n"
                                         "    {1}\n"
                                         "    return result")


class InputOutputControlMethodFactory(IServiceMethodFactory):

    ##
    # @brief method to create the request function for the service element
    @staticmethod
    def create_requestFunction(diagServiceElement, xmlElements):
        serviceId = 0
        diagnosticId = 0
        optionRecord = 0

        shortName = "request_{0}".format(diagServiceElement.find('SHORT-NAME').text)
        requestElement = xmlElements[diagServiceElement.find('REQUEST-REF').attrib['ID-REF']]
        paramsElement = requestElement.find('PARAMS')

        encodeFunctions = []
        encodeFunction = ""

        for param in paramsElement:
            semantic = None
            try:
                semantic = param.attrib['SEMANTIC']
            except AttributeError:
                pass

            if(semantic == 'SERVICE-ID'):
                serviceId = [int(param.find('CODED-VALUE').text)]
            elif(semantic == 'ID'):
                diagnosticId = DecodeFunctions.intArrayToIntArray([int(param.find('CODED-VALUE').text)], 'int16', 'int8')
            elif(semantic == 'SUBFUNCTION'):
                optionRecord = DecodeFunctions.intArrayToIntArray([int(param.find('CODED-VALUE').text)], 'int8', 'int8')
            elif semantic == 'DATA':
                dataObjectElement = xmlElements[(param.find('DOP-REF')).attrib['ID-REF']]
                longName = param.find('LONG-NAME').text
                bytePosition = int(param.find('BYTE-POSITION').text)

                # If data object is a structure
                if dataObjectElement.find('DIAG-CODED-TYPE') is None:
                    dataObjectElement = xmlElements[dataObjectElement.find('PARAMS').find('PARAM').find('DOP-REF').attrib['ID-REF']]

                try:
                    encodingType = dataObjectElement.find('DIAG-CODED-TYPE').attrib['BASE-DATA-TYPE']
                except:
                    encodingType = "unknown"  # ... for now just drop into the "else" catch-all

                # We need to always respect given bit lengths!
                try:
                    bitLength = int(dataObjectElement.find('DIAG-CODED-TYPE').find('BIT-LENGTH').text)
                except:
                    bitLength = 32  # just assume maximum length when in doubt

                if(encodingType) == "A_ASCIISTRING":
                    functionStringList = "DecodeFunctions.stringToIntList(drDict['{0}'], None)".format(longName)
                    functionStringSingle = "DecodeFunctions.stringToIntList(dataRecord, None)"
                elif(encodingType) == "A_INT8":
                    functionStringList = "DecodeFunctions.intArrayToIntArray(drDict['{0}'], 'int8', 'int8')".format(longName)
                    functionStringSingle = "DecodeFunctions.intArrayToIntArray(dataRecord, 'int8', 'int8')"
                elif(encodingType) == "A_INT16":
                    functionStringList = "DecodeFunctions.intArrayToIntArray(drDict['{0}'], 'int16', 'int8')".format(longName)
                    functionStringSingle = "DecodeFunctions.intArrayToIntArray(dataRecord, 'int16', 'int8')"
                    if bitLength < 16:
                        functionStringList = functionStringList + "[1:]"
                        functionStringSingle = functionStringSingle + "[1:]"
                elif(encodingType) == "A_INT32":
                    functionStringList = "DecodeFunctions.intArrayToIntArray(drDict['{0}'], 'int32', 'int8')".format(longName)
                    functionStringSingle = "DecodeFunctions.intArrayToIntArray(dataRecord, 'int32', 'int8')"
                    if bitLength == 8:
                        functionStringList = functionStringList + "[3:]"
                        functionStringSingle = functionStringSingle + "[3:]"
                    elif bitLength == 16:
                        functionStringList = functionStringList + "[2:]"
                        functionStringSingle = functionStringSingle + "[2:]"
                    elif bitLength == 24:
                        functionStringList = functionStringList + "[1:]"
                        functionStringSingle = functionStringSingle + "[1:]"
                elif(encodingType) == "A_UINT8":
                    functionStringList = "DecodeFunctions.intArrayToIntArray(drDict['{0}'], 'uint8', 'int8')".format(longName)
                    functionStringSingle = "DecodeFunctions.intArrayToIntArray(dataRecord, 'uint8', 'int8')"
                elif(encodingType) == "A_UINT16":
                    functionStringList = "DecodeFunctions.intArrayToIntArray(drDict['{0}'], 'uint16', 'int8')".format(longName)
                    functionStringSingle = "DecodeFunctions.intArrayToIntArray(dataRecord, 'uint16', 'int8')"
                    if bitLength < 16:
                        functionStringList = functionStringList + "[1:]"
                        functionStringSingle = functionStringSingle + "[1:]"
                elif(encodingType) == "A_UINT32":
                    functionStringList = "DecodeFunctions.intArrayToIntArray(drDict['{0}'], 'uint32', 'int8')".format(longName)
                    functionStringSingle = "DecodeFunctions.intArrayToIntArray(dataRecord, 'uint32', 'int8')"
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
                    functionStringSingle = "dataRecord"

                # 
                encodeFunctions.append("encoded += {}".format(functionStringList))
                encodeFunction = "    else:\n" \
                                 "      if type(dataRecord) == list:\n" \
                                 "          for elem in dataRecord:\n" \
                                 "              encoded += {0}\n" \
                                 "      else:\n" \
                                 "          encoded = {1}".format(functionStringSingle.replace("dataRecord", "elem"),
                                                                  functionStringSingle)

        funcString = requestFuncTemplate.format(shortName,
                                                serviceId,
                                                diagnosticId,
                                                optionRecord,
												"\n        ".join(encodeFunctions),  # ... handles input via list
												encodeFunction)                  # ... handles input via single value

        exec(funcString)
        return (locals()[shortName],str(optionRecord))



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
        diagnosticId = 0
        optionRecord = 0

        responseIdStart = 0
        responseIdEnd = 0
        diagnosticIdStart = 0
        diagnosticIdEnd = 0
        optionRecordStart = 0
        optionRecordEnd = 0

        shortName = diagServiceElement.find('SHORT-NAME').text
        checkFunctionName = "check_{0}".format(shortName)
        positiveResponseElement = xmlElements[(diagServiceElement.find('POS-RESPONSE-REFS')).find('POS-RESPONSE-REF').attrib['ID-REF']]

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

                if(semantic == 'SERVICE-ID'):
                    responseId = int(param.find('CODED-VALUE').text)
                    bitLength = int((param.find('DIAG-CODED-TYPE')).find('BIT-LENGTH').text)
                    listLength = int(bitLength / 8)
                    responseIdStart = startByte
                    responseIdEnd = startByte + listLength
                    totalLength += listLength
                elif(semantic == 'ID'):
                    diagnosticId = int(param.find('CODED-VALUE').text)
                    bitLength = int((param.find('DIAG-CODED-TYPE')).find('BIT-LENGTH').text)
                    listLength = int(bitLength / 8)
                    diagnosticIdStart = startByte
                    diagnosticIdEnd = startByte + listLength
                    totalLength += listLength
                elif(semantic == 'SUBFUNCTION'):
                    optionRecord = int(param.find('CODED-VALUE').text)
                    bitLength = int((param.find('DIAG-CODED-TYPE')).find('BIT-LENGTH').text)
                    listLength = int(bitLength / 8)
                    optionRecordStart = startByte
                    optionRecordEnd = startByte + listLength
                    totalLength += listLength
                elif(semantic == 'DATA'):
                    dataObjectElement = xmlElements[(param.find('DOP-REF')).attrib['ID-REF']]
                    if(dataObjectElement.tag == "DATA-OBJECT-PROP"):
                        start = int(param.find('BYTE-POSITION').text)
                        bitLength = int(dataObjectElement.find('DIAG-CODED-TYPE').find('BIT-LENGTH').text)
                        listLength = int(bitLength/8)
                        totalLength += listLength
                    elif(dataObjectElement.tag == "STRUCTURE"):
                        dataObjectElement = xmlElements[dataObjectElement.find('PARAMS').find('PARAM').find('DOP-REF').attrib['ID-REF']]
                        start = int(param.find('BYTE-POSITION').text)
                        bitLength = int(dataObjectElement.find('DIAG-CODED-TYPE').find('BIT-LENGTH').text)
                        listLength = int(bitLength / 8)
                        totalLength += listLength
                        pass
                else:
                    pass
            except:
                #print(sys.exc_info())
                pass


        checkFunctionString = checkFunctionTemplate.format(checkFunctionName, # 0
                                                           responseId, # 1
                                                           diagnosticId, # 2
                                                           optionRecord, # 3
                                                           responseIdStart, # 4
                                                           responseIdEnd, # 5
                                                           diagnosticIdStart, # 6
                                                           diagnosticIdEnd, # 7
                                                           optionRecordStart, # 8
                                                           optionRecordEnd, # 9
                                                           totalLength) # 10

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

        # The values in the response include SID and DID, but these do not need to be returned (and already checked in the check function).

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
                if semantic == 'ID':
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
