#!/usr/bin/env python

__author__ = "Richard Clubb"
__copyrights__ = "Copyright 2018, the python-uds project"
__credits__ = ["Richard Clubb"]

__license__ = "MIT"
__maintainer__ = "Richard Clubb"
__email__ = "richard.clubb@embeduk.com"
__status__ = "Development"


from FunctionCreation.iServiceMethodFactory import IServiceMethodFactory


class WriteDataByIdentifierMethodFactory(IServiceMethodFactory):

    ##
    # @brief method to create the request function for the service element
    @staticmethod
    def create_requestFunction(diagServiceElement, xmlElements):
        pass

    ##
    # @brief method to create the function to check the positive response for validity
    @staticmethod
    def create_checkPositiveResponseFunction(diagServiceElement, xmlElements):
        pass

    ##
    # @brief method to encode the positive response from the raw type to it physical representation
    @staticmethod
    def create_encodePositiveResponseFunction(diagServiceElement, xmlElements):
        pass

    ##
    # @brief method to create the negative response function for the service element
    @staticmethod
    def create_checkNegativeResponseFunction(diagServiceElement, xmlElements):
        pass
