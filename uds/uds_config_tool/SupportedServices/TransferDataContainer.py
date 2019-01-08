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


class TransferDataContainer(object):

    __metaclass__ = iContainer

    def __init__(self):
        self.requestFunctions = {}
        self.checkFunctions = {}
        self.negativeResponseFunctions = {}
        self.positiveResponseFunctions = {}
 

    ##
    # @brief this method is bound to an external Uds object, referenced by target, so that it can be called
    # as one of the in-built methods. uds.transferData("something","something else") It does not operate
    # on this instance of the container class.
    @staticmethod
    def __transferData(target, blockSequenceCounter=None, transferRequestParameterRecord=None, transferBlock=None, transferBlocks=None, **kwargs):

        def transferChunks(transmitChunks):
            retval = None
            for i in range(len(transmitChunks)):
                retval = target.transferData(i+1, transmitChunks[i])
            return retval

        # Adding an option to send all chunks in a block (note, this could be separated off into a separate methid if required, but this is the only one bound at present)
        if transferBlock is not None:
            return transferChunks(transferBlock.transmitChunks())

        # Adding an option to send all chunks in an ihex file (note, this could be separated off into a separate methid if required, but this is the only one bound at present)
        if transferBlocks is not None:
            return transferChunks(transferBlocks.transmitChunks())

        # Note: transferData does not show support for multiple DIDs in the spec, so this is handling only a single DID with data record.
        requestFunction = target.transferDataContainer.requestFunctions['TransferData']
        checkFunction = target.transferDataContainer.checkFunctions['TransferData']
        negativeResponseFunction = target.transferDataContainer.negativeResponseFunctions['TransferData']
        positiveResponseFunction = target.transferDataContainer.positiveResponseFunctions['TransferData']

        # Call the sequence of functions to execute the ECU Reset request/response action ...
        # ==============================================================================

        # Create the request. Note: we do not have to pre-check the dataRecord as this action is performed by 
        # the recipient (the response codes 0x?? and 0x?? provide the necessary cover of errors in the request) ...
        request = requestFunction(blockSequenceCounter,transferRequestParameterRecord)


        # Send request and receive the response ...
        response = target.send(request,responseRequired=True) # ... this returns a single response
        negativeResponseFunction(response)  # ... throws an exception to be handled at a higher level if a negative response is received

        # We have a positive response so check that it makes sense to us ...
        checkFunction(response)

        # All is still good, so return the response (currently this function does nothing, but including it here as a hook in case that changes) ...
        return positiveResponseFunction(response)


    def bind_function(self, bindObject):
        bindObject.transferData = MethodType(self.__transferData, bindObject)

    def add_requestFunction(self, aFunction, dictionaryEntry):  # ... dictionaryEntry is not used (just there for consistency in UdsConfigTool.py) - i.e. this service is effectively hardcoded
        self.requestFunctions['TransferData'] = aFunction

    def add_checkFunction(self, aFunction, dictionaryEntry):  # ... dictionaryEntry is not used (just there for consistency in UdsConfigTool.py) - i.e. this service is effectively hardcoded
        self.checkFunctions['TransferData'] = aFunction

    def add_negativeResponseFunction(self, aFunction, dictionaryEntry):  # ... dictionaryEntry is not used (just there for consistency in UdsConfigTool.py) - i.e. this service is effectively hardcoded
        self.negativeResponseFunctions['TransferData'] = aFunction

    def add_positiveResponseFunction(self, aFunction, dictionaryEntry):  # ... dictionaryEntry is not used (just there for consistency in UdsConfigTool.py) - i.e. this service is effectively hardcoded
        self.positiveResponseFunctions['TransferData'] = aFunction