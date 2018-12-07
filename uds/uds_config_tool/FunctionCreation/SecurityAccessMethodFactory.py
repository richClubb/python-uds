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
                                                 getPositiveResponse


requestFuncTemplate_getSeed = str("def {0}(suppressResponse=False):\n"
                                  "    securityRequest = {2}\n"
                                  "    if suppressResponse: securityRequest |= 0x80\n"
                                  "    return [{1}, securityRequest]"
                                  )

requestFuncTemplate_sendKey = str("def {0}(key):\n"
                                  "    serviceId = {1}\n"
                                  "    subFunction = {2}\n"
                                  "    return [serviceId, subFunction] + key")


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
            print(requestFuncString)
        elif subfunction is not None:
            securityRequest = int(getParamWithSemantic(requestElement, "SUBFUNCTION").find("CODED-VALUE").text)
            requestFuncString = requestFuncTemplate_sendKey.format(sdgsName, serviceId, securityRequest)
            print(requestFuncString)
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

        positiveResponseElement = getPositiveResponse(diagServiceElement, xmlElements)

        responseId = int(getParamWithSemantic(positiveResponseElement, "SERVICE-ID").find("CODED-VALUE").text)

        

        pass



    ##
    # @brief method to encode the positive response from the raw type to it physical representation
    @staticmethod
    def create_encodePositiveResponseFunction(diagServiceElement, xmlElements):
        pass

    ##
    # @brief method to create the negative response function for the service element
    @staticmethod
    def create_checkNegativeResponseFunction(diagServiceElement, xmlElements):
        pass

if __name__ == "__main__":

    pass