import can
from can.interfaces import pcan, vector
from uds_configuration.ConfigSingleton import get_config


class CanConnectionFactory(object):

    connections = {}

    @staticmethod
    def __call__(config=None):

        config = get_config()

        # check config file and load
        connectionType = config['DEFAULT']['interface']

        if connectionType == 'virtual':
            connectionName = config['virtual']['interfaceName']
            if connectionName not in CanConnectionFactory.connections:
                CanConnectionFactory.connections[connectionName] = can.interface.Bus(connectionName,
                                                                                     bustype='virtual')
            return CanConnectionFactory.connections[connectionName]

        elif connectionType == 'peak':
            channel = config['peak']['device']
            if channel not in CanConnectionFactory.connections:
                baudrate = config['connection']['baudrate']
                CanConnectionFactory.connections[channel] = pcan.PcanBus(channel,
                                                                         bitrate=baudrate)
            return CanConnectionFactory.connections[channel]

        elif connectionType == 'vector':
            channel = config['vector']['channel']
            app_name = config['vector']['app_name']
            connectionKey = str("{0}_{1}").format(app_name, channel)
            if connectionKey not in CanConnectionFactory.connections:
                baudrate = int(self.__config['connection']['baudrate']) * 1000
                bus = vector.VectorBus(channel,
                                       app_name=app_name,
                                       data_bitrate=baudrate)

            return CanConnectionFactory.connections[connectionKey]
