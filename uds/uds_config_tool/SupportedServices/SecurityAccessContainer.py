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


class SecurityAccessContainer(object):

    __metaclass__ = iContainer

    def __init__(self):
        self.requestFunctions = {}
        self.checkFunctions = {}
        self.negativeResponseFunctions = {}
        self.positiveResponseFunctions = {}

    @staticmethod
    def __securityAccess(target, parameter, key=None, suppressResponse=False):

        requestFunction = target.securityAccessContainer.requestFunctions[parameter]
        checkNegativeResponseFunction = target.securityAccessContainer.negativeResponseFunctions[parameter]
        checkPositiveResponseFunctions = target.securityAccessContainer.positiveResponseFunctions[parameter]
        checkSidFunction = checkPositiveResponseFunctions[0]
        checkSecurityAccessFunction = checkPositiveResponseFunctions[1]
        checkDataFunction = checkPositiveResponseFunctions[2]

        # if the key is not none then we are sending a key back to the ECU check the key type
        if key is not None:
            #check key format
            # send request for key response
            response = target.send(requestFunction(key, suppressResponse), responseRequired=not(suppressResponse))
        else:
            response = target.send(requestFunction(suppressResponse))

        if suppressResponse is False:
            checkNegativeResponseFunction(response)

        if checkDataFunction is None:
            output = None
        else:
            checkDataFunction(response[2:])
            output = response[2:]

        return output

    def bind_function(self, bindObject):
        bindObject.securityAccess = MethodType(self.__securityAccess, bindObject)

    def add_requestFunction(self, aFunction, dictionaryEntry):
        self.requestFunctions[dictionaryEntry] = aFunction

    def add_checkFunction(self, aFunction, dictionaryEntry):
        self.checkFunctions[dictionaryEntry] = aFunction

    def add_negativeResponseFunction(self, aFunction, dictionaryEntry):
        self.negativeResponseFunctions[dictionaryEntry] = aFunction

    def add_positiveResponseFunction(self, aFunction, dictionaryEntry):
        self.positiveResponseFunctions[dictionaryEntry] = aFunction
