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


class ReadDTCContainer(object):

    __metaclass__ = iContainer

    def __init__(self):
        self.requestFunctions = {}
        self.checkFunctions = {}
        self.negativeResponseFunctions = {}
        self.positiveResponseFunctions = {}

    ##
    # @brief this method is bound to an external Uds object, referenced by target, so that it can be called
    # as one of the in-built methods. uds.readDTC("something") It does not operate
    # on this instance of the container class.
    @staticmethod
    def __readDTC(target, subfunctions, dataRecord=[], **kwargs):
	
        # Some local functions to deal with use concatenation of a number of DIDs in RDBI operation ...

        # After an array of lengths has been constructed for the individual response elements, we need a simple function to check it against the response
        def checkTotalResponseLength(input,expectedLengthsList):
            lengthExpected = sum(expectedLengthsList)
            if(len(input) != lengthExpected): raise Exception("Total length returned not as expected. Expected: {0}; Got {1}".format(lengthExpected,len(input)))

        # The check functions just want to know about the next bit of the response, so this just pops it of the front of the response
        def popResponseElement(input,expectedList):
            if expectedList == []: raise Exception("Total length returned not as expected. Missing elements.")
            return (input[0:expectedList[0]], input[expectedList[0]:], expectedList[1:])

        if type(subfunctions) is not list:
            subfunctions = [subfunctions]
        subfunctions = sorted(subfunctions) # ... the spec always shows them sorted, so sticking to that - the return values are labelled, so order doesn't matter

        # Adding acceptance of lists at this point, as the spec allows for multiple subfunctions in the request to be concatenated ...
        requestSIDFunction = target.readDTCContainer.requestSIDFunctions["FaultMemoryRead[{0}]".format(subfunctions[0])]  # ... the SID should be the same for all DIDs, so just use the first
        requestSubfuncFunctions = [target.readDTCContainer.requestSubfuncFunctions["FaultMemoryRead[{0}]".format(subfunctions)] for subfunction in subfunctions]
        requestParamFunctions = [target.readDTCContainer.requestParamFunctions["FaultMemoryRead[{0}]".format(subfunctions)] for subfunction in subfunctions]

        # Adding acceptance of lists at this point, as the spec allows for multiple rdbi request to be concatenated ...
        checkSIDResponseFunction = target.readDTCContainer.checkSIDResponseFunctions["FaultMemoryRead[{0}]".format(subfunctions[0])]
        checkSIDLengthFunction = target.readDTCContainer.checkSIDLengthFunctions["FaultMemoryRead[{0}]".format(subfunctions[0])]
        checkSubfuncResponseFunctions = [target.readDTCContainer.checkDIDResponseFunctions["FaultMemoryRead[{0}]".format(subfunctions)] for subfunction in subfunctions]
        checkSubfuncLengthFunctions = [target.readDTCContainer.checkDIDLengthFunctions["FaultMemoryRead[{0}]".format(subfunctions)] for subfunction in subfunctions]

        # This is the same for all RDBI responses, irrespective of list or single input
        negativeResponseFunction = target.readDTCContainer.negativeResponseFunctions["FaultMemoryRead[{0}]".format(subfunctions[0])] # ... single code irrespective of list use, so just use the first

        # Adding acceptance of lists at this point, as the spec allows for multiple rdbi request to be concatenated ...
        positiveResponseFunctions = [target.readDTCContainer.positiveResponseFunctions["FaultMemoryRead[{0}]".format(subfunctions)] for subfunction in subfunctions]

        # Call the sequence of functions to execute the RDBI request/response action ...
        # ==============================================================================

        # Create the request ...
        request = requestSIDFunction()
        for subfuncFunc in requestSubfuncFunctions:
            request += subfuncFunc()                # ... creates an array of integers
        for requestParamFunc in requestParamFunctions:
            request += requestParamFunc(dataRecord) # ... extends array of integers if any params are present (dependent on the sub-functions present)

        # Send request and receive the response ...
        response = target.send(request) # ... this returns a single response
        negativeResponseFunction(response)  # ... throws an exception to be handled at a higher level if a negative response is received


        # We have a positive response so check that it makes sense to us ...
        SIDLength = checkSIDLengthFunction()
        expectedLengths = [SIDLength] ???????????need to check mutiples of data in some cases!!!! not an easy one to check!
