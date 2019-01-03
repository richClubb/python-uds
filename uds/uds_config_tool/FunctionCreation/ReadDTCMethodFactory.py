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


# Note: the request is not the simplest to parse from the ODX, so paritally hardcoding this one again (for now at least)
requestFuncTemplate = str("def {0}(DTCStatusMask=[],DTCMaskRecord=[],DTCSnapshotRecordNumber=[],DTCExtendedRecordNumber=[],DTCSeverityMask=[]):\n"
                          "    encoded = []\n"
                          "    {3}\n"
                          "    return {1} + {2} + encoded # ... SID, sub-func, and params")

checkFunctionTemplate = str("def {0}(input):\n"
                            "    serviceIdExpected = {1}\n"
                            "    subFunctionExpected = {2}\n"
                            "    serviceId = DecodeFunctions.buildIntFromList(input[{3}:{4}])\n"
                            "    subFunction = DecodeFunctions.buildIntFromList(input[{5}:{6}])\n"
                            "    if(serviceId != serviceIdExpected): raise Exception(\"Service Id Received not expected. Expected {{0}}; Got {{1}} \".format(serviceIdExpected, serviceId))\n"
                            "    if(subFunction != subFunctionExpected): raise Exception(\"Sub-function Received not expected. Expected {{0}}; Got {{1}} \".format(subFunctionExpected, subFunction))\n"
                            "{7}")

negativeResponseFuncTemplate = str("def {0}(input):\n"
                                   "    {1}")

