#!/usr/bin/env python

__author__ = "Richard Clubb"
__copyrights__ = "Copyright 2018, the python-uds project"
__credits__ = ["Richard Clubb"]

__license__ = "MIT"
__maintainer__ = "Richard Clubb"
__email__ = "richard.clubb@embeduk.com"
__status__ = "Development"


from uds.uds_config_tool.IHexFunctions import ihexFile as ihexFileParser
from uds.uds_config_tool.ISOStandard.ISOStandard import IsoDataFormatIdentifier
from uds import Config
from uds import TpFactory
from os import path

##
# @brief a description is needed
class Uds(object):

    ##
    # @brief a constructor
    # @param [in] reqId The request ID used by the UDS connection, defaults to None if not used
    # @param [in] resId The response Id used by the UDS connection, defaults to None if not used
    def __init__(self, configPath=None, ihexFile=None, **kwargs):

        self.__config = None
        self.__transportProtocol = None
        self.__P2_CAN_Client = None
        self.__P2_CAN_Server = None

        self.__loadConfiguration(configPath)
        self.__checkKwargs(**kwargs)

        self.__transportProtocol = self.__config['uds']['transportProtocol']
        self.__P2_CAN_Client = float(self.__config['uds']['P2_CAN_Client'])
        self.__P2_CAN_Server = float(self.__config['uds']['P2_CAN_Server'])

        tpFactory = TpFactory()
        self.tp = tpFactory(self.__transportProtocol, configPath=configPath, **kwargs)

        # used as a semaphore for the tester present
        self.__transmissionActive_flag = False

        # Process any ihex file that has been associated with the ecu at initialisation
        self.__ihexFile = ihexFileParser(ihexFile) if ihexFile is not None else None

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
            self.__config['uds']['transportProtocol'] = kwargs['transportProtocol']

        if 'P2_CAN_Server' in kwargs:
            self.__config['uds']['P2_CAN_Server'] = str(kwargs['P2_CAN_Server'])

        if 'P2_CAN_Client' in kwargs:
            self.__config['uds']['P2_CAN_Client'] = str(kwargs['P2_CAN_Client'])


    @property
    def ihexFile(self):
        return self.__ihexFile

    @ihexFile.setter
    def ihexFile(self, value):
        if value is not None:
            self.__ihexFile = ihexFileParser(value)

    
    ##
    # @brief Currently only called from transferFile to transfer ihex files
    def transferIHexFile(self,transmitChunkSize=None,compressionMethod=None):
        if transmitChunkSize is not None:
            self.__ihexFile.transmitChunksize = transmitChunkSize
        if compressionMethod is None:
            compressionMethod = IsoDataFormatIdentifier.noCompressionMethod
        self.requestDownload([compressionMethod], self.__ihexFile.transmitAddress, self.__ihexFile.transmitLength)
        self.transferData(transferBlocks=self.__ihexFile)
        return self.transferExit()

    ##
    # @brief This will eventually support more than one file type, but for now is limited to ihex only
    def transferFile(self,fileName=None,transmitChunkSize=None,compressionMethod=None):
        if fileName is None and self.__ihexFile is None:
            raise FileNotFoundError("file to transfer has not been specified")

        # Currently only ihex is recognised and supported
        if fileName[-4:] == '.hex' or fileName[-5:] == '.ihex':
            self.__ihexFile = ihexFileParser(fileName)
            return self.transferIHexFile(transmitChunkSize,compressionMethod)
        else:
            raise FileNotFoundError("file to transfer has not been recognised as a supported type ['.hex','.ihex']")



    ##
    # @brief
    def send(self, msg, responseRequired=True, functionalReq=False):

        # sets a current transmission in progress
        self.__transmissionActive_flag = True

        response = None

        a = self.tp.send(msg, functionalReq)

        if functionalReq is True:
            responseRequired = False

        if responseRequired:
            response = self.tp.recv(self.__P2_CAN_Client)

        # lets go of the hold on transmissions
        self.__transmissionActive_flag = False

        return response

    def disconnect(self):

        self.tp.closeConnection()

if __name__ == "__main__":

    pass