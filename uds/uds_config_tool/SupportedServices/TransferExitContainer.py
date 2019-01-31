#!/usr/bin/env python

__author__ = "Richard Clubb"
__copyrights__ = "Copyright 2018, the python-uds project"
__credits__ = ["Richard Clubb"]

__license__ = "MIT"
__maintainer__ = "Richard Clubb"
__email__ = "richard.clubb@embeduk.com"
__status__ = "Development"


from uds.uds_config_tool.SupportedServices.iContainer import iContainer
from types import MethodType


class TransferExitContainer(object):

    __metaclass__ = iContainer

    def __init__(self):
        self.requestFunctions = {}
        self.checkFunctions = {}
        self.negativeResponseFunctions = {}
        self.positiveResponseFunctions = {}
 

    ##
    # @brief this method is bound to an external Uds object, referenced by target, so that it can be called
    # as one of the in-built methods. uds.transferExit("something") It does not operate
    # on this instance of the container class.
    @staticmethod
    def __transferExit(target, transferRequestParameterRecord=None, **kwargs):

        # Note: TransferExit does not show support for multiple DIDs in the spec, so this is handling only a single DID with data record.
        requestFunction = target.transferExitContainer.requestFunctions['TransferExit']
        checkFunction = target.transferExitContainer.checkFunctions['TransferExit']
        negativeResponseFunction = target.transferExitContainer.negativeResponseFunctions['TransferExit']
        positiveResponseFunction = target.transferExitContainer.positiveResponseFunctions['TransferExit']

        # Call the sequence of functions to execute the ECU Reset request/response action ...
        # ==============================================================================

        # Create the request. Note: we do not have to pre-check the dataRecord as this action is performed by 
        # the recipient (the response codes 0x?? and 0x?? provide the necessary cover of errors in the request) ...
        request = requestFunction(transferRequestParameterRecord)

        # Send request and receive the response ...
        response = target.send(request,responseRequired=True) # ... this returns a single response
        negativeResponseFunction(response)  # ... throws an exception to be handled at a higher level if a negative response is received

        # We have a positive response so check that it makes sense to us ...
        checkFunction(response)

        # All is still good, so return the response (currently this function does nothing, but including it here as a hook in case that changes) ...
        return positiveResponseFunction(response)


    def bind_function(self, bindObject):
        bindObject.transferExit = MethodType(self.__transferExit, bindObject)

    def add_requestFunction(self, aFunction, dictionaryEntry):  # ... dictionaryEntry is not used (just there for consistency in UdsConfigTool.py) - i.e. this service is effectively hardcoded
        self.requestFunctions['TransferExit'] = aFunction

    def add_checkFunction(self, aFunction, dictionaryEntry):  # ... dictionaryEntry is not used (just there for consistency in UdsConfigTool.py) - i.e. this service is effectively hardcoded
        self.checkFunctions['TransferExit'] = aFunction

    def add_negativeResponseFunction(self, aFunction, dictionaryEntry):  # ... dictionaryEntry is not used (just there for consistency in UdsConfigTool.py) - i.e. this service is effectively hardcoded
        self.negativeResponseFunctions['TransferExit'] = aFunction

    def add_positiveResponseFunction(self, aFunction, dictionaryEntry):  # ... dictionaryEntry is not used (just there for consistency in UdsConfigTool.py) - i.e. this service is effectively hardcoded
        self.positiveResponseFunctions['TransferExit'] = aFunction