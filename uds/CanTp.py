#!/usr/bin/env python

__author__ = "Richard Clubb"
__copyrights__ = "Copyright 2018, the python-uds project"
__credits__ = ["Richard Clubb"]

__license__ = "MIT"
__maintainer__ = "Richard Clubb"
__email__ = "richard.clubb@embeduk.com"
__status__ = "Development"

from CanTpTypes import CanTpTimeoutWaitingForFlowControl, CanTpMessageType, CanTpFsType, CanTpMessageState
from CanTpMessage import CanTpMessage
import can
from can.interfaces.pcan import pcan
from iTp import iTp
import time
import os
import sys
import config


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
        self.__config = None

        self.__bus = self.createBusConnection()
        self.__listener = can.Listener()
        self.__listener.on_message_received = self.callback_onReceive
        self.__notifier = can.Notifier(self.__bus, [self.__listener], 1)

        self.__reqId = reqId
        self.__resId = resId

        self.__recvMsg = CanTpMessage()
        self.__recvBuffer = []
        self.__recvMsg_flag = False

        if(self.__config is not None):
            self.__stMin = int(self.__config['canTp']['STMin_default'])
            self.__bs = int(self.__config['canTp']['BS_default'])
            self.__timeout = int(self.__config['canTp']['Send_Timeout'])
            self.__N_WFTmax = int(self.__config['canTp']['N_WFTmax'])
        else:
            self.__stMin = 10
            self.__bs = 0
            self.__timeout = 10000
            self.__N_WFTmax = 3
        self.__N_WFT = 0

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
        self.__recvBuffer = []
        self.__N_WFT = 0
        msg = CanTpMessage(payload)
        outMsg = can.Message()
        outMsg.arbitration_id = self.__reqId

        startTime = time_ms()
        waitingForResponse = True
        timeout = self.__timeout
        while(waitingForResponse & (msg.messageState != CanTpMessageState.FINISHED)):

            response = self.getNextBufferedMessage()
            if(response is not None):
                startTime = time_ms()
                stMin, wait_flag = msg.processResponse(response)

                if(
                        (stMin is None) &
                        (wait_flag is True)
                ):
                    self.__N_WFT += 1
                    time.sleep(1)
                elif(stMin is not None):
                    self.__stMin = stMin
                    self.__N_WFT = 0

            output = msg.getNextSendFrame()
            if(output is not None):
                outMsg.data = output
                self.__bus.send(outMsg)
                startTime = time_ms()

            currTime = time_ms()
            if((currTime - startTime) > timeout):
                raise Exception("Timeout")

            if(self.__N_WFT >= self.__N_WFTmax):
                raise Exception("Too many waits")

            time.sleep(self.__stMin / 1000)

    ##
    # @brief recv method
    # @param [in] timeout_ms The timeout to wait before exiting
    # @return a list
    def recv(self, timeout_ms):
        msg = CanTpMessage()
        startTime = time_ms()
        waitingForResponse = True
        outputMsg = can.Message()
        while(waitingForResponse):

            # if a message is pending
            response = self.getNextBufferedMessage()
            if(response is not None):
                #process the message
                msg.processResponse(response)

            #prepare to send the next
            output = msg.getNextReceiveFrame()
            if(output is not None):
                outputMsg.data = output
                self.__bus.send(outputMsg)

            if(msg.messageState == CanTpMessageState.FINISHED):
                output = msg.payload
                msg.reset()
                return output

            currTime = time_ms()
            if((currTime - startTime) > timeout_ms):
                waitingForResponse = False
                raise Exception("Timeout waiting for response")

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
            self.__recvBuffer.append(msg.data)

    ##
    # @brief closes down the connection
    def close(self):
        # shut down the listener
        pass


if __name__ == "__main__":
    canTp = CanTp()
    pass
