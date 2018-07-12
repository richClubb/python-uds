#!/usr/bin/env python

__author__ = "Richard Clubb"
__copyrights__ = "Copyright 2018, the python-uds project"
__credits__ = ["Richard Clubb"]

__license__ = "MIT"
__maintainer__ = "Richard Clubb"
__email__ = "richard.clubb@embeduk.com"
__status__ = "Development"

from Uds import Uds
from UdsMessage import UdsMessage
import configparser
import logging
import os.path

##
# @class Ecu
# @brief The higher level interface object
class Ecu(object):

    ##
    # Instantiates a new ECU object with specified request and response Id. If no Ids are supplied then it will
    # try and parse the config.ini file to get default values.
    #
    # @param [in] reqId the request Id for UDS communications
    # @param [in] resId the response Id for UDS communications
    def __init__(self, reqId=None, resId=None):
        self.__config = None
        try:
            self.__config = configparser.ConfigParser()
            self.__config.read('config.ini')
        except:
            pass

        if self.__config is not None:
            if(reqId is None):
                self.__reqId = int(self.__config['ecu']['ReqId_default'], 16)
            else:
                self.__reqId = reqId
            if(resId is None):
                self.__resId = int(self.__config['ecu']['ResId_default'], 16)
            else:
                self.__resId = resId
        else:
            self.__reqId = reqId
            self.__resId = resId

        self.__udsChannel = Uds(reqId=self.__reqId, resId=self.__resId)

        if(self.__config is not None):
            loggerName = self.__config['logging']['LoggerName']
            #logLevel = self.__config['logging']['LoggingLevel']
            self.__logger = logging.getLogger(loggerName)
            self.__logger.setLevel(logging.INFO)
            fh = logging.FileHandler('logging.log')
            fh.setLevel(logging.INFO)
            sh = logging.StreamHandler()
            sh.setLevel(logging.INFO)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            fh.setFormatter(formatter)
            sh.setFormatter(formatter)
            self.__logger.addHandler(fh)
            self.__logger.addHandler(sh)

        # this part defines how the services are loaded

    ##
    # @brief
    # @param [in] msg The Uds message to be transmitted
    def send(self, msg):
        self.__logger.info("Sending Uds message " + str(msg.request))
        self.__udsChannel.send(msg)


if __name__ == "__main__":

    pass