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
requestFuncTemplate = str("def {0}(dataRecord):\n"
                          "    encoded = []\n"
                          "    if type(dataRecord) == list and type(dataRecord[0]) == tuple:\n"
                          "        drDict = dict(dataRecord)\n"
                          "        {3}\n"
                          "{4}\n"
                          "    return {1} + {2} + encoded")									 


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
                                         "    return")

class WriteDataByIdentifierMethodFactory(IServiceMethodFactory):

    ##
    # @brief method to create the request function for the service element
    @staticmethod
    def create_requestFunction(diagServiceElement, xmlElements):
        serviceId = 0
        diagnosticId = 0

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
            elif(semantic == 'ID'):
                diagnosticId = DecodeFunctions.intArrayToIntArray([int(param.find('CODED-VALUE').text)], 'int16', 'int8')
            elif semantic == 'DATA':
                dataObjectElement = xmlElements[(param.find('DOP-REF')).attrib['ID-REF']]
                longName = param.find('LONG-NAME').text
                bytePosition = int(param.find('BYTE-POSITION').text)
                # Catching any exceptions where we don't know the type - these will fail elsewhere, but at least we can test what does work.
                try:
                    encodingType = dataObjectElement.find('DIAG-CODED-TYPE').attrib['BASE-DATA-TYPE']
                except:
                    encodingType = "unknown"  # ... for now just drop into the "else" catch-all ??????????????????????????????????????????????
                if(encodingType) == "A_ASCIISTRING":
                    functionStringList = "DecodeFunctions.stringToIntList(drDict['{0}'], None)".format(longName)
                    functionStringSingle = "DecodeFunctions.stringToIntList(dataRecord, None)"
                elif(encodingType) == "A_INT8":
                    functionStringList = "DecodeFunctions.intArrayToIntArray(drDict['{0}'], 'int8', 'int8')".format(longName)
                    functionStringSingle = "DecodeFunctions.intArrayToIntArray(dataRecord, 'int8', 'int8')"
                elif(encodingType) == "A_INT16":
                    functionStringList = "DecodeFunctions.intArrayToIntArray(drDict['{0}'], 'int16', 'int8')".format(longName)
                    functionStringSingle = "DecodeFunctions.intArrayToIntArray(dataRecord, 'int16', 'int8')"
                elif(encodingType) == "A_INT32":
                    functionStringList = "DecodeFunctions.intArrayToIntArray(drDict['{0}'], 'int32', 'int8')".format(longName)
                    functionStringSingle = "DecodeFunctions.intArrayToIntArray(dataRecord, 'int32', 'int8')"
                elif(encodingType) == "A_UINT8":
                    functionStringList = "DecodeFunctions.intArrayToIntArray(drDict['{0}'], 'uint8', 'int8')".format(longName)
                    functionStringSingle = "DecodeFunctions.intArrayToIntArray(dataRecord, 'uint8', 'int8')"
                elif(encodingType) == "A_UINT16":
                    functionStringList = "DecodeFunctions.intArrayToIntArray(drDict['{0}'], 'uint16', 'int8')".format(longName)
                    functionStringSingle = "DecodeFunctions.intArrayToIntArray(dataRecord, 'uint16', 'int8')"
                elif(encodingType) == "A_UINT32":
                    functionStringList = "DecodeFunctions.intArrayToIntArray(drDict['{0}'], 'uint32', 'int8')".format(longName)
                    functionStringSingle = "DecodeFunctions.intArrayToIntArray(dataRecord, 'uint32', 'int8')"
                else:
                    functionStringList = "drDict['{0}']".format(longName)
                    functionStringSingle = "dataRecord"

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
                encodeFunctions.append("encoded += {1}".format(longName,
                                                                 functionStringList))
                encodeFunction = "    else:\n        encoded = {1}".format(longName,functionStringSingle)



        # If we have only a single value for the dataRecord to send, then we can simply suppress the single value sending option.
        # Note: in the reverse case, we do not suppress the dictionary method of sending, as this allows extra flexibility, allowing 
        # a user to use a consistent list format in all situations if desired.
        if len(encodeFunctions) > 1:
            encodeFunction = ""

        funcString = requestFuncTemplate.format(shortName,
                                                serviceId,
                                                diagnosticId,
												"\n        ".join(encodeFunctions),  # ... handles input via list
												encodeFunction)                  # ... handles input via single value
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
        diagnosticIdStart = 0
        diagnosticIdEnd = 0

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
                else:
                    pass
            except:
                #print(sys.exc_info())
                pass

        checkFunctionString = checkFunctionTemplate.format(checkFunctionName, # 0
                                                           responseId, # 1
                                                           diagnosticId, # 2
                                                           responseIdStart, # 3
                                                           responseIdEnd, # 4
                                                           diagnosticIdStart, # 5
                                                           diagnosticIdEnd, # 6
                                                           totalLength) # 7
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
