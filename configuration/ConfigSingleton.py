from configparser import ConfigParser
from os import path

udsConfig = None

def get_config():

    global udsConfig

    dirpath = path.dirname(__file__)
    configPath = dirpath + "\defaultConfig.ini"

    if udsConfig == None:
        udsConfig = ConfigParser()
        if path.isfile(configPath):
            udsConfig.read(configPath)
        else:
            raise FileNotFoundError("Base config file not found in configuration directory")

    return udsConfig

def load_additional_config(filepath):

    config = get_config()
    localConfig = ConfigParser()

    if path.isfile(filepath):
        config.read(filepath)
    else:
        raise FileNotFoundError("No file found")