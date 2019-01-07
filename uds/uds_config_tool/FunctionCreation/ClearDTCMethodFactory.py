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


# When encode the dataRecord for transmission we have to allow for multiple elements in the data record
# i.e. 'value1' - for a single value, or [('param1','value1'),('param2','value2')]  for more complex data records
requestFuncTemplate = str("def {0}(groupOfDTC):\n"
                          "    {2}\n"
                          "    return {1} + encoded")									 


checkFunctionTemplate = str("def {0}(input):\n"
                            "    serviceIdExpected = {1}\n"
                            "    serviceId = DecodeFunctions.buildIntFromList(input[{2}:{3}])\n"
                            "    if(len(input) != {4}): raise Exception(\"Total length returned not as expected. Expected: {4}; Got {{0}}\".format(len(input)))\n"
                            "    if(serviceId != serviceIdExpected): raise Exception(\"Service Id Received not expected. Expected {{0}}; Got {{1}} \".format(serviceIdExpected, serviceId))")

negativeResponseFuncTemplate = str("def {0}(input):\n"
                                   "    {1}")

encodePositiveResponseFuncTemplate = str("def {0}(input):\n"
                                         "    return")

class ClearDTCMethodFactory(IServiceMethodFactory):

    ##
    # @brief method to create the request function for the service element
    @staticmethod
    def create_requestFunction(diagServiceElement, xmlElements):
        serviceId = 0
        diagnosticId = 0

        shortName = "request_{0}".format(diagServiceElement.find('SHORT-NAME').text)
        requestElement = xmlElements[diagServiceElement.find('REQUEST-REF').attrib['ID-REF']]
        paramsElement = requestElement.find('PARAMS')

        encodeFunction = "None"

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
            elif semantic == 'DATA':
                dataObjectElement = xmlElements[(param.find('DOP-REF')).attrib['ID-REF']]
                longName = param.find('LONG-NAME').text
                bytePosition = int(param.find('BYTE-POSITION').text)
                # We're not worrying about the formatting here, as we simply need the 3 byte hex to identify the DTC or DTC group ... (but can be changed if required)
                functionStringSingle = "DecodeFunctions.intArrayToIntArray(groupOfDTC, 'uint8', 'int8')"

                encodeFunction = "encoded = {1}".format(longName,functionStringSingle)

        funcString = requestFuncTemplate.format(shortName,
                                                serviceId,
												encodeFunction)
        exec(funcString)
        return locals()[shortName]

    ##
    # @brief method to create the function to check the positive response for validity
    @staticmethod
    def create_checkPositiveResponseFunction(diagServiceElement, xmlElements):
        responseId = 0
        diagnosticId = 0

        responseIdStart = 0
        responseIdEnd = 0

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
                else:
                    pass
            except:
                #print(sys.exc_info())
                pass

        checkFunctionString = checkFunctionTemplate.format(checkFunctionName, # 0
                                                           responseId, # 1
                                                           responseIdStart, # 2
                                                           responseIdEnd, # 3
                                                           totalLength) # 4
        exec(checkFunctionString)
        return locals()[checkFunctionName]

    ##
    # @brief method to encode the positive response from the raw type to it physical representation
    @staticmethod
    def create_encodePositiveResponseFunction(diagServiceElement, xmlElements):
        # There's nothing to extract here! The only value in the response is the DID, checking of which is handled in the check function, 
        # so must be present and ok. This function is only required to return the default None response.
		
        shortName = diagServiceElement.find('SHORT-NAME').text
        encodePositiveResponseFunctionName = "encode_{0}".format(shortName)
		
        encodeFunctionString = encodePositiveResponseFuncTemplate.format(encodePositiveResponseFunctionName) # 0
        exec(encodeFunctionString)
        return locals()[encodePositiveResponseFunctionName]

    ##
    # @brief method to create the negative response function for the service element
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
