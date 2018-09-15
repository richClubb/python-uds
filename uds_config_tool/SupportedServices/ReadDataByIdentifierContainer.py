#!/usr/bin/env python

__author__ = "Richard Clubb"
__copyrights__ = "Copyright 2018, the python-uds project"
__credits__ = ["Richard Clubb"]

__license__ = "MIT"
__maintainer__ = "Richard Clubb"
__email__ = "richard.clubb@embeduk.com"
__status__ = "Development"


from uds_config_tool.SupportedServices.iContainer import iContainer
from types import MethodType


class ReadDataByIdentifierContainer(iContainer):

    def __init__(self):
        self.requestFunctions = {}
        self.checkFunctions = {}
        self.negativeResponseFunctions = {}
        self.positiveResponseFunctions = {}

    @staticmethod
    def __readDataByIdentifier(target, parameter):
        requestFunction = target.readDataByIdentifierContainer.requestFunctions[parameter]
        checkFunction = target.readDataByIdentifierContainer.checkFunctions[parameter]
        negativeResponseFunction = target.readDataByIdentifierContainer.negativeResponseFunctions[parameter]
        positiveResponseFunction = target.readDataByIdentifierContainer.positiveResponseFunctions[parameter]

        request = requestFunction()

        response = target.send(request)

        checkFunction(response)
        negativeResponseFunction(response)
        return positiveResponseFunction(response)

    def bind_function(self, bindObject):
        bindObject.readDataByIdentifier = MethodType(self.__readDataByIdentifier, bindObject)

    def add_requestFunction(self, aFunction, dictionaryEntry):
        self.requestFunctions[dictionaryEntry] = aFunction

    def add_checkFunction(self, aFunction, dictionaryEntry):
        self.checkFunctions[dictionaryEntry] = aFunction

    def add_negativeResponseFunction(self, aFunction, dictionaryEntry):
        self.negativeResponseFunctions[dictionaryEntry] = aFunction

    def add_positiveResponseFunction(self, aFunction, dictionaryEntry):
        self.positiveResponseFunctions[dictionaryEntry] = aFunction


if __name__ == "__main__":

    pass




