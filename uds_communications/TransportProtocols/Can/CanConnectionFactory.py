import can
from can.interfaces import pcan, vector
from uds_configuration.Config import Config
from os import path


class CanConnectionFactory(object):

    connections = {}
    config = None

    @staticmethod
    def __call__(configPath=None, **kwargs):

        CanConnectionFactory.loadConfiguration(configPath)
        CanConnectionFactory.checkKwargs(**kwargs)

        # check config file and load
        connectionType = CanConnectionFactory.config['can']['interface']

        if connectionType == 'virtual':
            connectionName = CanConnectionFactory.config['virtual']['interfaceName']
            if connectionName not in CanConnectionFactory.connections:
                CanConnectionFactory.connections[connectionName] = can.interface.Bus(connectionName,
                                                                                     bustype='virtual')
            return CanConnectionFactory.connections[connectionName]

        elif connectionType == 'peak':
            channel = CanConnectionFactory.config['peak']['device']
            if channel not in CanConnectionFactory.connections:
                baudrate = CanConnectionFactory.config['connection']['baudrate']
                CanConnectionFactory.connections[channel] = pcan.PcanBus(channel,
                                                                         bitrate=baudrate)
            return CanConnectionFactory.connections[channel]

        elif connectionType == 'vector':
            channel = CanConnectionFactory.config['vector']['channel']
            app_name = CanConnectionFactory.config['vector']['app_name']
            connectionKey = str("{0}_{1}").format(app_name, channel)
            if connectionKey not in CanConnectionFactory.connections:
                baudrate = int(CanConnectionFactory.config['connection']['baudrate']) * 1000
                bus = vector.VectorBus(channel,
                                       app_name=app_name,
                                       data_bitrate=baudrate)

            return CanConnectionFactory.connections[connectionKey]

    @staticmethod
    def loadConfiguration(configPath=None):

        CanConnectionFactory.config = Config()

        localConfig = path.dirname(__file__) + "\config.ini"
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

