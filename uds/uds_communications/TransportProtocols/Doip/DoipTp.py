#!/usr/bin/env python

__author__ = "Jacob Schaer"
__copyrights__ = "Copyright 2021, the python-uds project"
__credits__ = ["Richard Clubb", "Jacob Schaer"]

__license__ = "MIT"
__maintainer__ = "Richard Clubb"
__email__ = "richard.clubb@embeduk.com"
__status__ = "Development"


from os import path

from uds import iTp
from uds import Config

# Load python-doipclient library
from doipclient import DoIPClient

class DoipTp(iTp):

    #__metaclass__ = iTp

    def __init__(self, configPath=None, **kwargs):

        # perform the instance config
        self.__config = None

        self.__loadConfiguration(configPath)
        self.__checkKwargs(**kwargs)

        self.__ecu_ip = self.__config["DoIP"]["ecuIP"]
        self.__ecu_logical_address = int(self.__config["DoIP"]["ecuLogicalAddress"], 16)
        self.__tcp_port = int(self.__config["DoIP"]["tcpPort"])
        self.__activation_type = int(self.__config["DoIP"]["activationType"], 16)
        self.__protocol_version = int(self.__config["DoIP"]["protocolVersion"], 16)
        self.__client_logical_address = int(self.__config["DoIP"]["clientLogicalAddress"], 16)
        self.__use_secure = self.__config["DoIP"]["useSecure"]

        self.__connection = DoIPClient(
            self.__ecu_ip,
            self.__ecu_logical_address,
            tcp_port=self.__tcp_port,
            activation_type=self.__activation_type,
            protocol_version=self.__protocol_version,
            client_logical_address=self.__client_logical_address,
            use_secure=self.__use_secure)

    def send(self, payload, functionalReq=False):  # TODO: functionalReq not used???
        self.__connection.send_diagnostic(bytearray(payload))

    def recv(self, timeout_s):
        return list(self._connection.receive_diagnostic(timeout=timeout_s))

    def closeConnection(self):
        self.__connection.close()

    ##
    # @brief clear out the receive list
    def clearBufferedMessages(self):
        self._connection.empty_rxqueue()

    ##
    # @brief used to load the local configuration options and override them with any passed in from a config file
    def __loadConfiguration(self, configPath, **kwargs):
        # load the base config
        baseConfig = path.dirname(__file__) + "/config.ini"
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

    ##
    # @brief goes through the kwargs and overrides any of the local configuration options
    def __checkKwargs(self, **kwargs):
        if 'ecu_ip' in kwargs:
            self.__config['DoIP']['ecuIP'] = kwargs['ecu_ip']
        if 'ecu_logical_address' in kwargs:
            self.__config['DoIP']['ecuLogicalAddress'] = hex(kwargs['ecu_logical_address'])
        if 'tcp_port' in kwargs:
            self.__config['DoIP']['tcpPort'] = str(kwargs['tcp_port'])
        if 'activation_type' in kwargs:
            self.__config['DoIP']['activationType'] = hex(kwargs['activation_type'])
        if 'protocol_version' in kwargs:
            self.__config['DoIP']['protocolVersion'] = hex(kwargs['protocol_version'])
        if 'client_logical_address' in kwargs:
            self.__config['DoIP']['clientLogicalAddress'] = hex(kwargs['client_logical_address'])
        if 'use_secure' in kwargs:
            self.__config['DoIP']['useSecure'] = True if kwargs['use_secure'] else False