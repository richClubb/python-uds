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
import threading

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
        #print(("__transmissionActive_flag initialised (clear):",self.__transmissionActive_flag))
        # The above flag should prevent testerPresent operation, but in case of race conditions, this lock prevents actual overlapo in the sending
        self.sendLock = threading.Lock()

        # Process any ihex file that has been associated with the ecu at initialisation
        self.__ihexFile = ihexFileParser(ihexFile) if ihexFile is not None else None



    def __loadConfiguration(self, configPath=None):

        baseConfig = path.dirname(__file__) + "/config.ini"
        # print(baseConfig)
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
    def send(self, msg, responseRequired=True, functionalReq=False, tpWaitTime = 0.01):
        # sets a current transmission in progress - tester present (if running) will not send if this flag is set to true
        self.__transmissionActive_flag = True
        #print(("__transmissionActive_flag set:",self.__transmissionActive_flag))

        response = None

        # We're moving to threaded operation, so putting a lock around the send operation. 
        self.sendLock.acquire()
        try:
            a = self.tp.send(msg, functionalReq, tpWaitTime)
        finally:
            self.sendLock.release()

        if functionalReq is True:
            responseRequired = False

        # Note: in automated mode (unlikely to be used any other way), there is no response from tester present, so threading is not an issue here.
        if responseRequired:
            while True:
                response = self.tp.recv(self.__P2_CAN_Client)
                if not ((response[0] == 0x7F) and (response[2] == 0x78)):
                    break

        # If the diagnostic session control service is supported, record the sending time for possible use by the tester present functionality (again, if present) ...		
        try:
            self.sessionSetLastSend()
        except:
            pass  # ... if the service isn't present, just ignore
			
        # Lets go of the hold on transmissions - allows test present to resume operation (if it's running)
        self.__transmissionActive_flag = False
        #print(("__transmissionActive_flag cleared:",self.__transmissionActive_flag))

        return response

    def disconnect(self):

        self.tp.closeConnection()
        
    ##
    # @brief
    def isTransmitting(self):
        #print(("requesting __transmissionActive_flag:",self.__transmissionActive_flag))
        return self.__transmissionActive_flag

if __name__ == "__main__":

    pass
