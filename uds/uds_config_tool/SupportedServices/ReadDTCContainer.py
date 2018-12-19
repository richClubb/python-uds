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
    def __readDTC(target, subfunction, DTCStatusMask=None, DTCMaskRecord=None, DTCSnapshotRecordNumber=None, DTCExtendedRecordNumber=None, DTCSeverityMask=None, **kwargs):
        # Note: readDTC does not show support for DIDs or multiple subfunctions in the spec, so this is handling only a single subfunction with data record.
        requestFunction = target.readDTCContainer.requestFunctions["FaultMemoryRead[{0}]".format(subfunction)]
        checkResponseFunction = target.readDTCContainer.checkResponseFunctions["FaultMemoryRead[{0}]".format(subfunction)]
        negativeResponseFunction = target.readDTCContainer.negativeResponseFunctions["FaultMemoryRead[{0}]".format(subfunctions[0])]
        positiveResponseFunction = target.readDTCContainer.positiveResponseFunctions["FaultMemoryRead[{0}]".format(subfunction)]

        # Call the sequence of functions to execute the RDBI request/response action ...
        # ==============================================================================

        # Create the request ...
        DTCStatusMask = [DTCStatusMask] if DTCStatusMask is not None else []
		DTCMaskRecord = DTCMaskRecord if DTCMaskRecord is not None else []
		DTCSnapshotRecordNumber = [DTCSnapshotRecordNumber] if DTCSnapshotRecordNumber is not None else []
		DTCExtendedRecordNumber = [DTCExtendedRecordNumber] if DTCExtendedRecordNumber is not None else []
		DTCSeverityMask = [DTCSeverityMask] if DTCSeverityMask is not None else []
        request = requestFunction(DTCStatusMask=DTCStatusMask,DTCMaskRecord=DTCMaskRecord,DTCSnapshotRecordNumber=[],DTCExtendedRecordNumber=[],DTCSeverityMask=[])


        # Send request and receive the response ...
        response = target.send(request) # ... this returns a single response
        negativeResponseFunction(response)  # ... throws an exception to be handled at a higher level if a negative response is received

        # We have a positive response so check that it makes sense to us ...
		
???????????????we have to work with lists here, so the return length is variable >???????????????????? looking at the rdbi code for ideas ???????????
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