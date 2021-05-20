#!/usr/bin/env python

__author__ = "Richard Clubb"
__copyrights__ = "Copyright 2018, the python-uds project"
__credits__ = ["Richard Clubb"]

__license__ = "MIT"
__maintainer__ = "Richard Clubb"
__email__ = "richard.clubb@embeduk.com"
__status__ = "Development"

import can
from can.interfaces import pcan, vector
from time import sleep

from uds import iTp
from uds import ResettableTimer
from uds import fillArray
from uds.uds_communications.TransportProtocols.Can.CanTpTypes import CanTpAddressingTypes, CanTpState, \
    CanTpMessageType, CanTpFsTypes, CanTpMTypes
from uds.uds_communications.TransportProtocols.Can.CanTpTypes import CANTP_MAX_PAYLOAD_LENGTH, SINGLE_FRAME_DL_INDEX, \
    FIRST_FRAME_DL_INDEX_HIGH, FIRST_FRAME_DL_INDEX_LOW, FC_BS_INDEX, FC_STMIN_INDEX, N_PCI_INDEX, \
    FIRST_FRAME_DATA_START_INDEX, SINGLE_FRAME_DATA_START_INDEX, CONSECUTIVE_FRAME_SEQUENCE_NUMBER_INDEX, \
    CONSECUTIVE_FRAME_SEQUENCE_DATA_START_INDEX, FLOW_CONTROL_BS_INDEX, FLOW_CONTROL_STMIN_INDEX
from uds import CanConnectionFactory
#from uds import CanConnection
from uds import Config

from os import path


