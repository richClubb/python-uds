#!/usr/bin/env python

__author__ = "Richard Clubb"
__copyrights__ = "Copyright 2018, the python-uds project"
__credits__ = ["Richard Clubb"]

__license__ = "MIT"
__maintainer__ = "Richard Clubb"
__email__ = "richard.clubb@embeduk.com"
__status__ = "Development"


import can
import time
from struct import unpack

from uds import createUdsConnection
from uds import Uds

payload = []
test2Response = [0x62, 0xF1, 0x8C, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x39]


def callback_onReceive_singleFrame(msg):
    #print("Received Id: " + str(msg.arbitration_id))
    #print("Data: " + str(msg.data))
    response = [0x04, 0x62, 0xF1, 0x8C, 0x01, 0x00, 0x00, 0x00]
    outMsg = can.Message()
    outMsg.arbitration_id = 0x650
    outMsg.data = response
    bus1.send(outMsg)
    time.sleep(1)


def callback_onReceive_multiFrameResponse_noBs(msg):
    global payload
    # print("Received Id: " + str(msg.arbitration_id))
    # print("Data: " + str(msg.data))
    N_PCI = ((msg.data[0] & 0xf0) >> 4)
    outMsg = can.Message()
    outMsg.arbitration_id = 0x650
    if(N_PCI == 0):
        outMsg.data = [0x10, 19] + test2Response[0:6]
        bus1.send(outMsg)
        time.sleep(0.01)
    if(N_PCI == 3):
        outMsg.data = [0x21] + test2Response[6:13]
        bus1.send(outMsg)
        time.sleep(0.01)
        outMsg.data = [0x22] + test2Response[13:19] + [0]
        bus1.send(outMsg)
        time.sleep(0.01)

startTime = 0
lastTime = 0
def callback_onReceive_multiFrameSend(msg):
    global startTime, lastTime
    startTime = time.time()
    #print("Separation time: " + str(startTime - lastTime))
    # print("Received Id: " + str(msg.arbitration_id))
    #print("Data: " + str(msg.data))
    response = msg.data
    N_PCI = (response[0] & 0xF0) >> 4
    responsePayload = []
    outMsg = can.Message()
    outMsg.arbitration_id = 0x650
    if(N_PCI == 1):
        #print("First frame received, responding CTS")
        responsePayload = [0x30, 5, 5, 00, 00, 00, 00, 00]
        outMsg.data = responsePayload
        bus1.send(outMsg)
    elif(N_PCI == 2):
        #print("Consecutive frame received")
        if(
                (msg.data[7] == 40) |
                (msg.data[7] == 110) |
                (msg.data[7] == 180)
        ):
            #print("End of block, sending CTS")
            responsePayload = [0x30, 10, 10, 00, 00, 00, 00, 00]
            outMsg.data = responsePayload
            bus1.send(outMsg)
    lastTime = startTime

def callback_onReceive_multiFrameWithWait(msg):
    print("Received Id: " + str(msg.arbitration_id))
    print("Data: " + str(unpack('BBBBBBBB', msg.data)))
    response = msg.data
    N_PCI = (response[0] & 0xF0) >> 4
    responsePayload = []
    outMsg = can.Message()
    outMsg.arbitration_id = 0x650
    if(N_PCI == 1):
        #print("First frame received, responding CTS")
        responsePayload = [0x30, 5, 20, 00, 00, 00, 00, 00]
        outMsg.data = responsePayload
        bus1.send(outMsg)
    elif(N_PCI == 2):
        #print("Consecutive frame received")
        if(
                (msg.data[7] == 40) |
                (msg.data[7] == 75) |
                (msg.data[7] == 145) |
                (msg.data[7] == 180)
        ):
            #print("End of block, sending CTS")
            responsePayload = [0x30, 10, 10, 00, 00, 00, 00, 00]
            outMsg.data = responsePayload
            bus1.send(outMsg)
        elif( msg.data[7] == 110 ):
            #print("End of block, producing a Wait")
            responsePayload = [0x31, 0, 0, 0, 0, 0, 0, 0]
            outMsg.data = responsePayload
            bus1.send(outMsg)
            time.sleep(0.7)
            responsePayload = [0x30, 10, 10, 00, 00, 00, 00, 00]
            outMsg.data = responsePayload
            bus1.send(outMsg)

