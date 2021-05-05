#!/usr/bin/env python

__author__ = "Richard Clubb"
__copyrights__ = "Copyright 2018, the python-uds project"
__credits__ = ["Richard Clubb"]

__license__ = "MIT"
__maintainer__ = "Richard Clubb"
__email__ = "richard.clubb@embeduk.com"
__status__ = "Development"


from os import path
from time import sleep

from lin import LinBus
#from lin import LinBusFactory
from uds import iTp
from uds import Config
from uds import ResettableTimer
from uds import fillArray


# types
from uds.uds_communications.TransportProtocols.Lin.LinTpTypes import LinTpState, LinTpMessageType

# consts
from uds.uds_communications.TransportProtocols.Lin.LinTpTypes import LINTP_MAX_PAYLOAD_LENGTH, N_PCI_INDEX, \
    SINGLE_FRAME_DL_INDEX, SINGLE_FRAME_DATA_START_INDEX, \
    FIRST_FRAME_DL_INDEX_HIGH, FIRST_FRAME_DL_INDEX_LOW, FIRST_FRAME_DATA_START_INDEX, \
    CONSECUTIVE_FRAME_SEQUENCE_NUMBER_INDEX, CONSECUTIVE_FRAME_SEQUENCE_DATA_START_INDEX

class LinTp(iTp):

    #__metaclass__ = iTp

    def __init__(self, configPath=None, **kwargs):

        # perform the instance config
        self.__config = None

        self.__loadConfiguration(configPath)
        self.__checkKwargs(**kwargs)

        self.__maxPduLength = 6

        self.__NAD = int(self.__config["linTp"]["nodeAddress"], 16)
        self.__STMin = float(self.__config["linTp"]["STMin"])

        # hardcoding the baudrate for the time being
        self.__connection = LinBus.LinBus(19200)  # ... TODO: replace with something like the following
        #self.__connection = LinBusFactory.LinBusFactory(linBusType="Peak",baudrate=19200)   # ... TODO: replace with defined values rather than variables
        self.__connection.on_message_received = self.callback_onReceive
        # self.__connection.on_message_received = self.callback_onReceive  ... needs to be replaced as handled internall in the LIN bus impl
        self.__connection.startDiagnosticSchedule()
        #self.__connection.startSchedule()  # ... replaced by this

        self.__recvBuffer = []
        self.__transmitBuffer = None

    def send(self, payload, functionalReq=False):  # TODO: functionalReq not used???
        #self.__connection.send(payload)  # .... implemented in the LIN bus impl, so the rest of function replaced by this
        payloadLength = len(payload)

        if payloadLength > LINTP_MAX_PAYLOAD_LENGTH:
            raise Exception("Payload too large for CAN Transport Protocol")

        if payloadLength <= self.__maxPduLength:
            state = LinTpState.SEND_SINGLE_FRAME
        else:
            # we might need a check for functional request as we may not be able to service functional requests for
            # multi frame requests
            state = LinTpState.SEND_FIRST_FRAME
            firstFrameData = payload[0:self.__maxPduLength-1]
            cfBlocks = self.create_blockList(payload[5:])
            sequenceNumber = 1

        txPdu = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]

        endOfMessage_flag = False

        ## this needs fixing to get the timing from the config
        timeoutTimer = ResettableTimer(1)
        stMinTimer = ResettableTimer(self.__STMin)

        self.clearBufferedMessages()

        timeoutTimer.start()
        while endOfMessage_flag is False:

            rxPdu = self.getNextBufferedMessage()

            if rxPdu is not None:
                raise Exception("Unexpected receive frame")

            if state == LinTpState.SEND_SINGLE_FRAME:
                txPdu[N_PCI_INDEX] += (LinTpMessageType.SINGLE_FRAME << 4)
                txPdu[SINGLE_FRAME_DL_INDEX] += payloadLength
                txPdu[SINGLE_FRAME_DATA_START_INDEX:] = fillArray(payload, self.__maxPduLength)
                self.transmit(txPdu)
                endOfMessage_flag = True
            elif state == LinTpState.SEND_FIRST_FRAME:
                payloadLength_highNibble = (payloadLength & 0xF00) >> 8
                payloadLength_lowNibble  = (payloadLength & 0x0FF)
                txPdu[N_PCI_INDEX] += (LinTpMessageType.FIRST_FRAME << 4)
                txPdu[FIRST_FRAME_DL_INDEX_HIGH] += payloadLength_highNibble
                txPdu[FIRST_FRAME_DL_INDEX_LOW] += payloadLength_lowNibble
                txPdu[FIRST_FRAME_DATA_START_INDEX:] = firstFrameData
                self.transmit(txPdu)
                state = LinTpState.SEND_CONSECUTIVE_FRAME
                stMinTimer.start()
                timeoutTimer.restart()
            elif state == LinTpState.SEND_CONSECUTIVE_FRAME:
                if(
                        stMinTimer.isExpired() and
                        (self.__transmitBuffer is None)
                ):
                    txPdu[N_PCI_INDEX] += (LinTpMessageType.CONSECUTIVE_FRAME << 4)
                    txPdu[CONSECUTIVE_FRAME_SEQUENCE_NUMBER_INDEX] += sequenceNumber
                    txPdu[CONSECUTIVE_FRAME_SEQUENCE_DATA_START_INDEX:] = cfBlocks.pop(0)
                    self.transmit(txPdu)
                    sequenceNumber = (sequenceNumber + 1) % 16
                    stMinTimer.restart()
                    timeoutTimer.restart()

                    if len(cfBlocks) == 0:
                        endOfMessage_flag = True

            txPdu = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]

            sleep(0.001)

            if timeoutTimer.isExpired(): raise Exception("Timeout")

    def recv(self, timeout_s):
        #return self.__connection.recv(... can pass timeout from here if required ...)  # .... implemented in the LIN bus impl, so the rest of function replaced by this
        timeoutTimer = ResettableTimer(timeout_s)

        payload = []
        payloadPtr = 0
        payloadLength = None

        sequenceNumberExpected = 1

        endOfMessage_flag = False

        state = LinTpState.IDLE

        timeoutTimer.start()
        while endOfMessage_flag is False:

            rxPdu = self.getNextBufferedMessage()

            if rxPdu is not None:
                N_PCI = (rxPdu[N_PCI_INDEX] & 0xF0) >> 4
                if state == LinTpState.IDLE:
                    if N_PCI == LinTpMessageType.SINGLE_FRAME:
                        payloadLength = rxPdu[N_PCI_INDEX & 0x0F]
                        payload = rxPdu[SINGLE_FRAME_DATA_START_INDEX: SINGLE_FRAME_DATA_START_INDEX + payloadLength]
                        endOfMessage_flag = True
                    elif N_PCI == LinTpMessageType.FIRST_FRAME:
                        payload = rxPdu[FIRST_FRAME_DATA_START_INDEX:]
                        payloadLength = ((rxPdu[FIRST_FRAME_DL_INDEX_HIGH] & 0x0F) << 8) + rxPdu[
                            FIRST_FRAME_DL_INDEX_LOW]
                        payloadPtr = self.__maxPduLength - 1
                        state = LinTpState.RECEIVING_CONSECUTIVE_FRAME
                        timeoutTimer.restart()
                elif state == LinTpState.RECEIVING_CONSECUTIVE_FRAME:
                    if N_PCI == LinTpMessageType.CONSECUTIVE_FRAME:
                        sequenceNumber = rxPdu[CONSECUTIVE_FRAME_SEQUENCE_NUMBER_INDEX] & 0x0F
                        if sequenceNumber != sequenceNumberExpected:
                            raise Exception("Consecutive frame sequence out of order")
                        else:
                            sequenceNumberExpected = (sequenceNumberExpected + 1) % 16
                        payload += rxPdu[CONSECUTIVE_FRAME_SEQUENCE_DATA_START_INDEX:]
                        payloadPtr += (self.__maxPduLength)
                        timeoutTimer.restart()
                    else:
                        raise Exception("Unexpected PDU received")

            if payloadLength is not None:
                if payloadPtr >= payloadLength:
                    endOfMessage_flag = True

            if timeoutTimer.isExpired():
                raise Exception("Timeout in waiting for message")

        return list(payload[:payloadLength])

    ##
    # dummy function for the time being
    def closeConnection(self):
        #self.__connection.disconnect()  # .... implemented in the LIN bus impl, so the rest of function replaced by this
        self.__connection.closeConnection()

    def callback_onReceive(self, msg):
        msgNad = msg.payload[0]
        msgFrameId = msg.frameId

        #print("Received message")

        if msgNad == self.__NAD:
            if msgFrameId == 0x3C:
                if msg.payload == self.__transmitBuffer:
                    self.__transmitBuffer = None

            elif msgFrameId == 0x3D or 125:

                self.__recvBuffer.append(msg.payload[1:8])

    ##
    # @brief clear out the receive list
    def clearBufferedMessages(self):
        self.__recvBuffer = []
        self.__transmitBuffer = None

    ##
    # @brief retrieves the next message from the received message buffers
    # @return list, or None if nothing is on the receive list
    def getNextBufferedMessage(self):
        length = len(self.__recvBuffer)
        if(length != 0):
            return self.__recvBuffer.pop(0)
        else:
            return None

    ##
    # @brief creates the blocklist from the blocksize and payload
    def create_blockList(self, payload):
        blockList = []
        currBlock = []

        payloadLength = len(payload)
        counter = 0

        for i in range(0, payloadLength):

            currBlock.append(payload[i])
            counter += 1

            if counter == self.__maxPduLength:
                blockList.append(currBlock)
                counter = 0
                currBlock = []

        if len(currBlock) != 0:
            blockList.append(fillArray(currBlock, self.__maxPduLength))

        return blockList

    # This function is effectively moved down to the LIN bus impl (i.e. only called from within send() which is moving down
    def transmit(self, payload):
        txPdu = [self.__NAD] + payload
        self.__connection.sendMasterRequest(txPdu)
        self.__transmitBuffer = txPdu

    """
    def addSchedule(self):
        #self.__connection.addSchedule(index???)  # .... implemented in the LIN bus impl, so the rest of function replaced by this

    def startSchedule(self):
        #self.__connection.startSchedule(index???)  # .... implemented in the LIN bus impl, so the rest of function replaced by this

    def pauseSchedule(self):
        #self.__connection.pauseSchedule(index???)  # .... implemented in the LIN bus impl, so the rest of function replaced by this

    def stopSchedule(self):
        #self.__connection.stopSchedule(index???)  # .... implemented in the LIN bus impl, so the rest of function replaced by this
    """

    def wakeup(self):
        #self.__connection.wakeBus(index???)  # .... implemented in the LIN bus impl, so the rest of function replaced by this
        self.__connection.wakeup()


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
        if 'nodeAddress' in kwargs:
            self.__config['linTp']['nodeAddress'] = str(hex(kwargs['nodeAddress']))

        if 'STMin' in kwargs:
            self.__config['linTp']['STMin'] = str(kwargs['STMin'])