##
# @class CanTp
# @brief This is the main class to support CAN transport protocol
#
# Will spawn a CanTpListener class for incoming messages
# depends on a bus object for communication on CAN
class CanTp(iTp):

    configParams = ['reqId', 'resId', 'addressingType']

    ##
    # @brief constructor for the CanTp object
    def __init__(self, configPath=None, **kwargs):

        # perform the instance config
        self.__config = None

        self.__loadConfiguration(configPath)
        self.__checkKwargs(**kwargs)

        # load variables from the config
        self.__N_AE = int(self.__config['canTp']['N_AE'], 16)
        self.__N_TA = int(self.__config['canTp']['N_TA'], 16)
        self.__N_SA = int(self.__config['canTp']['N_SA'], 16)

        Mtype = self.__config['canTp']['Mtype']
        if (Mtype == "DIAGNOSTICS"):
            self.__Mtype = CanTpMTypes.DIAGNOSTICS
        elif (Mtype == "REMOTE_DIAGNOSTICS"):
            self.__Mtype = CanTpMTypes.REMOTE_DIAGNOSTICS
        else:
            raise Exception("Do not understand the Mtype config")

        addressingType = self.__config['canTp']['addressingType']
        if addressingType == "NORMAL":
            self.__addressingType = CanTpAddressingTypes.NORMAL
        elif addressingType == "NORMAL_FIXED":
            self.__addressingType = CanTpAddressingTypes.NORMAL_FIXED
        elif self.__addressingType == "EXTENDED":
            self.__addressingType = CanTpAddressingTypes.EXTENDED
        elif addressingType == "MIXED":
            self.__addressingType = CanTpAddressingTypes.MIXED
        else:
            raise Exception("Do not understand the addressing config")

        self.__reqId = int(self.__config['canTp']['reqId'], 16)
        self.__resId = int(self.__config['canTp']['resId'], 16)

        # sets up the relevant parameters in the instance
        if(
                (self.__addressingType == CanTpAddressingTypes.NORMAL) |
                (self.__addressingType == CanTpAddressingTypes.NORMAL_FIXED)
        ):
            self.__minPduLength = 7
            self.__maxPduLength = 63
            self.__pduStartIndex = 0
        elif(
                (self.__addressingType == CanTpAddressingTypes.EXTENDED) |
                (self.__addressingType == CanTpAddressingTypes.MIXED)
        ):
            self.__minPduLength = 6
            self.__maxPduLength = 62
            self.__pduStartIndex = 1

        # set up the CAN connection
        canConnectionFactory = CanConnectionFactory()
        self.__connection = canConnectionFactory(self.callback_onReceive,
                                                 self.__resId, # <-filter
                                                 configPath, **kwargs)

        self.__recvBuffer = []

        self.__discardNegResp = bool(self.__config['canTp']['discardNegResp'])

    ##
    # @brief used to load the local configuration options and override them with any passed in from a config file
    def __loadConfiguration(self, configPath, **kwargs):

        #load the base config
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

        if 'addressingType' in kwargs:
            self.__config['canTp']['addressingType'] = kwargs['addressingType']

        if 'reqId' in kwargs:
            self.__config['canTp']['reqId'] = str(hex(kwargs['reqId']))

        if 'resId' in kwargs:
            self.__config['canTp']['resId'] = str(hex(kwargs['resId']))

        if 'N_SA' in kwargs:
            self.__config['canTp']['N_SA'] = str(kwargs['N_SA'])

        if 'N_TA' in kwargs:
            self.__config['canTp']['N_TA'] = str(kwargs['N_TA'])

        if 'N_AE' in kwargs:
            self.__config['canTp']['N_AE'] = str(kwargs['N_AE'])

        if 'Mtype' in kwargs:
            self.__config['canTp']['Mtype'] = str(kwargs['Mtype'])

        if 'discardNegResp' in kwargs:
            self.__config['canTp']['discardNegResp'] = str(kwargs['discardNegResp'])

    ##
    # @brief connection method
    # def createBusConnection(self):
    #     # check config file and load
    #     connectionType = self.__config['DEFAULT']['interface']
    #
    #     if connectionType == 'virtual':
    #         connectionName = self.__config['virtual']['interfaceName']
    #         bus = can.interface.Bus(connectionName,
    #                                 bustype='virtual')
    #     elif connectionType == 'peak':
    #         channel = self.__config['peak']['device']
    #         baudrate = self.__config['connection']['baudrate']
    #         bus = pcan.PcanBus(channel,
    #                            bitrate=baudrate)
    #     elif connectionType == 'vector':
    #         channel = self.__config['vector']['channel']
    #         app_name = self.__config['vector']['app_name']
    #         baudrate = int(self.__config['connection']['baudrate']) * 1000
    #         bus = vector.VectorBus(channel,
    #                                app_name=app_name,
    #                                data_bitrate=baudrate)
    #
    #     return bus

    ##
    # @brief send method
    # @param [in] payload the payload to be sent
    def send(self, payload, functionalReq=False):

        payloadLength = len(payload)
        payloadPtr = 0

        state = CanTpState.IDLE

        if payloadLength > CANTP_MAX_PAYLOAD_LENGTH:
            raise Exception("Payload too large for CAN Transport Protocol")

        if payloadLength < self.__maxPduLength:
            state = CanTpState.SEND_SINGLE_FRAME
        else:
            # we might need a check for functional request as we may not be able to service functional requests for
            # multi frame requests
            state = CanTpState.SEND_FIRST_FRAME

        txPdu = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]

        sequenceNumber = 1
        endOfMessage_flag = False

        blockList = []
        currBlock = []

        ## this needs fixing to get the timing from the config
        timeoutTimer = ResettableTimer(1)
        stMinTimer = ResettableTimer()

        self.clearBufferedMessages()

        while endOfMessage_flag is False:

            rxPdu = self.getNextBufferedMessage()

            if rxPdu is not None:
                N_PCI = (rxPdu[0] & 0xF0) >> 4
                if N_PCI == CanTpMessageType.FLOW_CONTROL:
                    fs = rxPdu[0] & 0x0F
                    if fs == CanTpFsTypes.WAIT:
                        raise Exception("Wait not currently supported")
                    elif fs == CanTpFsTypes.OVERFLOW:
                        raise Exception("Overflow received from ECU")
                    elif fs == CanTpFsTypes.CONTINUE_TO_SEND:
                        if state == CanTpState.WAIT_FLOW_CONTROL:
                            if fs == CanTpFsTypes.CONTINUE_TO_SEND:
                                bs = rxPdu[FC_BS_INDEX]
                                if(bs == 0):
                                    bs = 585
                                blockList = self.create_blockList(payload[payloadPtr:],
                                                                  bs)
                                stMin = self.decode_stMin(rxPdu[FC_STMIN_INDEX])
                                currBlock = blockList.pop(0)
                                state = CanTpState.SEND_CONSECUTIVE_FRAME
                                stMinTimer.timeoutTime = stMin
                                stMinTimer.start()
                                timeoutTimer.stop()
                        else:
                            raise Exception("Unexpected Flow Control Continue to Send request")
                    else:
                        raise Exception("Unexpected fs response from ECU")
                else:
                    raise Exception("Unexpected response from device")

            if state == CanTpState.SEND_SINGLE_FRAME:
                if len(payload) <= self.__minPduLength:
                    txPdu[N_PCI_INDEX] += (CanTpMessageType.SINGLE_FRAME << 4)
                    txPdu[SINGLE_FRAME_DL_INDEX] += payloadLength
                    txPdu[SINGLE_FRAME_DATA_START_INDEX:] = fillArray(payload, self.__minPduLength)
                else:
                    txPdu[N_PCI_INDEX] = 0
                    txPdu[FIRST_FRAME_DL_INDEX_LOW] = payloadLength
                    txPdu[FIRST_FRAME_DATA_START_INDEX:] = payload
                self.transmit(txPdu, functionalReq)
                endOfMessage_flag = True
            elif state == CanTpState.SEND_FIRST_FRAME:
                payloadLength_highNibble = (payloadLength & 0xF00) >> 8
                payloadLength_lowNibble  = (payloadLength & 0x0FF)
                txPdu[N_PCI_INDEX] += (CanTpMessageType.FIRST_FRAME << 4)
                txPdu[FIRST_FRAME_DL_INDEX_HIGH] += payloadLength_highNibble
                txPdu[FIRST_FRAME_DL_INDEX_LOW] += payloadLength_lowNibble
                txPdu[FIRST_FRAME_DATA_START_INDEX:] = payload[0:self.__maxPduLength-1]
                payloadPtr += self.__maxPduLength-1
                self.transmit(txPdu, functionalReq)
                timeoutTimer.start()
                state = CanTpState.WAIT_FLOW_CONTROL
            elif state == CanTpState.SEND_CONSECUTIVE_FRAME:
                if(stMinTimer.isExpired()):
                    txPdu[N_PCI_INDEX] += (CanTpMessageType.CONSECUTIVE_FRAME << 4)
                    txPdu[CONSECUTIVE_FRAME_SEQUENCE_NUMBER_INDEX] += sequenceNumber
                    txPdu[CONSECUTIVE_FRAME_SEQUENCE_DATA_START_INDEX:] = currBlock.pop(0)
                    payloadPtr += self.__maxPduLength
                    self.transmit(txPdu, functionalReq)
                    sequenceNumber = (sequenceNumber + 1) % 16
                    stMinTimer.restart()
                    if(len(currBlock) == 0):
                        if(len(blockList) == 0):
                            endOfMessage_flag = True
                        else:
                            timeoutTimer.start()
                            state = CanTpState.WAIT_FLOW_CONTROL
                            #print("waiting for flow control")

            txPdu = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
            # timer / exit condition checks
            if(timeoutTimer.isExpired()):
                raise Exception("Timeout waiting for message")

            sleep(0.01)

    ##
    # @brief recv method
    # @param [in] timeout_ms The timeout to wait before exiting
    # @return a list
    def recv(self, timeout_s):

        timeoutTimer = ResettableTimer(timeout_s)

        payload = []
        payloadPtr = 0
        payloadLength = None

        sequenceNumberExpected = 1

        txPdu = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]

        endOfMessage_flag = False

        state = CanTpState.IDLE

        timeoutTimer.start()
        while endOfMessage_flag is False:

            rxPdu = self.getNextBufferedMessage()

            if rxPdu is not None:
                if rxPdu[N_PCI_INDEX] == 0x00:
                    rxPdu = rxPdu[1:]
                    N_PCI = 0
                else:
                    N_PCI = (rxPdu[N_PCI_INDEX] & 0xF0) >> 4
                if state == CanTpState.IDLE:
                    if N_PCI == CanTpMessageType.SINGLE_FRAME:
                        payloadLength = rxPdu[N_PCI_INDEX & 0x0F]
                        payload = rxPdu[SINGLE_FRAME_DATA_START_INDEX: SINGLE_FRAME_DATA_START_INDEX + payloadLength]
                        endOfMessage_flag = True
                    elif N_PCI == CanTpMessageType.FIRST_FRAME:
                        payload = rxPdu[FIRST_FRAME_DATA_START_INDEX:]
                        payloadLength = ((rxPdu[FIRST_FRAME_DL_INDEX_HIGH] & 0x0F) << 8) + rxPdu[FIRST_FRAME_DL_INDEX_LOW]
                        payloadPtr = self.__maxPduLength - 1
                        state = CanTpState.SEND_FLOW_CONTROL
                elif state == CanTpState.RECEIVING_CONSECUTIVE_FRAME:
                    if N_PCI == CanTpMessageType.CONSECUTIVE_FRAME:
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

            if state == CanTpState.SEND_FLOW_CONTROL:
                txPdu[N_PCI_INDEX] = 0x30
                txPdu[FLOW_CONTROL_BS_INDEX] = 0
                txPdu[FLOW_CONTROL_STMIN_INDEX] = 0x1E
                self.transmit(txPdu)
                state = CanTpState.RECEIVING_CONSECUTIVE_FRAME

            if payloadLength is not None:
                if payloadPtr >= payloadLength:
                    endOfMessage_flag = True

            if timeoutTimer.isExpired():
                raise Exception("Timeout in waiting for message")

        return list(payload[:payloadLength])

    ##
    # dummy function for the time being
    def closeConnection(self):
        # deregister filters, listeners and notifiers etc
        # close can connection
        CanConnectionFactory.clearConnections()
        self.__connection.shutdown()
        self.__connection = None

    ##
    # @brief clear out the receive list
    def clearBufferedMessages(self):
        self.__recvBuffer = []

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
    # @brief the listener callback used when a message is received
    def callback_onReceive(self, msg):
        if self.__addressingType == CanTpAddressingTypes.NORMAL:
            if msg.arbitration_id == self.__resId:
                self.__recvBuffer.append(msg.data[self.__pduStartIndex:])
        elif self.__addressingType == CanTpAddressingTypes.NORMAL_FIXED:
            raise Exception("I do not know how to receive this addressing type yet")
        elif self.__addressingType == CanTpAddressingTypes.MIXED:
            raise Exception("I do not know how to receive this addressing type yet")
        else:
            raise Exception("I do not know how to receive this addressing type")

    ##
    # @brief function to decode the StMin parameter
    @staticmethod
    def decode_stMin(val):
        if (val <= 0x7F):
            time = val / 1000
            return time
        elif (
                (val >= 0xF1) &
                (val <= 0xF9)
        ):
            time = (val & 0x0F) / 10000
            return time
        else:
            raise Exception("Unknown STMin time")

    ##
    # @brief creates the blocklist from the blocksize and payload
    def create_blockList(self, payload, blockSize):

        blockList = []
        currBlock = []
        currPdu = []

        payloadPtr = 0
        blockPtr = 0

        payloadLength = len(payload)
        pduLength = self.__maxPduLength
        blockLength = blockSize * pduLength

        working = True
        while(working):
            if (payloadPtr + pduLength) >= payloadLength:
                working = False
                currPdu = fillArray(payload[payloadPtr:], pduLength)
                currBlock.append(currPdu)
                blockList.append(currBlock)

            if working:
                currPdu = payload[payloadPtr:payloadPtr+pduLength]
                currBlock.append(currPdu)
                payloadPtr += pduLength
                blockPtr += pduLength

                if(blockPtr == blockLength):
                    blockList.append(currBlock)
                    currBlock = []
                    blockPtr = 0

        return blockList

    ##
    # @brief transmits the data over can using can connection
    # def transmit(self, data, functionalReq=False):
    #
    #     # check functional request
    #     if functionalReq:
    #         raise Exception("Functional requests are currently not supported")
    #     else:
    #         self.__connection.transmit(data, self.__reqId, self.__addressingType)

    def transmit(self, data, functionalReq=False):
        # check functional request
        if functionalReq:
            raise Exception("Functional requests are currently not supported")

        transmitData = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]

        if (
            (self.__addressingType == CanTpAddressingTypes.NORMAL) |
            (self.__addressingType == CanTpAddressingTypes.NORMAL_FIXED)
        ):
            transmitData = data
        elif self.__addressingType == CanTpAddressingTypes.MIXED:
            transmitData[0] = self.__N_AE
            transmitData[1:] = data
        else:
            raise Exception("I do not know how to send this addressing type")

        self.__connection.transmit(transmitData, self.__reqId, )

    @property
    def reqIdAddress(self):
        return self.__reqId

    @reqIdAddress.setter
    def reqIdAddress(self, value):
        self.__reqId = value

    @property
    def resIdAddress(self):
        return self.__resId

    @resIdAddress.setter
    def resIdAddress(self, value):
        self.__resId = value

    