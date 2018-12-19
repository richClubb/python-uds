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
# Note: the request is not the simplest to parse from the ODX, so paritally hardcoding this one again (for now at least)
requestFuncTemplate = str("def {0}(DTCStatusMask=[],DTCMaskRecord=[],DTCSnapshotRecordNumber=[],DTCExtendedRecordNumber=[],DTCSeverityMask=[]):\n"
                          "    encoded = []\n"
                          "    if {2} in [0x01,0x02, 0x0F, 0x11, 0x12, 0x13]: # ... DTCStatusMask required for these subfunctions\n"
                          "        encode += DTCStatusMask\n"
                          "    if {2} in [0x03,0x04, 0x06, 0x09, 0x10]: # ... DTCMaskRecord required for these subfunctions\n"
                          "        encode += DTCMaskRecord # ... format is [0xNN,0xNN,0xNN]\n"
                          "    if {2} in [0x03,0x04, 0x05]: # ... DTCSnapshotRecordNumber required for these subfunctions\n"
                          "        encode += DTCSnapshotRecordNumber\n"
                          "    if {2} in [0x06,0x10]: # ... DTCExtendedRecordNumber required for these subfunctions\n"
                          "        encode += DTCExtendedRecordNumber\n"
                          "    if {2} in [0x07,0x08]: # ... DTCSeverityMaskRecord required for these subfunctions\n"
                          "        encode += DTCSeverityMask+DTCStatusMask\n"
                          "    return {1} + {2} + encoded # ... SID, sub-func, and params")

						  


checkFunctionTemplate = str("def {0}(input):\n"
                            "    serviceIdExpected = {1}\n"
                            "    subFunctionExpected = {2}\n"
							
def {0}(input):
    serviceIdExpected = {1}
    subFunctionExpected = {2}
    if {2} in [0x01,0x02, 0x0F, 0x11, 0x12, 0x13]: # ... DTCStatusMask required for these subfunctions
        ??? check ???
	elif {2} in [0x01,0x02, 0x0F, 0x11, 0x12, 0x13]: # ... DTCStatusMask required for these subfunctions
        ??? check ???
												
???????????????????????							
  

negativeResponseFuncTemplate = str("def {0}(input):\n"
                                   "    {1}")

encodePositiveResponseFuncTemplate = str("def {0}(input):\n"
                                         "    encoded = []\n"
                                         "    retval = None\n"
                                         "    if {2} in [0x02, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F, 0x13]: # ... these subfunctions have details extracted as follows:\n"
                                         "        retval = {'DTCStatusAvailabilityMask':input[2:3], 'DTCAndStatusRecord':[]}\n"
                                         "        records = input[3:]\n"
                                         "        for i in range(len(records)/4):\n"
                                         "            recStart = i*4\n"
                                         "            retval['DTCAndStatusRecord'].append({'DTC':records[recStart:recStart+3],'statusOfDTC':records[recStart+3:recStart+4]})\n"
                                         "\n"
                                         "    if {2} in [0x01, 0x07, 0x11, 0x12]: # ... these subfunctions have details extracted as follows:\n"
                                         "        retval = {'DTCStatusAvailabilityMask':input[2:3], 'DTCFormatIdentifier':input[3:4], 'DTCCount':input[4:6]}  # ... DTCCount probably needs decoding\n"
                                         "		\n"
                                         "    if {2} in [0x03]: # ... these subfunctions have details extracted as follows:\n"
                                         "        retval = []\n"
                                         "        records = input[3:]\n"
                                         "        for i in range(len(records)/4):\n"
                                         "            recStart = i*4\n"
                                         "            retval.append({'DTC':records[recStart:recStart+3],'DTCSnapshotRecordNumber':records[recStart+3:recStart+4]})\n"
                                         "\n"
                                         "    if {2} in [0x04]: # ... these subfunctions have details extracted as follows:\n"
                                         "        pass # ?????????????????????????????????????????\n"
                                         "	# ... the  length needs to be derived from the ODX\n"
                                         "\n"
                                         "    if {2} in [0x05]: # ... these subfunctions have details extracted as follows:\n"
                                         "        pass # ?????????????????????????????????????????\n"
                                         "	# ... the  length needs to be derived from the ODX\n"
                                         "\n"
                                         "    if {2} in [0x06, 0x10]: # ... these subfunctions have details extracted as follows:\n"
                                         "        pass\n"
                                         "    #    retval = {'DTCAndStatusRecord':{'DTC':records[2:5],'statusOfDTC':records[5:6]},'DTCExtendedData':[]}\n"
                                         "    #    records = input[6:]\n"
                                         "    #    for i in range(len(records)/4):\n"
                                         "    #        recStart = i*4\n"
                                         "    #        retval['DTCExtendedData'].append({'DTCExtendedDataRecordNumber':records[recStart:recStart+1],'DTCExtendedDataRecord':records[recStart+1:recStart+?????]})\n"
                                         "	# ... the extended data length needs to be derived from the ODX\n"
                                         "\n"
                                         "    if {2} in [0x08, 0x09]: # ... these subfunctions have details extracted as follows:\n"
                                         "        retval = {'DTCStatusAvailabilityMask':input[2:3], 'DTCAndSeverityRecord':[]}\n"
                                         "        records = input[3:]\n"
                                         "        for i in range(len(records)/6):\n"
                                         "            recStart = i*6\n"
                                         "            retval['DTCAndSeverityRecord'].append({'DTCSeverity':records[recStart:recStart+1],'DTCFunctionalUnit':records[recStart+1:recStart+2],'DTC':records[recStart+2:recStart+5],'statusOfDTC':records[recStart+5:recStart+6]})\n"
                                         "\n"
                                         "    return retval")
							
							
class ReadDTCMethodFactory(IServiceMethodFactory):

    ##
    # @brief method to create the request function for the service element
    @staticmethod
    def create_requestFunction(diagServiceElement, xmlElements):
        # Note: due to the compleixty of the call, this one is partially hardcoded - we do at least check the ODX file far enough to ensure that the request and subfunction are accurate.
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
            elif(semantic == 'SUBFUNCTION'):
                shortName += param.find('SHORT-NAME').text
                subfunction = DecodeFunctions.intArrayToIntArray([int(param.find('CODED-VALUE').text)], 'int16', 'int8')

        funcString = requestFuncTemplate.format(shortName,
                                                serviceId,
                                                subfunction)
        exec(funcString)
        return locals()[shortName]

    ##
    # @brief method to create the function to check the positive response for validity
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
