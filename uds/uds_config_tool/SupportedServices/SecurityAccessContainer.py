#!/usr/bin/env python

__author__ = "Richard Clubb"
__copyrights__ = "Copyright 2018, the python-uds project"
__credits__ = ["Richard Clubb"]

__license__ = "MIT"
__maintainer__ = "Richard Clubb"
__email__ = "richard.clubb@embeduk.com"
__status__ = "Development"


from uds.uds_config_tool.SupportedServices.iContainer import iContainer


class SecurityAccessContainer(object):

    __metaclass__ = iContainer

    def __init__(self):
        self.requestFunctions = {}
        self.checkFunctions = {}
        self.negativeResponseFunctions = {}
        self.positiveResponseFunctions = {}

    @staticmethod
    def __securityAccess(target, parameter, suppressResponse=False, key=None):

        requestFunction = target.securityAccessContainer.requestFunctions[parameter]

        # if the key is not none then we are sending a key back to the ECU check the key type
        if key is not None:
            pass
        else:
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