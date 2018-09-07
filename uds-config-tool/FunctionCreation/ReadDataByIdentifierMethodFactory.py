#!/usr/bin/env python

__author__ = "Richard Clubb"
__copyrights__ = "Copyright 2018, the python-uds project"
__credits__ = ["Richard Clubb"]

__license__ = "MIT"
__maintainer__ = "Richard Clubb"
__email__ = "richard.clubb@embeduk.com"
__status__ = "Development"


import DecodeFunctions
import sys
from FunctionCreation.iServiceMethodFactory import IServiceMethodFactory


requestFuncTemplate = str("def {0}():\n"
                          "    return {1} + {2}")

checkFunctionTemplate = str("def {0}(input):\n"
                            "    serviceIdExpected = {1}\n"
                            "    diagnosticIdExpected = {2}\n"
                            "    serviceId = DecodeFunctions.buildIntFromList(input[{3}:{4}])\n"
                            "    diagnosticId = DecodeFunctions.buildIntFromList(input[{5}:{6}])\n"
                            "    if(len(input) != {7}): raise Exception(\"Total length returned not as expected. Expected: {7}; Got {{0}}\".format(len(input)))\n"
                            "    if(serviceId != serviceIdExpected): raise Exception(\"Service Id Received not expected. Expected {{0}}; Got {{1}} \".format(serviceIdExpected, serviceId))\n"
                            "    if(diagnosticId != diagnosticIdExpected): raise Exception(\"Diagnostic Id Received not as expected. Expected: {{0}}; Got {{1}}\".format(diagnosticIdExpected, diagnosticId))")

negativeResponseFuncTemplate = str("def {0}(input):\n"
                                   "    {1}")

encodePositiveResponseFuncTemplate = str("def {0}(input):\n"
                                         "    result = {{}}\n"
                                         "    {1}\n"
                                         "    return result")


##
# @brief this should be static
class ReadDataByIdentifierMethodFactory(IServiceMethodFactory):

    @staticmethod
    def create_requestFunction(diagServiceElement, xmlElements):

        serviceId = 0
        diagnosticId = 0

        shortName = "request_{0}".format(diagServiceElement.find('SHORT-NAME').text)
        requestElement = xmlElements[diagServiceElement.find('REQUEST-REF').attrib['ID-REF']]
        paramsElement = requestElement.find('PARAMS')
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

        funcString = requestFuncTemplate.format(shortName,
                                                serviceId,
                                                diagnosticId)
        # print(funcString)
        exec(funcString)
        return locals()[shortName]

    @staticmethod
    def create_checkPositiveResponseFunction(diagServiceElement, xmlElements):

        responseId = 0
        diagnosticId = 0

        shortName = diagServiceElement.find('SHORT-NAME').text
        checkFunctionName = "check_{0}".format(shortName)
        positiveResponseElement = xmlElements[(diagServiceElement.find('POS-RESPONSE-REFS')).find('POS-RESPONSE-REF').attrib['ID-REF']]

        paramsElement = positiveResponseElement.find('PARAMS')

        totalLength = 0

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
                print(sys.exc_info())
                pass

        checkFunctionString = checkFunctionTemplate.format(checkFunctionName, # 0
                                                           responseId, # 1
                                                           diagnosticId, # 2
                                                           responseIdStart, # 3
                                                           responseIdEnd, # 4
                                                           diagnosticIdStart, # 5
                                                           diagnosticIdEnd, # 6
                                                           totalLength) # 7

        # print(checkFunctionString)
        exec(checkFunctionString)
        return locals()[checkFunctionName]

    ##
    # @brief may need refactoring to deal with multiple positive-responses
    @staticmethod
    def create_encodePositiveResponseFunction(diagServiceElement, xmlElements):

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

        # print(encodeFunctionString)
        exec(encodeFunctionString)
        a = locals()[encodePositiveResponseFunctionName]
        return locals()[encodePositiveResponseFunctionName]

    @staticmethod
    def create_checkNegativeResponseFunction(diagServiceElement, xmlElements):

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

                    checkString = "if input[{0}:{1}] == {2}: raise Exception(\"Detected negative response: [hex(n) for n in input]\")".format(start,
                                                                                                                                              end,
                                                                                                                                              serviceId)
                    # print(checkString)
                    negativeResponseChecks.append(checkString)

                    pass
                pass

        negativeResponseFunctionString = negativeResponseFuncTemplate.format(check_negativeResponseFunctionName,
                                                                             "\n....".join(negativeResponseChecks))
        # print(negativeResponseFunctionString)
        exec(negativeResponseFunctionString)
        return locals()[check_negativeResponseFunctionName]

