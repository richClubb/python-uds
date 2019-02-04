#!/usr/bin/env python

__author__ = "Richard Clubb"
__copyrights__ = "Copyright 2018, the python-uds project"
__credits__ = ["Richard Clubb"]

__license__ = "MIT"
__maintainer__ = "Richard Clubb"
__email__ = "richard.clubb@embeduk.com"
__status__ = "Development"


defaultTPTimeout = 10  # ... (s): default to sending tester present 10s after last request (if required) - note: this includes after previous TesterPresent for repeating operation

from uds.uds_config_tool.SupportedServices.iContainer import iContainer
from types import MethodType
import time


class DiagnosticSessionControlContainer(object):
    __metaclass__ = iContainer

    def __init__(self):
        self.requestFunctions = {}
        self.checkFunctions = {}
        self.negativeResponseFunctions = {}
        self.positiveResponseFunctions = {}

        self.testerPresent = {}
        self.currentSession = None
        self.lastSend = None
		
    ##
    # @brief this method is bound to an external Uds object, referenced by target, so that it can be called
    # as one of the in-built methods. uds.diagnosticSessionControl("session type") It does not operate
    # on this instance of the container class.
    @staticmethod
    def __diagnosticSessionControl(target, parameter, suppressResponse=False, testerPresent=False, tpTimeout=defaultTPTimeout, **kwargs):

        # Note: diagnosticSessionControl does not show support for multiple DIDs in the spec, so this is handling only a single DID with data record.
        requestFunction = target.diagnosticSessionControlContainer.requestFunctions[parameter]
        if parameter in target.diagnosticSessionControlContainer.checkFunctions:
            checkFunction = target.diagnosticSessionControlContainer.checkFunctions[parameter]
        else:
            checkFunction = None
        negativeResponseFunction = target.diagnosticSessionControlContainer.negativeResponseFunctions[parameter]
        positiveResponseFunction = target.diagnosticSessionControlContainer.positiveResponseFunctions[parameter]
        if parameter in target.diagnosticSessionControlContainer.positiveResponseFunctions:
            positiveResponseFunction = target.diagnosticSessionControlContainer.positiveResponseFunctions[parameter]
        else:
            positiveResponseFunction = None

        # Call the sequence of functions to execute the Diagnostic Session Control request/response action ...
        # ==============================================================================
		
        # Code additions to support interaction with tester present for a given diagnostic session ...
        target.diagnosticSessionControlContainer.currentSession = parameter
		# Note: if testerPresent is set, then timeout is checked every second, so timeout values less than second will always be equivalent to one second.
        target.diagnosticSessionControlContainer.testerPresent[parameter] = {'reqd': True,'timeout':tpTimeout} if testerPresent else {'reqd': False,'timeout':None}
        # Note: lastSend is initialised via a call to __sessionSetLastSend() when send is called
        if testerPresent:
            target.testerPresentThread()

        if checkFunction is None or positiveResponseFunction is None:  # ... i.e. we only have a send_only service specified in the ODX
            suppressResponse = True

        # Create the request. Note: we do not have to pre-check the dataRecord as this action is performed by 
        # the recipient (the response codes 0x?? and 0x?? provide the necessary cover of errors in the request) ...
        request = requestFunction(suppressResponse)

        if suppressResponse == False:        # Send request and receive the response ...
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

    ##
    # @brief this method is bound to an external Uds object, referenced by target, so that it can be called
    # as one of the in-built methods. uds.testerPresentSessionRecord() It does not operate
    # on this instance of the container class.
    # The purpose of this method is to inform the caller of requirement for tester present messages, and if required, at what frequency (in ms)
    @staticmethod
    def __testerPresentSessionRecord(target, **kwargs):
        sessionType = target.diagnosticSessionControlContainer.currentSession
        if sessionType is None:
            sessionType = 'Default Session'
        return target.diagnosticSessionControlContainer.testerPresent[sessionType] if sessionType in target.diagnosticSessionControlContainer.testerPresent else {'reqd': False,'timeout':None}

    ##
    # @brief this method is bound to an external Uds object, referenced by target, so that it can be called
    # as one of the in-built methods. uds.testerPresentSessionRecord() It does not operate
    # on this instance of the container class.
    # The purpose of this method is to record the last send time (any message) for the current diagnostic session.
    @staticmethod
    def __sessionSetLastSend(target, **kwargs):
        target.diagnosticSessionControlContainer.lastSend = int(round(time.time()))  # ... in seconds

    ##
    # @brief this method is bound to an external Uds object, referenced by target, so that it can be called
    # as one of the in-built methods. uds.testerPresentSessionRecord() It does not operate
    # on this instance of the container class.
    # The purpose of this method is to record the last send time (any message) for the current diagnostic session.
    @staticmethod
    def __testerPresentDisable(target, **kwargs):
        sessionType = target.diagnosticSessionControlContainer.currentSession
        if sessionType is None:
            sessionType = 'Default Session'
        target.diagnosticSessionControlContainer.testerPresent[sessionType] = {'reqd': False,'timeout':None}
        target.diagnosticSessionControlContainer.lastSend = None

    ##
    # @brief this method is bound to an external Uds object, referenced by target, so that it can be called
    # as one of the in-built methods. uds.testerPresentSessionRecord() It does not operate
    # on this instance of the container class.
    # The purpose of this method is to inform the caller of the time (in seconds) since the last message was sent for the current diagnostic session.
    @staticmethod
    def __sessionTimeSinceLastSend(target, **kwargs):
        now = int(round(time.time()))  # ... in seconds
        try:
            return (now - target.diagnosticSessionControlContainer.lastSend)
        except:
            return 0

    def bind_function(self, bindObject):
        bindObject.diagnosticSessionControl = MethodType(self.__diagnosticSessionControl, bindObject)
        # Adding an additional functions to allow internal requests to process testerPresent behaviour required for the diagnostic session ...
        bindObject.testerPresentSessionRecord = MethodType(self.__testerPresentSessionRecord, bindObject)
        bindObject.sessionSetLastSend = MethodType(self.__sessionSetLastSend, bindObject)
        bindObject.testerPresentDisable = MethodType(self.__testerPresentDisable, bindObject)
        bindObject.sessionTimeSinceLastSend = MethodType(self.__sessionTimeSinceLastSend, bindObject)

    def add_requestFunction(self, aFunction, dictionaryEntry):
        if aFunction is not None: # ... allow for a send only version being processed
            self.requestFunctions[dictionaryEntry] = aFunction

    def add_checkFunction(self, aFunction, dictionaryEntry):
        if aFunction is not None: # ... allow for a send only version being processed
            self.checkFunctions[dictionaryEntry] = aFunction

    def add_negativeResponseFunction(self, aFunction, dictionaryEntry):
        if aFunction is not None: # ... allow for a send only version being processed
            self.negativeResponseFunctions[dictionaryEntry] = aFunction

    def add_positiveResponseFunction(self, aFunction, dictionaryEntry):
        if aFunction is not None: # ... allow for a send only version being processed
            self.positiveResponseFunctions[dictionaryEntry] = aFunction

