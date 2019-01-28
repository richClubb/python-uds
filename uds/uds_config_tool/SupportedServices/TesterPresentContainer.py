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


class TesterPresentContainer(object):

    __metaclass__ = iContainer

    def __init__(self):
        self.requestFunctions = {}
        self.checkFunctions = {}
        self.negativeResponseFunctions = {}
        self.positiveResponseFunctions = {}

    ##
    # @brief this method is bound to an external Uds object, referenced by target, so that it can be called
    # as one of the in-built methods. uds.testerPresentContainer() It does not operate
    # on this instance of the container class.
    @staticmethod
    def __testerPresent(target, suppressResponse=False, disable=False, **kwargs):

        # If the disable flag is set, we do nothing but remove any testerPresent behaviour for the current session
        if disable:
            target.testerPresentDisable() # ... see diagnostic session control container
            return

        # Note: testerPresentContainer has no DID required and only supports a zeroSubFunction in order to support response suppression.
        requestFunction = target.testerPresentContainer.requestFunctions["TesterPresent"]
        if "TesterPresent" in target.testerPresentContainer.checkFunctions:
            checkFunction = target.testerPresentContainer.checkFunctions["TesterPresent"]
        else:
            checkFunction = None
        negativeResponseFunction = target.testerPresentContainer.negativeResponseFunctions["TesterPresent"]
        if "TesterPresent" in target.testerPresentContainer.positiveResponseFunctions:
            positiveResponseFunction = target.testerPresentContainer.positiveResponseFunctions["TesterPresent"]
        else:
            positiveResponseFunction = None

        # Call the sequence of functions to execute the Tester Present request/response action ...
        # ==============================================================================

        if checkFunction is None or positiveResponseFunction is None:
            suppressResponse = True

        # Create the request ...
        request = requestFunction(suppressResponse)

        if suppressResponse == False:
            # Send request and receive the response ...
            response = target.send(request,responseRequired=True) # ... this returns a single response
            negativeResponseFunction(response)  # ... throws an exception to be handled at a higher level if a negative response is received

            # We have a positive response so check that it makes sense to us ...
            checkFunction(response)

            # All is still good, so return the response (currently this function does nothing, but including it here as a hook in case that changes) ...
            return positiveResponseFunction(response)
			
		# ... else ...
        # Send request and receive the response ...
        response = target.send(request,responseRequired=False) # ... this suppresses any response handling (not expected)
        return

    def bind_function(self, bindObject):
        bindObject.testerPresent = MethodType(self.__testerPresent, bindObject)

    def add_requestFunction(self, aFunction, dictionaryEntry):
        if aFunction is not None: # ... allow for a send only version being processed
            self.requestFunctions["TesterPresent"] = aFunction

    def add_checkFunction(self, aFunction, dictionaryEntry):
        if aFunction is not None: # ... allow for a send only version being processed
            self.checkFunctions["TesterPresent"] = aFunction

    def add_negativeResponseFunction(self, aFunction, dictionaryEntry):
        if aFunction is not None: # ... allow for a send only version being processed
            self.negativeResponseFunctions["TesterPresent"] = aFunction

    def add_positiveResponseFunction(self, aFunction, dictionaryEntry):
        if aFunction is not None: # ... allow for a send only version being processed
            self.positiveResponseFunctions["TesterPresent"] = aFunction