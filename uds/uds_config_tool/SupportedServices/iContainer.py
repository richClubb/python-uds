#!/usr/bin/env python

__author__ = "Richard Clubb"
__copyrights__ = "Copyright 2018, the python-uds project"
__credits__ = ["Richard Clubb"]

__license__ = "MIT"
__maintainer__ = "Richard Clubb"
__email__ = "richard.clubb@embeduk.com"
__status__ = "Development"


from abc import ABCMeta, abstractmethod

class iContainer(ABCMeta):

    @abstractmethod
    def add_requestFunction(self, aFunction, dictionaryEntry):
        raise NotImplementedError("add_requestFucntion not implemented")

    @abstractmethod
    def add_checkFunction(self, aFunction, dictionaryEntry):
        raise NotImplementedError("add_checkFunction not implemented")

    @abstractmethod
    def add_negativeResponseFunction(self, aFunction, dictionaryEntry):
        raise NotImplementedError("add_negativeResponseFunction not implemented")

    @abstractmethod
    def add_positiveResponseFunction(self, aFunction, dictionaryEntry):
        raise NotImplementedError("add_positiveResponseFunction not implemented")
