#!/usr/bin/env python

__author__ = "Richard Clubb"
__copyrights__ = "Copyright 2018, the python-uds project"
__credits__ = ["Richard Clubb"]

__license__ = "MIT"
__maintainer__ = "Richard Clubb"
__email__ = "richard.clubb@embeduk.com"
__status__ = "Development"


from abc import ABCMeta, abstractmethod


##
# @brief this should be static
class IServiceMethodFactory(ABCMeta):

    ##
    # @brief method to create the request function for the service element
    @staticmethod
    @abstractmethod
    def create_requestFunction(diagServiceElement, xmlElements):
        raise NotImplementedError("create_requestFunction not yet implemented")

    ##
    # @brief method to create the function to check the positive response for validity
    @staticmethod
    @abstractmethod
    def create_checkPositiveResponseFunction(diagServiceElement, xmlElements):
        raise NotImplementedError("create_checkPositiveResponseFunction not yet implemented")

    ##
    # @brief method to encode the positive response from the raw type to it physical representation
    @staticmethod
    @abstractmethod
    def create_encodePositiveResponseFunction(diagServiceElement, xmlElements):
        raise NotImplementedError("create_encodePositiveResponseFunction not yet implemented")

    ##
    # @brief method to create the negative response function for the service element
    @staticmethod
    @abstractmethod
    def create_checkNegativeResponseFunction(diagServiceElement, xmlElements):
        raise NotImplementedError("create_checkNegativeResponseFunction not yet implemented")
