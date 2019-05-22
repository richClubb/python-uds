import can
from can.interfaces import pcan, vector
from uds.uds_configuration.Config import Config
from os import path
from platform import system
#from uds import CanConnection
from uds.uds_communications.TransportProtocols.Can.CanConnection import CanConnection

# used to conditionally import socketcan for linux to avoid error messages
if system() == "Linux":
    from can.interfaces import socketcan

class CanConnectionFactory(object):

    connections = {}
    config = None

    @staticmethod
    def __call__(callback=None, filter=None, configPath=None, **kwargs):

        CanConnectionFactory.loadConfiguration(configPath)
        CanConnectionFactory.checkKwargs(**kwargs)

        # check config file and load
        connectionType = CanConnectionFactory.config['can']['interface']

        if connectionType == 'virtual':
            connectionName = CanConnectionFactory.config['virtual']['interfaceName']
            if connectionName not in CanConnectionFactory.connections:
                CanConnectionFactory.connections[connectionName] = CanConnection(callback, filter,
                                                                                 can.interface.Bus(connectionName,
                                                                                     bustype='virtual'))
            else:
                CanConnectionFactory.connections[connectionName].addCallback(callback)
                CanConnectionFactory.connections[connectionName].addFilter(filter)
            return CanConnectionFactory.connections[connectionName]

        elif connectionType == 'peak':
            channel = CanConnectionFactory.config['peak']['device']
            if channel not in CanConnectionFactory.connections:
                baudrate = CanConnectionFactory.config['can']['baudrate']
                CanConnectionFactory.connections[channel] = CanConnection(callback, filter,
                                                                          pcan.PcanBus(channel,
                                                                          bitrate=baudrate))
            else:
                CanConnectionFactory.connections[channel].addCallback(callback)
                CanConnectionFactory.connections[channel].addFilter(filter)
                
            return CanConnectionFactory.connections[channel]

        elif connectionType == 'vector':
            channel = int(CanConnectionFactory.config['vector']['channel'])
            app_name = CanConnectionFactory.config['vector']['appName']
            connectionKey = str("{0}_{1}").format(app_name, channel)
            if connectionKey not in CanConnectionFactory.connections:
                baudrate = int(CanConnectionFactory.config['can']['baudrate'])
                CanConnectionFactory.connections[connectionKey] = CanConnection(callback, filter,
                                                                                vector.VectorBus(channel,
                                                                                    app_name=app_name,
                                                                                    data_bitrate=baudrate))
            else:
                CanConnectionFactory.connections[connectionKey].addCallback(callback)
                CanConnectionFactory.connections[connectionKey].addFilter(filter)
            return CanConnectionFactory.connections[connectionKey]

        elif connectionType == 'socketcan':
            if system() == "Linux":
                channel = CanConnectionFactory.config['socketcan']['channel']
                if channel not in CanConnectionFactory.connections:
                    CanConnectionFactory.connections[channel] = CanConnection(callback, filter,
                                                                              socketcan.SocketcanBus(channel=channel))
                else:
                    CanConnectionFactory.connections[channel].addCallback(callback)
                    CanConnectionFactory.connections[channel].addFilter(filter)
                return CanConnectionFactory.connections[channel]
            else:
                raise Exception("SocketCAN on Pythoncan currently only supported in Linux")

    @staticmethod
    def loadConfiguration(configPath=None):

        CanConnectionFactory.config = Config()

        localConfig = path.dirname(__file__) + "/config.ini"
        CanConnectionFactory.config.read(localConfig)

        if configPath is not None:
            if path.exists(configPath):
                CanConnectionFactory.config.read(configPath)
            else:
                raise FileNotFoundError("Can not find config file")

    @staticmethod
    def checkKwargs(**kwargs):

        if 'interface' in kwargs:
            CanConnectionFactory.config['can']['interface'] = kwargs['interface']

        if 'baudrate' in kwargs:
            CanConnectionFactory.config['can']['baudrate'] = kwargs['baudrate']

        if 'device' in kwargs:
            CanConnectionFactory.config['peak']['device'] = kwargs['device']

        if 'appName' in kwargs:
            CanConnectionFactory.config['vector']['appName'] = kwargs['appName']

        if 'channel' in kwargs:
            CanConnectionFactory.config['vector']['channel'] = kwargs['channel']

