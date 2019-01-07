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
        checkFunction = target.readDTCContainer.checkFunctions["FaultMemoryRead[{0}]".format(subfunction)]
        negativeResponseFunction = target.readDTCContainer.negativeResponseFunctions["FaultMemoryRead[{0}]".format(subfunction)]
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
        checkFunction(response)

        # All is still good, so return the response (currently this function does nothing, but including it here as a hook in case that changes) ...
        return positiveResponseFunction(response)

    def bind_function(self, bindObject):
        bindObject.readDTC = MethodType(self.__readDTC, bindObject)

    def add_requestFunction(self, aFunction, dictionaryEntry):
        self.requestFunctions[dictionaryEntry] = aFunction

    def add_checkFunction(self, aFunction, dictionaryEntry):
        self.checkFunctions[dictionaryEntry] = aFunction

    def add_negativeResponseFunction(self, aFunction, dictionaryEntry):
        self.negativeResponseFunctions[dictionaryEntry] = aFunction

    def add_positiveResponseFunction(self, aFunction, dictionaryEntry):
        self.positiveResponseFunctions[dictionaryEntry] = aFunction