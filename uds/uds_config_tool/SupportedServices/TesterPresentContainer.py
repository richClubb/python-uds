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
import threading
import time


class TesterPresentContainer(object):

    __metaclass__ = iContainer
	
    testerPresentThreadRef = None
    testerPresentTargets = set()

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
    def __testerPresent(target, suppressResponse=True, disable=False, **kwargs):

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


    ##
    # @brief this method is bound to an external Uds object, referenced by target, so that it can be called
    # as one of the in-built methods. uds.testerPresentThread() It does not operate
    # on this instance of the container class.
    # Important Note: we always keep a single thread running in the background monitoring the testerPresent requirements.
    # As this is static, and we can have many ECU connections via different UDS instances, this means we need to check them all!
    @staticmethod
    def __testerPresentThread(target, **kwargs):

        def __tpWorker():
            #print("work thread started (should be once only)")
            while True:
                #print("inside worker loop")
                for tgt in TesterPresentContainer.testerPresentTargets:
                    try:
                        transmitting = tgt.isTransmitting()
                    except:
                        continue  # ... there's a problem with the stored target - e.g. target no longer in use, so a dead reference - so skip it
                    # ... otherwise we continue outside of the try/except block to avoid trapping any exceptions that may need to be propagated upwards
                    #print("target found")
                    if not transmitting:
                        #print("target not transmitting")
                        tpSessionRecord = tgt.testerPresentSessionRecord()
                        if tpSessionRecord['reqd']: # ... testPresent behaviour is required for the current diagnostic session
                            #print("tp required for target")
                            if tgt.sessionTimeSinceLastSend() >= tpSessionRecord['timeout']:
                                #print("timed out! - sending test present")
                                tgt.testerPresent()
                if not threading.main_thread().is_alive():
                    return
                time.sleep(1.0) # ... check if tester present is required every 1s (we are unlikely to require finer granularity).
                # Note: I'm avoiding direct wait mechanisms (of testerPresent TO) to allow for radical difference in behaviour for changing diagnostic sessions.
                # This can of course be changed.

        TesterPresentContainer.testerPresentTargets.add(target) # ... track a list of all possible concurrent targets, as we process tester present for all targets via one thread
        if TesterPresentContainer.testerPresentThreadRef is None:
            TesterPresentContainer.testerPresentThreadRef = threading.Thread(name='tpWorker', target=__tpWorker)
            TesterPresentContainer.testerPresentThreadRef.start()


    def bind_function(self, bindObject):
        bindObject.testerPresent = MethodType(self.__testerPresent, bindObject)
        bindObject.testerPresentThread = MethodType(self.__testerPresentThread, bindObject)

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