encodePositiveResponseFuncTemplate = str("def {0}(input):\n"
                                         "    encoded = []\n"
                                         "    retval = None\n"
                                         "{1}\n"
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
        encodeString = ""

        for param in paramsElement:
            semantic = None
            try:
                semantic = param.attrib['SEMANTIC']
            except AttributeError:
                pass
            except KeyError:
                pass

            if(semantic == 'SERVICE-ID'):
                serviceId = [int(param.find('CODED-VALUE').text)]
            elif(semantic == 'SUBFUNCTION'):
                shortName += param.find('SHORT-NAME').text
                subfunction = DecodeFunctions.intArrayToIntArray([int(param.find('CODED-VALUE').text)], 'int8', 'int8')
                if subfunction[0] in [0x01,0x02, 0x0F, 0x11, 0x12, 0x13]: # ... DTCStatusMask required for these subfunctions
                    encodeString = "encoded += DTCStatusMask"
                elif subfunction[0] in [0x03,0x04, 0x06, 0x09, 0x10]: # ... DTCMaskRecord required for these subfunctions
                    encodeString = "encoded += DTCMaskRecord # ... format is [0xNN,0xNN,0xNN]"
                elif subfunction[0] in [0x03,0x04, 0x05]: # ... DTCSnapshotRecordNumber required for these subfunctions
                    encodeString = "encoded += DTCSnapshotRecordNumber"
                elif subfunction[0] in [0x06,0x10]: # ... DTCExtendedRecordNumber required for these subfunctions
                    encodeString = "encoded += DTCExtendedRecordNumber"
                elif subfunction[0] in [0x07,0x08]: # ... DTCSeverityMaskRecord required for these subfunctions
                    encodeString = "encoded += DTCSeverityMask+DTCStatusMask"

        funcString = requestFuncTemplate.format(shortName,
                                                serviceId,
                                                subfunction,
                                                encodeString)
        exec(funcString)
        return (locals()[shortName],str(subfunction))

    ##
    # @brief method to create the function to check the positive response for validity
    @staticmethod
    def create_checkPositiveResponseFunction(diagServiceElement, xmlElements):
        responseId = 0
        subfunction = 0

        responseIdStart = 0
        responseIdEnd = 0
        subfunctionStart = 0
        subfunctionEnd = 0

        shortName = diagServiceElement.find('SHORT-NAME').text
        checkFunctionName = "check_{0}".format(shortName)
        positiveResponseElement = xmlElements[(diagServiceElement.find('POS-RESPONSE-REFS')).find('POS-RESPONSE-REF').attrib['ID-REF']]

        paramsElement = positiveResponseElement.find('PARAMS')

        totalLength = 0
        subfunctionChecks = ""

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
                    subfunction = int(param.find('CODED-VALUE').text)
                    bitLength = int((param.find('DIAG-CODED-TYPE')).find('BIT-LENGTH').text)
                    listLength = int(bitLength / 8)
                    subfunctionStart = startByte
                    subfunctionEnd = startByte + listLength
                    totalLength += listLength

                    if subfunction in [0x02,0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F, 0x13]: # ... DTCStatusMask required for these subfunctions
                        subfunctionChecks += "    if len(input) < 3: raise Exception(\"Total length returned not as expected. Expected: greater than or equal to 3; Got {{0}}\".format(len(input)))\n"
                        subfunctionChecks += "    if (len(input)-3)%4 != 0: raise Exception(\"Total length returned not as expected. Received a partial DTC and Status Record; Got {{0}} total length\".format(len(input)))\n"
                    elif subfunction in [0x01, 0x07, 0x11, 0x12]: # ... DTCStatusMask required for these subfunctions
                        subfunctionChecks += "    if len(input) != 6: raise Exception(\"Total length returned not as expected. Expected: 6; Got {{0}}\".format(len(input)))\n"
                    elif subfunction in [0x03]: # ... DTCStatusMask required for these subfunctions
                        subfunctionChecks += "    if len(input) < 2: raise Exception(\"Total length returned not as expected. Expected: greater than or equal to 2; Got {{0}}\".format(len(input)))\n"
                        subfunctionChecks += "    if (len(input)-2)%4 != 0: raise Exception(\"Total length returned not as expected. Received a partial DTC and Snapshot Record Number; Got {{0}} total length\".format(len(input)))\n"
                    elif subfunction in [0x04]: # ... DTCStatusMask required for these subfunctions
                        subfunctionChecks += "    pass #??? ... we need to parse the ODX for DTC length detials or this one, so leaving till spoken to Richard ???\n"
                    elif subfunction in [0x05]: # ... DTCStatusMask required for these subfunctions
                        subfunctionChecks += "    pass #??? ... we need to parse the ODX for DTC length detials or this one, so leaving till spoken to Richard ???\n"
                    elif subfunction in [0x06, 0x10]: # ... DTCStatusMask required for these subfunctions
                        subfunctionChecks += "    pass #??? ... we need to parse the ODX for DTC length detials or this one, so leaving till spoken to Richard ???\n"
                    elif subfunction in [0x08, 0x09]: # ... DTCStatusMask required for these subfunctions
                        subfunctionChecks += "    if len(input) < 3: raise Exception(\"Total length returned not as expected. Expected: greater than or equal to 3; Got {{0}}\".format(len(input)))\n"
                        subfunctionChecks += "    if (len(input)-3)%6 != 0: raise Exception(\"Total length returned not as expected. Received a partial DTC and Severity Record; Got {{0}} total length\".format(len(input)))\n"

                else:
                    pass
            except:
                #print(sys.exc_info())
                pass


        checkFunctionString = checkFunctionTemplate.format(checkFunctionName, # 0
                                                           responseId, # 1
                                                           subfunction, # 2
                                                           responseIdStart, # 3
                                                           responseIdEnd, # 4
                                                           subfunctionStart, # 5
                                                           subfunctionEnd, # 6
                                                           subfunctionChecks) # 7
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
        positiveResponseElement = xmlElements[(diagServiceElement.find('POS-RESPONSE-REFS')).find('POS-RESPONSE-REF').attrib['ID-REF']]
		
        paramsElement = positiveResponseElement.find('PARAMS')
        subfunctionResponse = ""

        for param in paramsElement:
            try:
                semantic = None
                try:
                    semantic = param.attrib['SEMANTIC']
                except AttributeError:
                    pass

                if(semantic == 'SUBFUNCTION'):
                    subfunction = int(param.find('CODED-VALUE').text)
                    if subfunction in [0x02,0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F, 0x13]: # ... DTCStatusMask required for these subfunctions
                            subfunctionResponse += "    retval = {'DTCStatusAvailabilityMask':input[2:3], 'DTCAndStatusRecord':[]}\n"
                            subfunctionResponse += "    records = input[3:]\n"
                            subfunctionResponse += "    for i in range(int(len(records)/4)):\n"
                            subfunctionResponse += "        recStart = i*4\n"
                            subfunctionResponse += "        retval['DTCAndStatusRecord'].append({'DTC':records[recStart:recStart+3],'statusOfDTC':records[recStart+3:recStart+4]})\n"
                    elif subfunction in [0x01, 0x07, 0x11, 0x12]: # ... DTCStatusMask required for these subfunctions
                            subfunctionResponse += "    retval = {'DTCStatusAvailabilityMask':input[2:3], 'DTCFormatIdentifier':input[3:4], 'DTCCount':[(input[4]<<8)+input[5]]}  # ... DTCCount decoded as int16\n"
                    elif subfunction in [0x03]: # ... DTCStatusMask required for these subfunctions
                            subfunctionResponse += "    retval = []\n"
                            subfunctionResponse += "    records = input[3:]\n"
                            subfunctionResponse += "    for i in range(int(len(records)/4)):\n"
                            subfunctionResponse += "        recStart = i*4\n"
                            subfunctionResponse += "        retval.append({'DTC':records[recStart:recStart+3],'DTCSnapshotRecordNumber':records[recStart+3:recStart+4]})\n"
                    elif subfunction in [0x04]: # ... DTCStatusMask required for these subfunctions
                            subfunctionResponse += "    pass #??? ... we need to parse the ODX for DTC length detials or this one, so leaving till spoken to Richard ???\n"
                    elif subfunction in [0x05]: # ... DTCStatusMask required for these subfunctions
                            subfunctionResponse += "    pass #??? ... we need to parse the ODX for DTC length detials or this one, so leaving till spoken to Richard ???\n"
                    elif subfunction in [0x06, 0x10]: # ... DTCStatusMask required for these subfunctions
                            subfunctionResponse += "    pass #??? ... we need to parse the ODX for DTC length detials or this one, so leaving till spoken to Richard ???\n"
                    elif subfunction in [0x08, 0x09]: # ... DTCStatusMask required for these subfunctions
                            subfunctionResponse += "    retval = {'DTCStatusAvailabilityMask':input[2:3], 'DTCAndSeverityRecord':[]}\n"
                            subfunctionResponse += "    records = input[3:]\n"
                            subfunctionResponse += "    for i in range(int(len(records)/6)):\n"
                            subfunctionResponse += "        recStart = i*6\n"
                            subfunctionResponse += "        retval['DTCAndSeverityRecord'].append({'DTCSeverity':records[recStart:recStart+1],'DTCFunctionalUnit':records[recStart+1:recStart+2],'DTC':records[recStart+2:recStart+5],'statusOfDTC':records[recStart+5:recStart+6]})\n"
            except:
                pass


        encodeFunctionString = encodePositiveResponseFuncTemplate.format(encodePositiveResponseFunctionName, # 0
                                                                         subfunctionResponse) # 1
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
