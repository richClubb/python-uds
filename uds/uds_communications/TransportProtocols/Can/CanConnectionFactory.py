import can
from can.interfaces import pcan, vector
from can.interfaces.vector.canlib import get_channel_configs
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
    bus = None

    @staticmethod
    def __call__(callback=None, filter=None, configPath=None, **kwargs):

        CanConnectionFactory.loadConfiguration(configPath)
        CanConnectionFactory.checkKwargs(**kwargs)

        # check config file and load
        connectionType = CanConnectionFactory.config['can']['interface']
        useFd = CanConnectionFactory.config['can']['canfd']
        baudrate = int(CanConnectionFactory.config['can']['baudrate'])
        data_baudrate = int(CanConnectionFactory.config['can']['data_baudrate'])

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
                if CanConnectionFactory.bus:
                    CanConnectionFactory.connections[channel] = CanConnection(callback, filter, CanConnectionFactory.bus, True)
                else:
                    f_clock_mhz = int(CanConnectionFactory.config['peak']['f_clock_mhz'])
                    nom_brp = int(CanConnectionFactory.config['peak']['nom_brp'])
                    nom_tseg1 = int(CanConnectionFactory.config['peak']['nom_tseg1'])
                    nom_tseg2 = int(CanConnectionFactory.config['peak']['nom_tseg2'])
                    nom_sjw = int(CanConnectionFactory.config['peak']['nom_sjw'])
                    data_brp = int(CanConnectionFactory.config['peak']['data_brp'])
                    data_tseg1 = int(CanConnectionFactory.config['peak']['data_tseg1'])
                    data_tseg2 = int(CanConnectionFactory.config['peak']['data_tseg2'])
                    data_sjw = int(CanConnectionFactory.config['peak']['data_sjw'])
                    CanConnectionFactory.connections[channel] = CanConnection(callback, filter,
                                                                            can.interface.Bus(interface='pcan', 
                                                                                                channel=channel, 
                                                                                                state=can.bus.BusState['ACTIVE'],
                                                                                                bitrate=500000, 
                                                                                                fd=useFd, 
                                                                                                f_clock_mhz=f_clock_mhz,
                                                                                                nom_brp=nom_brp,
                                                                                                nom_tseg1=nom_tseg1,
                                                                                                nom_tseg2=nom_tseg2,
                                                                                                nom_sjw=nom_sjw,
                                                                                                data_brp=data_brp,
                                                                                                data_tseg1=data_tseg1,
                                                                                                data_tseg2=data_tseg2,
                                                                                                data_sjw=data_sjw))
            else:
                CanConnectionFactory.connections[channel].addCallback(callback)
                CanConnectionFactory.connections[channel].addFilter(filter)
                
            return CanConnectionFactory.connections[channel]

        elif connectionType == 'vector':
            channel = int(CanConnectionFactory.config['vector']['channel'])
            app_name = CanConnectionFactory.config['vector']['appName']            
            connectionKey = str("{0}_{1}").format(app_name, channel)
            if connectionKey not in CanConnectionFactory.connections:
                if CanConnectionFactory.bus:
                    CanConnectionFactory.connections[connectionKey] = CanConnection(callback, filter, CanConnectionFactory.bus, True)
                else:
                    serial = None
                    if 'serial' in CanConnectionFactory.config['vector']:
                        if str(CanConnectionFactory.config['vector']['serial']).upper() == "AUTO":
                            serial = CanConnectionFactory.detectVectorSerial()
                        else:
                            serial = int(CanConnectionFactory.config['vector']['serial'])
                    CanConnectionFactory.connections[connectionKey] = CanConnection(callback, filter,
                                                                                    can.interface.Bus(bustype='vector', poll_interval=0.001, channel=channel, serial=serial, bitrate=baudrate, data_bitrate=data_baudrate, fd=useFd, app_name=app_name))
            else:
                CanConnectionFactory.connections[connectionKey].addCallback(callback)
                CanConnectionFactory.connections[connectionKey].addFilter(filter)
            return CanConnectionFactory.connections[connectionKey]

        elif connectionType == 'socketcan':
            if system() == "Linux":
                channel = CanConnectionFactory.config['socketcan']['channel']
                if channel not in CanConnectionFactory.connections:
                    CanConnectionFactory.connections[channel] = CanConnection(callback, filter,
                                                                              socketcan.SocketcanBus(channel=channel,
                                                                              fd=useFd, bitrate=baudrate, data_bitrate=data_baudrate))
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

        if 'serial' in kwargs:
            CanConnectionFactory.config['vector']['serial'] = kwargs['serial']

        if 'channel' in kwargs:
            CanConnectionFactory.config['vector']['channel'] = kwargs['channel']

        if 'bus' in kwargs:
            CanConnectionFactory.bus = kwargs['bus']

    @staticmethod
    def detectVectorSerial() -> int:
        # Get all channels configuration
        channel_configs = get_channel_configs()
        # Getting all serial numbers
        serial_numbers = set()
        for channel_config in channel_configs:
            serial_number = channel_config.serialNumber
            if serial_number != 0:
                serial_numbers.add(channel_config.serialNumber)
        if serial_numbers:
            # if several devices are discovered, the first Vector Box is chosen
            serial_number = min(serial_numbers)
            return serial_number
        return None

    @staticmethod
    def clearConnections():
        # purge connections dict at can disconnect
        CanConnectionFactory.connections = {}