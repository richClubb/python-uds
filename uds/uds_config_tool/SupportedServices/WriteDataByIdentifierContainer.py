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


class WriteDataByIdentifierContainer(object):

    __metaclass__ = iContainer

    def __init__(self):
        self.requestFunctions = {}
        self.checkFunctions = {}
        self.negativeResponseFunctions = {}
        self.positiveResponseFunctions = {}

    ##
    # @brief this method is bound to an external Uds object, referenced by target, so that it can be called
    # as one of the in-built methods. uds.writeDataByIdentifier("something","data record") It does not operate
    # on this instance of the container class.
    @staticmethod
    def __writeDataByIdentifier(target, parameter, dataRecord, **kwargs):

        # Note: WDBI does not show support for multiple DIDs in the spec, so this is handling only a single DID with data record.
        requestFunction = target.writeDataByIdentifierContainer.requestFunctions[parameter]
        checkFunction = target.writeDataByIdentifierContainer.checkFunctions[parameter]
        negativeResponseFunction = target.writeDataByIdentifierContainer.negativeResponseFunctions[parameter]
        positiveResponseFunction = target.writeDataByIdentifierContainer.positiveResponseFunctions[parameter]

        # Call the sequence of functions to execute the RDBI request/response action ...
        # ==============================================================================

        # Create the request. Note: we do not have to pre-check the dataRecord as this action is performed by 
        # the recipient (the response codes 0x13 and 0x31 provide the necessary cover of errors in the request) ...
        request = requestFunction(dataRecord)

        # Send request and receive the response ...
        response = target.send(request) # ... this returns a single response
        negativeResponseFunction(response)  # ... throws an exception to be handled at a higher level if a negative response is received

        # We have a positive response so check that it makes sense to us ...
        checkFunction(response)

        # All is still good, so return the response (currently this function does nothing, but including it here as a hook in case that changes) ...
        return positiveResponseFunction(response)

    def bind_function(self, bindObject):
        bindObject.writeDataByIdentifier = MethodType(self.__writeDataByIdentifier, bindObject)

    def add_requestFunction(self, aFunction, dictionaryEntry):
        self.requestFunctions[dictionaryEntry] = aFunction

    def add_checkFunction(self, aFunction, dictionaryEntry):
        self.checkFunctions[dictionaryEntry] = aFunction

    def add_negativeResponseFunction(self, aFunction, dictionaryEntry):
        self.negativeResponseFunctions[dictionaryEntry] = aFunction

    def add_positiveResponseFunction(self, aFunction, dictionaryEntry):
        self.positiveResponseFunctions[dictionaryEntry] = aFunction