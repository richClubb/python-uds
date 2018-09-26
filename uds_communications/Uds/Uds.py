#!/usr/bin/env python

__author__ = "Richard Clubb"
__copyrights__ = "Copyright 2018, the python-uds project"
__credits__ = ["Richard Clubb"]

__license__ = "MIT"
__maintainer__ = "Richard Clubb"
__email__ = "richard.clubb@embeduk.com"
__status__ = "Development"


from uds_configuration.Config import Config
from uds_communications.TransportProtocols.TpFactory import TpFactory
from os import path

##
# @brief a description is needed
class Uds(object):

    ##
    # @brief a constructor
    # @param [in] reqId The request ID used by the UDS connection, defaults to None if not used
    # @param [in] resId The response Id used by the UDS connection, defaults to None if not used
    def __init__(self, configPath=None, **kwargs):

        self.__config = None
        self.__transportProtocol = None
        self.__P2_CAN_Client = None
        self.__P2_CAN_Server = None

        self.__loadConfiguration(configPath)

        self.__transportProtocol = self.__config['uds']['transportProtocol']
        self.__P2_CAN_Client = int(self.__config['uds']['P2_CAN_Client'])
        self.__P2_CAN_Server = int(self.__config['uds']['P2_CAN_Server'])

        self.__checkKwargs(**kwargs)

        tpFactory = TpFactory()
        self.__tp = tpFactory(self.__transportProtocol, configPath=configPath, **kwargs)

        # used as a semaphore for the tester present
        self.__transmissionActive_flag = False

    def __loadConfiguration(self, configPath=None):

        baseConfig = path.dirname(__file__) + "\config.ini"
        self.__config = Config()
        if path.exists(baseConfig):
            self.__config.read(baseConfig)
        else:
            raise FileNotFoundError("No base config file")

        # check the config path
        if configPath is not None:
            if path.exists(configPath):
                self.__config.read(configPath)
            else:
                raise FileNotFoundError("specified config not found")

    def __checkKwargs(self, **kwargs):

        if 'transportProtocol' in kwargs:
            self.__transportProtocol = kwargs['transportProtocol']

        if 'P2_CAN_Server' in kwargs:
            self.__P2_CAN_Server = kwargs['P2_CAN_Server']

        if 'P2_CAN_Client' in kwargs:
            self.__P2_CAN_Client = kwargs['P2_CAN_Client']

    ##
    # @brief
    def send(self, msg, responseRequired=True, functionalReq=False):

        # sets a current transmission in progress
        self.__transmissionActive_flag = True

        response = None

        self.__tp.send(msg, functionalReq)

        if functionalReq is True:
            responseRequired = False

        if responseRequired:
            response = self.__tp.recv(self.__P2_CAN_Client)

        # lets go of the hold on transmissions
        self.__transmissionActive_flag = False

        return response


if __name__ == "__main__":
    pass
