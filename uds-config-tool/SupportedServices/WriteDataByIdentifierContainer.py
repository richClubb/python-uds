#!/usr/bin/env python

__author__ = "Richard Clubb"
__copyrights__ = "Copyright 2018, the python-uds project"
__credits__ = ["Richard Clubb"]

__license__ = "MIT"
__maintainer__ = "Richard Clubb"
__email__ = "richard.clubb@embeduk.com"
__status__ = "Development"


from SupportedServices.iContainer import iContainer


class WriteDataByIdentifierContainer(iContainer):

    def __init__(self):
        self.requestFunctions = {}
        self.checkFunctions = {}
        self.negativeResponseFunctions = {}
        self.positiveResponseFunctions = {}

    @staticmethod
    def __writeDataByIdentifier(target, parameter, **kwargs):
        pass

    def bind_function(self, bindObject):
        pass

    def add_requestFunction(self, aFunction, dictionaryEntry):
        pass

    def add_checkFunction(self, aFunction, dictionaryEntry):
        pass

    def add_negativeResponseFunction(self, aFunction, dictionaryEntry):
        pass

    def add_positiveResponseFunction(self, aFunction, dictionaryEntry):
        pass