#!/usr/bin/env python

__author__ = "Richard Clubb"
__copyrights__ = "Copyright 2018, the python-uds project"
__credits__ = ["Richard Clubb"]

__license__ = "MIT"
__maintainer__ = "Richard Clubb"
__email__ = "richard.clubb@embeduk.com"
__status__ = "Development"

from CanTpMessage import CanTpMessage, CanTpMessageType
from CanTpListener import CanTpListener
import can
from ITp import ITp

from Debugging import debugPrint


##
# @class CanTp
# @brief This is the main class to support CAN transport protocol
#
# Will spawn a CanTpListener class for incoming messages
# depends on a bus object for communication on CAN
class CanTp(ITp):

    ##
    # @brief constructor for the CanTp object
    def __init__(self, logger=None, reqId=None, resId=None):
        self.__bus = self.createBusConnection()
        self.__listener = CanTpListener()
        self.__listener.on_message_received = self.callback_onReceive_receiving
        self.__notifier = can.Notifier(self.__bus, [self.__listener], 0)
        self.__logger = logger
        self.__reqId = reqId
        self.__resId = resId
        self.__notifier = None
        self.__recvMsg = CanTpMessage()
        self.__recvMsg_flag = False

    ##
    # @brief connection method
    def createBusConnection(self):
        bus = can.interface.Bus('test', bustype='virtual')
        return bus

    ##
    # @brief send method
    def send(self, payload):
        msg = CanTpMessage(payload)
        canMsg = can.Message()

        if(msg.msgType == CanTpMessageType.SINGLE_FRAME):
            canMsg.data = msg.sf
            self.__bus.send(canMsg)
        elif(msg.msgType == CanTpMessageType.MULTI_FRAME):
            self.__listener.on_message_received = self.callback_onReceive_sending
            # send first frame
            canMsg.data = msg.ff
            self.__bus.send(canMsg)
            # wait for flow control

            # calculate block sizes and set up timers for stMin

            # send rest of payload

                # send consecutive frames until end of block

                # at end of block wait for flow control

                # repeat until end

            raise NotImplementedError("Multi frame transmission not yet supported")

    ##
    # @brief recv method
    def recv(self):
        msg = CanTpMessage()
        self.__listener.on_message_received = self.callback_onReceive_receiving

    ##
    # @brief the listener callback used when sending a message
    def callback_onReceive_sending(self, msg):
        debugPrint("CanTp Instance received message during sending")
        #
        self.__recvMsg = CanTpMessage(msg.data)
        self.__recvMsg_flag = True

    ##
    # @brief the listener callback used with receiving a message
    def callback_onReceive_receiving(self, msg):
        debugPrint("CanTp Instance received message during receiving")


if __name__ == "__main__":
    pass