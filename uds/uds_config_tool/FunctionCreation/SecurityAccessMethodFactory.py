#!/usr/bin/env python

__author__ = "Richard Clubb"
__copyrights__ = "Copyright 2018, the python-uds project"
__credits__ = ["Richard Clubb"]

__license__ = "MIT"
__maintainer__ = "Richard Clubb"
__email__ = "richard.clubb@embeduk.com"
__status__ = "Development"


from uds.uds_config_tool.FunctionCreation.iServiceMethodFactory import IServiceMethodFactory
from uds.uds_config_tool.UtilityFunctions import getSdgsDataItem, getSdgsData, getShortName, getLongName, \
                                                 getServiceIdFromDiagService, getParamWithSemantic, \
                                                 getPositiveResponse, getDiagObjectProp, getBitLengthFromDop
from math import ceil

##
# Inputs
# Function name
# expected security response
requestFuncTemplate_getSeed = str("def {0}(suppressResponse=False):\n"
                                  "    securityRequest = {2}\n"
                                  "    if suppressResponse: securityRequest |= 0x80\n"
                                  "    return [{1}, securityRequest]"
                                  )

requestFuncTemplate_sendKey = str("def {0}(key, suppressResponse=False):\n"
                                  "    serviceId = {1}\n"
                                  "    subFunction = {2}\n"
                                  "    if suppressResponse: subFunction |= 0x80\n"
                                  "    return [serviceId, subFunction] + key")

checkSidTemplate = str("def {0}(sid):\n"
                       "    expectedSid = {1}\n"
                       "    if expectedSid != sid: raise Exception(\"SID do not match\")"
                       )

checkSecurityAccessTemplate = str("def {0}(securityAccess):\n"
                                  "    expectedSecurityAccess = {1}\n"
                                  "    if expectedSecurityAccess != securityAccess: raise Exception(\"Security Mode does not match\")"
                                  )

checkReturnedDataTemplate = str("def {0}(data):\n"
                               "    expectedDataLength = {1}\n"
                               "    if expectedDataLength != len(data): raise Exception(\"Returned data length not expected\")"
                               )

checkNegativeResponseTemplate = str("def {0}(data):\n"
                                    "    if data[0] == 0x7F: raise Exception(\"Found negative response\")"
                                    )

##
# inputs:
# Length
checkInputDataTemplate = str("def {0}(data):\n"
                             "    expectedLength = {1}\n"
                             "    if isinstance(data, list):\n"
                             "        if len(data) != expectedLength: raise Exception(\"Input data does not match expected length\")\n"
                             "    else:"
                             "        pass")

