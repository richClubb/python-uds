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


class RequestDownloadContainer(object):

    __metaclass__ = iContainer

    def __init__(self):
        self.requestFunctions = {}
        self.checkFunctions = {}
        self.negativeResponseFunctions = {}
        self.positiveResponseFunctions = {}

    ##
    # @brief this method is bound to an external Uds object, referenced by target, so that it can be called
    # as one of the in-built methods. uds.requestDownload("something","data record") It does not operate
    # on this instance of the container class.
    @staticmethod
    def __requestDownload(target, FormatIdentifier, MemoryAddress, MemorySize, **kwargs):

        # Note: RequestDownload does not show support for multiple DIDs in the spec, so this is handling only a single DID with data record.
        requestFunction = target.requestDownloadContainer.requestFunctions['RequestDownload']
        checkFunction = target.requestDownloadContainer.checkFunctions['RequestDownload']
        negativeResponseFunction = target.requestDownloadContainer.negativeResponseFunctions['RequestDownload']
        positiveResponseFunction = target.requestDownloadContainer.positiveResponseFunctions['RequestDownload']

        # Call the sequence of functions to execute the request download request/response action ...
        # ==============================================================================

        if checkFunction is None or positiveResponseFunction is None:
            suppressResponse = True

        # Create the request. Note: we do not have to pre-check the dataRecord as this action is performed by 
        # the recipient (the response codes 0x13 and 0x31 provide the necessary cover of errors in the request) ...
        request = requestFunction(FormatIdentifier, MemoryAddress, MemorySize)

        # Send request and receive the response ...
        response = target.send(request,responseRequired=True) # ... this returns a single response
        nrc = negativeResponseFunction(response)  # ... return nrc value if a negative response is received
        if nrc:
            return nrc

        # We have a positive response so check that it makes sense to us ...
        checkFunction(response)

        # All is still good, so return the response (currently this function does nothing, but including it here as a hook in case that changes) ...
        return positiveResponseFunction(response)


    def bind_function(self, bindObject):
        bindObject.requestDownload = MethodType(self.__requestDownload, bindObject)

    def add_requestFunction(self, aFunction, dictionaryEntry):  # ... dictionaryEntry is not used (just there for consistency in UdsConfigTool.py) - i.e. this service is effectively hardcoded
        self.requestFunctions['RequestDownload'] = aFunction

    def add_checkFunction(self, aFunction, dictionaryEntry):  # ... dictionaryEntry is not used (just there for consistency in UdsConfigTool.py) - i.e. this service is effectively hardcoded
        self.checkFunctions['RequestDownload'] = aFunction

    def add_negativeResponseFunction(self, aFunction, dictionaryEntry):  # ... dictionaryEntry is not used (just there for consistency in UdsConfigTool.py) - i.e. this service is effectively hardcoded
        self.negativeResponseFunctions['RequestDownload'] = aFunction

    def add_positiveResponseFunction(self, aFunction, dictionaryEntry):  # ... dictionaryEntry is not used (just there for consistency in UdsConfigTool.py) - i.e. this service is effectively hardcoded
        self.positiveResponseFunctions['RequestDownload'] = aFunction