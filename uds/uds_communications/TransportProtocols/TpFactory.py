#!/usr/bin/env python

__author__ = "Richard Clubb"
__copyrights__ = "Copyright 2018, the python-uds project"
__credits__ = ["Richard Clubb"]

__license__ = "MIT"
__maintainer__ = "Richard Clubb"
__email__ = "richard.clubb@embeduk.com"
__status__ = "Development"


from uds import Config
from uds import CanTp
from uds import LinTp
from uds import TestTp
from os import path


##
# @brief class for creating Tp objects
class TpFactory(object):

    configType = ''
    configParameters = []

    config = None

    ##
    # @brief method to create the different connection types
    @staticmethod
    def __call__(tpType, configPath=None, **kwargs):

        #TpFactory.loadConfiguration(configPath)

        if(tpType == "CAN"):
            return CanTp(configPath=configPath, **kwargs)
        elif(tpType == "DoIP"):
            raise NotImplementedError("DoIP transport not currently supported")
        elif(tpType == "K-LINE"):
            raise NotImplementedError("K-Line Transport not currently supported")
        elif(tpType == "LIN"):
            return LinTp(configPath=configPath, **kwargs)
        elif(tpType == "FLEXRAY"):
            raise NotImplementedError("FlexRay Transport not currently supported")
        elif(tpType == "TEST"):
            return TestTp()
        else:
            raise Exception("Unknown transport type selected")

    @staticmethod
    def loadConfiguration(configPath=None):

        #load the base config
        baseConfig = path.dirname(__file__) + "/config.ini"
        config = Config()
        if path.exists(baseConfig):
            config.read(baseConfig)
        else:
            raise FileNotFoundError("No base config file")

        # check the config path
        if configPath is not None:
            if path.exists(configPath):
                config.read(configPath)
            else:
                raise FileNotFoundError("specified config not found")

        TpFactory.config = config


if __name__ == "__main__":

    pass