def callback_onReceive_multiFrameWith4Wait(msg):
    global startTime
    global lastTime
    startTime = time.time()
    #print("Separation time: " + str(startTime-lastTime))
    #print("Received Id: " + str(msg.arbitration_id))
    #print("Data: " + str(msg.data))
    response = msg.data
    N_PCI = (response[0] & 0xF0) >> 4
    responsePayload = []
    outMsg = can.Message()
    outMsg.arbitration_id = 0x650
    if(N_PCI == 1):
        #print("First frame received, responding CTS")
        responsePayload = [0x30, 5, 5, 00, 00, 00, 00, 00]
        outMsg.data = responsePayload
        bus1.send(outMsg)
    elif(N_PCI == 2):

        #print("Consecutive frame received")
        if(
                (msg.data[7] == 40) |
                (msg.data[7] == 75) |
                (msg.data[7] == 145) |
                (msg.data[7] == 180)
        ):
            #print("End of block, sending CTS")
            responsePayload = [0x30, 10, 127, 00, 00, 00, 00, 00]
            outMsg.data = responsePayload
            bus1.send(outMsg)
        elif( msg.data[7] == 110 ):
            #print("End of block, producing a Wait")
            responsePayload = [0x31, 0, 0, 0, 0, 0, 0, 0]
            outMsg.data = responsePayload
            bus1.send(outMsg)
            time.sleep(0.7)
            responsePayload = [0x31, 0, 0, 0, 0, 0, 0, 0]
            outMsg.data = responsePayload
            bus1.send(outMsg)
            time.sleep(0.7)
            responsePayload = [0x31, 0, 0, 0, 0, 0, 0, 0]
            outMsg.data = responsePayload
            bus1.send(outMsg)
            time.sleep(0.7)
            responsePayload = [0x31, 0, 0, 0, 0, 0, 0, 0]
            outMsg.data = responsePayload
            bus1.send(outMsg)
            time.sleep(0.7)
            responsePayload = [0x31, 0, 0, 0, 0, 0, 0, 0]
            outMsg.data = responsePayload
            bus1.send(outMsg)
            time.sleep(0.7)
            responsePayload = [0x30, 10, 127, 00, 00, 00, 00, 00]
            outMsg.data = responsePayload
            bus1.send(outMsg)
    lastTime = startTime


if __name__ == "__main__":
    bus1 = can.interface.Bus('virtualInterface', bustype="virtual")
    listener = can.Listener()
    notifier = can.Notifier(bus1, [listener], 0)

    uds = Uds(reqId=0x600, resId=0x650, interface="virtual")

    testEcu = createUdsConnection('Bootloader.odx', 'bootloader', interface="virtual")

    print("Test 1")
    listener.on_message_received = callback_onReceive_singleFrame
    resp = uds.send([0x22, 0xF1, 0x8C])
    print(resp)

    time.sleep(1)

    print("Test 2")
    listener.on_message_received = callback_onReceive_multiFrameResponse_noBs
    a = testEcu.readDataByIdentifier('ECU Serial Number')
    print(a)

    time.sleep(1)

    # print("Test 3")
    # listener.on_message_received = callback_onReceive_multiFrameSend
    # payloadRequest = []
    # for i in range(0, 200):
    #     payloadRequest.append(i)
    # udsMsg.request = payloadRequest
    # udsMsg.responseRequired = False
    # uds.send(udsMsg)
    # time.sleep(1)

    # print("Test 4")
    # listener.on_message_received = callback_onReceive_multiFrameWithWait
    # payloadRequest = []
    # for i in range(0, 200):
    #     payloadRequest.append(i)
    # udsMsg.request = payloadRequest
    # udsMsg.responseRequired = False
    # uds.send(udsMsg)

    # print("Test 5")
    # listener.on_message_received = callback_onReceive_multiFrameWith4Wait
    # payloadRequest = []
    # for i in range(0, 200):
    #     payloadRequest.append(i)
    # udsMsg.request = payloadRequest
    # udsMsg.responseRequired = False
    # uds.send(udsMsg)