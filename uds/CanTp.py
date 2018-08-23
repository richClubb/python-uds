#!/usr/bin/env python

__author__ = "Richard Clubb"
__copyrights__ = "Copyright 2018, the python-uds project"
__credits__ = ["Richard Clubb"]

__license__ = "MIT"
__maintainer__ = "Richard Clubb"
__email__ = "richard.clubb@embeduk.com"
__status__ = "Development"

from CanTpTypes import CanTpMessageState, CanTpState, CanTpMessageType, CanTpFsType
from CanTpMessage import CanTpMessage
import can
from iTp import iTp
import time
from Utilities.ResettableTimer import ResettableTimer
from struct import unpack


def time_ms():
    return time.time() * 1000


##
# @class CanTp
# @brief This is the main class to support CAN transport protocol
#
# Will spawn a CanTpListener class for incoming messages
# depends on a bus object for communication on CAN
class CanTp(iTp):

    ##
    # @brief constructor for the CanTp object
    def __init__(self, reqId=None, resId=None):

        self.__bus = self.createBusConnection()

        # there probably needs to be an adapter to deal with these parts as they couple to python-can heavily
        self.__listener = can.Listener()
        self.__listener.on_message_received = self.callback_onReceive
        self.__notifier = can.Notifier(self.__bus, [self.__listener], 0)

        self.__reqId = reqId
        self.__resId = resId

        self.__messageTimeout_s = 5
        self.__recvBuffer = []

        self.__stMin = 0.001
        self.__waitPeriod = 1
        self.__waitCounterMax = 3
    ##
    # @brief connection method
    def createBusConnection(self):
        # check config file and load
        bus = can.interface.Bus('test', bustype='virtual')
        #bus = pcan.PcanBus('PCAN_USBBUS1')
        return bus

    ##
    # @brief send method
    # @param [in] payload the payload to be sent
    def send(self, payload):

        # function initialisation
        tpMessage = CanTpMessage(payload)
        state = CanTpState.IDLE

        #timers
        timeoutTimer = ResettableTimer(self.__messageTimeout_s)
        separationTimer = ResettableTimer(self.__stMin)
        waitTimer = ResettableTimer(self.__waitPeriod)

        waitCounter = 0

        sequenceNumber = 0

        waitingForFcCts = False

        #can output variables
        canMsg = can.Message()
        canMsg.arbitration_id = self.__reqId

        # start processing the message
        timeoutTimer.start()
        okToSend = True

        # continue to process until the end of the message or until the message times
        while(
                (tpMessage.isEndOfMessage() == False) & # this could probably be changed to a state query
                (timeoutTimer.expired() == False)
        ):
            # wait monitoring
            # gets current message state and controls output

            if(tpMessage.state == CanTpMessageState.SINGLE_FRAME):
                canPdu = tpMessage.processState()
                canPduLength = tpMessage.length
                N_PCI = (CanTpMessageType.SINGLE_FRAME << 4) | canPduLength
                canFrame = [N_PCI] + canPdu
                canMsg.data = canFrame
                self.__bus.send(canMsg)
            elif(tpMessage.state == CanTpMessageState.FIRST_FRAME):
                canPdu = tpMessage.processState()
                canPduLength = tpMessage.length
                N_PCI_highByte = (CanTpMessageType.FIRST_FRAME << 4) | (canPduLength & 0xF00) >> 8
                N_PCI_lowByte = (canPduLength & 0x0FF)
                canFrame = [N_PCI_highByte, N_PCI_lowByte] + canPdu
                canMsg.data = canFrame
                self.__bus.send(canMsg)
            elif(tpMessage.state == CanTpMessageState.CONSECUTIVE_FRAME):
                if(okToSend):
                    canPdu = tpMessage.processState()
                    N_PCI = (CanTpMessageType.CONSECUTIVE_FRAME << 4) | sequenceNumber
                    canFrame = [N_PCI] + canPdu
                    canMsg.data = canFrame
                    self.__bus.send(canMsg)
                    separationTimer.reset()
                    sequenceNumber = (sequenceNumber + 1) % 16
            elif(tpMessage.state == CanTpMessageState.END_OF_BLOCK):
                _ = tpMessage.processState()
                separationTimer.reset()

            if(tpMessage.state == CanTpMessageState.END_OF_BLOCK):
                waitingForFcCts = True

            # process responses
            response = self.getNextBufferedMessage()
            if(response is not None):
                responseType = (response[0] & 0xF0) >> 4
                if(responseType == CanTpMessageType.FLOW_CONTROL):
                    fsType = response[0] & 0x0F
                    if(fsType == CanTpFsType.OVERFLOW):
                        raise Exception("Overflow error")
                    elif(fsType == CanTpFsType.WAIT):
                        waitTimer.start()
                        waitCounter += 1
                    elif(fsType == CanTpFsType.CONTINUE_TO_SEND):
                        if(waitingForFcCts):
                            waitCounter = 0
                            bs = response[1]
                            tpMessage.blockPayload(bs)
                            stMin = self.decode_stMin(response[2])
                            separationTimer.timeoutTime = stMin
                            timeoutTimer.reset()
                            waitingForFcCts = False
                        else:
                            raise Exception("Received message out of sequence")
                else:
                    raise Exception("Unexpected result")

            okToSend = True
            if(
                    separationTimer.isRunning()  |
                    waitingForFcCts is True
            ):
                okToSend = False

    ##
    # @brief recv method
    # @param [in] timeout_ms The timeout to wait before exiting
    # @return a list
    def recv(self, timeout_ms):
        timeoutTimer = ResettableTimer(timeout_ms)

        timeoutTimer.start()
        state = CanTpState.IDLE
        output = []
        payloadPtr = 0

        canMsg = can.Message()
        canMsg.arbitration_id = 0x600
        canMsg.data = [0x30, 00, 00, 00, 00, 00, 00, 00]

        sequenceNumber_last = None

        lengthExpected = 0

        while(
                (state != CanTpState.FINISHED) &
                (timeoutTimer.expired() == False)
        ):

            response = self.getNextBufferedMessage()
            if(response is not None):
                N_PCI = (response[0] & 0xF0) >> 4
                if(N_PCI == CanTpMessageType.SINGLE_FRAME):
                    state = CanTpState.RECEIVING_SINGLE_FRAME
                elif(N_PCI == CanTpMessageType.FIRST_FRAME):
                    state = CanTpState.RECEIVING_FIRST_FRAME
                elif(N_PCI == CanTpMessageType.CONSECUTIVE_FRAME):
                    pass
                elif(N_PCI == CanTpMessageType.FLOW_CONTROL):
                    raise Exception("Out of sequence error")

                if(state == CanTpState.RECEIVING_SINGLE_FRAME):
                    lengthExpected = response[0] & 0x0F
                    output = response[1:lengthExpected+1]
                    state = CanTpState.FINISHED
                elif(state == CanTpState.RECEIVING_FIRST_FRAME):
                    lengthExpected = ((response[0] & 0x0F) << 8) + (response[1])
                    output = response[2:]
                    payloadPtr = 6
                    self.__bus.send(canMsg)
                    state = CanTpState.RECEIVING_CONSECUTIVE_FRAME
                elif(state == CanTpState.RECEIVING_CONSECUTIVE_FRAME):
                    if (N_PCI != CanTpMessageType.CONSECUTIVE_FRAME):
                        raise Exception("Out of sequence error")

                    sequenceNumber_curr = response[0] & 0x0F
                    if(sequenceNumber_last is None):
                        if(sequenceNumber_curr != 0):
                            raise Exception("Sequence number out of sequence")
                    else:
                        sequenceNumber_expected = (sequenceNumber_last + 1) % 16
                        if(sequenceNumber_curr != sequenceNumber_expected):
                            raise Exception("Sequence number out of sequence")

                    output += response[1:]
                    payloadPtr += 7
                    sequenceNumber_last = sequenceNumber_curr

                    if(payloadPtr >= lengthExpected):
                        state = CanTpState.FINISHED
                        output = output[:lengthExpected]

        convertedOutput = []
        for i in range(0, len(output)):
            convertedOutput.append(output[i])
        return convertedOutput

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
        if(msg.arbitration_id == self.__resId):
            print("CanTp Instance received message")
            print(unpack('BBBBBBBB', msg.data))
            self.__recvBuffer.append(msg.data)

    ##
    # @brief function to decode the StMin parameter
    def decode_stMin(self, val):
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
    # @brief closes down the connection
    def close(self):
        # shut down the listener
        pass


if __name__ == "__main__":
    canTp = CanTp()
    pass