class SecurityAccessMethodFactory(object):

    __metaclass__ = IServiceMethodFactory

    ##
    # @brief method to create the request function for the service element
    @staticmethod
    def create_requestFunction(diagServiceElement, xmlElements):
        serviceId = 0x00
        securityRequest = 0x00

        # have to dig out the sgds name for this one
        requestElement = xmlElements[diagServiceElement.find('REQUEST-REF').attrib['ID-REF']]

        sdgsName = getSdgsDataItem(diagServiceElement, "DiagInstanceQualifier")

        serviceId = getServiceIdFromDiagService(diagServiceElement, xmlElements)
        accessMode = getParamWithSemantic(requestElement, "ACCESSMODE")
        subfunction = getParamWithSemantic(requestElement, "SUBFUNCTION")

        # if accessMode is not none then this is a seed request
        if accessMode is not None:
            securityRequest = int(getParamWithSemantic(requestElement, "ACCESSMODE").find("CODED-VALUE").text)
            requestFuncString = requestFuncTemplate_getSeed.format(sdgsName, serviceId, securityRequest)
        elif subfunction is not None:
            securityRequest = int(getParamWithSemantic(requestElement, "SUBFUNCTION").find("CODED-VALUE").text)
            requestFuncString = requestFuncTemplate_sendKey.format(sdgsName, serviceId, securityRequest)
        else:
            requestFuncString = None

        if requestFuncString is not None:
            exec(requestFuncString)
            return locals()[sdgsName]
        else:
            return None

    ##
    # @brief method to create the function to check the positive response for validity
    @staticmethod
    def create_checkPositiveResponseFunction(diagServiceElement, xmlElements):
        responseId = 0
        securityRequest = 0

        responseId = getServiceIdFromDiagService(diagServiceElement, xmlElements) + 0x40
        positiveResponseElement = getPositiveResponse(diagServiceElement, xmlElements)

        diagInstanceQualifier = getSdgsDataItem(diagServiceElement, "DiagInstanceQualifier")

        checkSidFunctionName = "check_{0}_sid".format(diagInstanceQualifier)
        checkSecurityAccessFunctionName = "check_{0}_securityAccess".format(diagInstanceQualifier)
        checkReturnedDataFunctionName = "check_{0}_returnedData".format(diagInstanceQualifier)

        accessmode = getParamWithSemantic(positiveResponseElement, "ACCESSMODE")
        subfunction = getParamWithSemantic(positiveResponseElement, "SUBFUNCTION")

        if accessmode is not None:
            securityRequest = int(accessmode.find("CODED-VALUE").text)
        elif subfunction is not None:
            securityRequest = int(subfunction.find("CODED-VALUE").text)
        else:
            raise Exception("Format not known")

        dataParams = getParamWithSemantic(positiveResponseElement, "DATA")

        if dataParams is not None:
            if isinstance(dataParams, list):
                raise Exception("Currently can not deal with lists of data")
            else:
                dop = getDiagObjectProp(dataParams, xmlElements)
                bitLength = getBitLengthFromDop(dop)
                payloadLength = int(ceil(bitLength / 8))
        else:
            payloadLength = 0

        checkSidFunctionString = checkSidTemplate.format(checkSidFunctionName,
                                                         responseId
                                                         )

        checkSecurityAccessFunctionString = checkSecurityAccessTemplate.format(checkSecurityAccessFunctionName,
                                                                               securityRequest)

        if payloadLength == 0:
            checkReturnedDataString = None
        else:
            checkReturnedDataString = checkReturnedDataTemplate.format(checkReturnedDataFunctionName,
                                                                       payloadLength)
            exec(checkReturnedDataString)

        exec(checkSidFunctionString)
        exec(checkSecurityAccessFunctionString)

        checkSidFunction = locals()[checkSidFunctionName]
        checkSecurityAccessFunction = locals()[checkSecurityAccessFunctionName]

        checkReturnedDataFunction = None
        try:
            checkReturnedDataFunction = locals()[checkReturnedDataFunctionName]
        except:
            pass

        return checkSidFunction, checkSecurityAccessFunction, checkReturnedDataFunction

    ##
    # @brief method to encode the positive response from the raw type to it physical representation
    @staticmethod
    def create_encodePositiveResponseFunction(diagServiceElement, xmlElements):

        raise Exception("Not implemented")

    ##
    # @brief method to create the negative response function for the service element
    @staticmethod
    def create_checkNegativeResponseFunction(diagServiceElement, xmlElements):

        diagInstanceQualifier = getSdgsDataItem(diagServiceElement, "DiagInstanceQualifier")

        checkNegativeResponseFunctionName = "check_{0}_negResponse".format(diagInstanceQualifier)

        checkNegativeResponseFunctionString = checkNegativeResponseTemplate.format(checkNegativeResponseFunctionName)

        exec(checkNegativeResponseFunctionString)

        return locals()[checkNegativeResponseFunctionName]

    @staticmethod
    def check_inputDataFunction(diagServiceElement, xmlElements):

        diagInstanceQualifier = getSdgsDataItem(diagServiceElement, "DiagInstanceQualifier")


if __name__ == "__main__":

    pass