????????????may need to seperate subfunc and response data return lengths? ?????????????????
        expectedLengths += [checkSubfuncLengthFunctions[i]() for i in range(len(checkSubfuncLengthFunctions))]
        checkTotalResponseLength(response,expectedLengths)

        # We've passed the length check, so check each element (which has to be present if the length is ok) ...
        SIDResponseComponent, responseRemaining, lengthsRemaining = popResponseElement(response,expectedLengths)
        checkSIDResponseFunction(SIDResponseComponent)
        Subfuncresponses = []
        for i in range(len(expectedLengths)-1):
            SubfuncResponseComponent, responseRemaining, lengthsRemaining = popResponseElement(responseRemaining,lengthsRemaining)
            Subfuncresponses.append(SubfuncResponseComponent)
            checkSubfuncResponseFunctions[i](SubfuncResponseComponent)

        # All is still good, so return the response ...
        returnValue = tuple([positiveResponseFunctions[i](Subfuncresponses[i],SIDLength) for i in range(len(Subfuncresponses))])
        if len(returnValue) == 1:
            returnValue = returnValue[0]  # ...we only send back a tuple if there were multiple DIDs
        return returnValue


    def bind_function(self, bindObject):
        bindObject.readDTC = MethodType(self.__readDTC, bindObject)

    ##
    # @brief method to add function to container - requestSIDFunction handles the SID component of the request message
    #def add_requestFunction(self, aFunction, dictionaryEntry):
    def add_requestSIDFunction(self, aFunction, dictionaryEntry):
        self.requestSIDFunctions[dictionaryEntry] = aFunction

    ##
    # @brief method to add function to container - requestSubfuncFunction handles the 1 to N subfunction components of the request message
    def add_requestSubfuncFunction(self, aFunction, dictionaryEntry):
        self.requestSubfuncFunctions[dictionaryEntry] = aFunction

    ##
    # @brief method to add function to container - requestParamFunction handles the 0 to N subfunction parameter components of the request message (not all subfunctions take params)
    def add_requestParamFunction(self, aFunction, dictionaryEntry):
        self.requestParamFunctions[dictionaryEntry] = aFunction

    ##
    # @brief method to add function to container - checkSIDResponseFunction handles the checking of the returning SID details in the response message
    def add_checkSIDResponseFunction(self, aFunction, dictionaryEntry):
        self.checkSIDResponseFunctions[dictionaryEntry] = aFunction

    ##
    # @brief method to add function to container - checkSIDLengthFunction handles return of the expected SID details length
    def add_checkSIDLengthFunction(self, aFunction, dictionaryEntry):
        self.checkSIDLengthFunctions[dictionaryEntry] = aFunction

    ##
    # @brief method to add function to container - checkSubfuncResponseFunction handles the checking of the returning subfunction details in the response message
    def add_checkSubfuncResponseFunction(self, aFunction, dictionaryEntry):
        self.checkSubfuncResponseFunctions[dictionaryEntry] = aFunction

    ##
    # @brief method to add function to container - checkSubfuncLengthFunction handles return of the expected subfunction details length
    def add_checkSubfuncLengthFunction(self, aFunction, dictionaryEntry):
        self.checkSubfuncLengthFunctions[dictionaryEntry] = aFunction

    ##
    # @brief method to add function to container - negativeResponseFunction handles the checking of all possible negative response codes in the response message, raising the required exception
    def add_negativeResponseFunction(self, aFunction, dictionaryEntry):
        self.negativeResponseFunctions[dictionaryEntry] = aFunction

    ##
    # @brief method to add function to container - positiveResponseFunction handles the extraction of any DID details in the response message fragment forthe DID that require return
    def add_positiveResponseFunction(self, aFunction, dictionaryEntry):
        self.positiveResponseFunctions[dictionaryEntry] = aFunction