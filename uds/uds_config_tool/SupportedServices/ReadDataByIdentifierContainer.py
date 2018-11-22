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


class ReadDataByIdentifierContainer(object):

    __metaclass__ = iContainer

    def __init__(self):

        # To cater for lists we may have to re-factor here - i.e. requestFunc can be split into requestSIDFunc and requestDIDFunc to allow building on the fly from a DID list
        # Also checkFunction into: checkSIDResonseFunction+SIDLengthFunction, checkResponseLengthFunction + responseLengthFunction, and an iterable checkDIDResponseFunction
        # Also positiveResponseFunc into: positiveResponseSIDFunction, and an iterable positiveResponseDIDFunction
        # Negative response function is ok as it it

        #self.requestFunctions = {}
        self.requestSIDFunctions = {}
        self.requestDIDFunctions = {}

        #self.checkFunctions = {}
        self.checkSIDResponseFunctions = {}
        self.checkSIDLengthFunctions = {}
        self.checkDIDResponseFunctions = {}
        self.checkDIDLengthFunctions = {}

        self.negativeResponseFunctions = {}

        self.positiveResponseFunctions = {}

    ##
    # @brief this method is bound to an external Uds object so that it call be called
    # as one of the in-built methods. uds.readDataByIdentifier("something") It does not operate
    # on this instance of the container class.
    @staticmethod
    def __readDataByIdentifier(target, parameter):
        # Some local functions to deal with use concatenation of a number of DIDs in RDBI operation ...

        # After an array of lengths has been constructed for the individual response elements, we need a simple function to check it against the response
        def checkTotalResponseLength(input,expectedLengthsList):
            lengthExpected = sum(expectedLengthsList)
            if(len(input) != lengthExpected): raise Exception("Total length returned not as expected. Expected: {0}; Got {1}".format(lengthExpected,len(input)))

        # The check functions just want to know about the next bit of the response, so this just pops it of the front of the response
        def popResponseElement(input,expectedList):
            if expectedList == []: raise Exception("Total length returned not as expected. Missing elements.")
            return (input[0:expectedList[0]], input[expectedList[0]:], expectedList[1:])


        dids = parameter
        if type(dids) is not list:
            dids = [dids]

        # Adding acceptance of lists at this point, as the spec allows for multiple rdbi request to be concatenated ...
        requestSIDFunction = target.readDataByIdentifierContainer.requestSIDFunctions[dids[0]]  # ... the SID should be the same for all DIDs, so just use the first
        requestDIDFunctions = [target.readDataByIdentifierContainer.requestDIDFunctions[did] for did in dids]

        # Adding acceptance of lists at this point, as the spec allows for multiple rdbi request to be concatenated ...
        checkSIDResponseFunction = target.readDataByIdentifierContainer.checkSIDResponseFunctions[dids[0]]
        checkSIDLengthFunction = target.readDataByIdentifierContainer.checkSIDLengthFunctions[dids[0]]
        checkDIDResponseFunctions = [target.readDataByIdentifierContainer.checkDIDResponseFunctions[did] for did in dids]
        checkDIDLengthFunctions = [target.readDataByIdentifierContainer.checkDIDLengthFunctions[did] for did in dids]

        # This is the same for all RDBI responses, irrespective of list or single input
        negativeResponseFunction = target.readDataByIdentifierContainer.negativeResponseFunctions[dids[0]] # ... single code irrespective of list use, so just use the first

        # Adding acceptance of lists at this point, as the spec allows for multiple rdbi request to be concatenated ...
        positiveResponseFunctions = [target.readDataByIdentifierContainer.positiveResponseFunctions[did] for did in dids]


        # Call the sequence of functions to execute the RDBI request/response action ...
        # ==============================================================================

        # Create the request ...
        request = requestSIDFunction()
        for didFunc in requestDIDFunctions:
            request += didFunc()                # ... creates an array of integers

        # Send request and receive the response ...
        response = target.send(request) # ... this returns a single response which may cover 1 or more DID response values
        negativeResponseFunction(response)  # ... throws an exception to be handled at a higher level if a negative response is received

        # We have a positive response so check that it makes sense to us ...
        SIDLength = checkSIDLengthFunction()
        expectedLengths = [SIDLength]
        expectedLengths += [checkDIDLengthFunctions[i]() for i in range(len(checkDIDLengthFunctions))]
        checkTotalResponseLength(response,expectedLengths)

        # We've passed the length check, so check each element (which has to be present if the length is ok) ...
        SIDResponseComponent, responseRemaining, lengthsRemaining = popResponseElement(response,expectedLengths)
        checkSIDResponseFunction(SIDResponseComponent)
        DIDresponses = []
        for i in range(len(expectedLengths)-1):
            DIDResponseComponent, responseRemaining, lengthsRemaining = popResponseElement(responseRemaining,lengthsRemaining)
            DIDresponses.append(DIDResponseComponent)
            checkDIDResponseFunctions[i](DIDResponseComponent)

        # All is still good, so return the response ...
        returnValue = tuple([positiveResponseFunctions[i](DIDresponses[i],SIDLength) for i in range(len(DIDresponses))])
        if len(returnValue) == 1:
            returnValue = returnValue[0]  # ...we only send back a tuple if there were multiple DIDs
        return returnValue


    def bind_function(self, bindObject):
        bindObject.readDataByIdentifier = MethodType(self.__readDataByIdentifier, bindObject)

    ##
    # @brief method to add function to container - requestSIDFunction handles the SID component of the request message
    #def add_requestFunction(self, aFunction, dictionaryEntry):
    def add_requestSIDFunction(self, aFunction, dictionaryEntry):
        self.requestSIDFunctions[dictionaryEntry] = aFunction

    ##
    # @brief method to add function to container - requestDIDFunction handles the 1 to N DID components of the request message
    def add_requestDIDFunction(self, aFunction, dictionaryEntry):
        self.requestDIDFunctions[dictionaryEntry] = aFunction

    ##
    # @brief method to add function to container - checkSIDResponseFunction handles the checking of the returning SID details in the response message
    def add_checkSIDResponseFunction(self, aFunction, dictionaryEntry):
        self.checkSIDResponseFunctions[dictionaryEntry] = aFunction

    ##
    # @brief method to add function to container - checkSIDLengthFunction handles return of the expected SID details length
    def add_checkSIDLengthFunction(self, aFunction, dictionaryEntry):
        self.checkSIDLengthFunctions[dictionaryEntry] = aFunction

    ##
    # @brief method to add function to container - checkDIDResponseFunction handles the checking of the returning DID details in the response message
    def add_checkDIDResponseFunction(self, aFunction, dictionaryEntry):
        self.checkDIDResponseFunctions[dictionaryEntry] = aFunction

    ##
    # @brief method to add function to container - checkDIDLengthFunction handles return of the expected DID details length
    def add_checkDIDLengthFunction(self, aFunction, dictionaryEntry):
        self.checkDIDLengthFunctions[dictionaryEntry] = aFunction

    ##
    # @brief method to add function to container - negativeResponseFunction handles the checking of all possible negative response codes in the response message, raising the required exception
    def add_negativeResponseFunction(self, aFunction, dictionaryEntry):
        self.negativeResponseFunctions[dictionaryEntry] = aFunction

    ##
    # @brief method to add function to container - positiveResponseFunction handles the extraction of any DID details in the response message fragment forthe DID that require return
    def add_positiveResponseFunction(self, aFunction, dictionaryEntry):
        self.positiveResponseFunctions[dictionaryEntry] = aFunction


if __name__ == "__main__":

    pass




