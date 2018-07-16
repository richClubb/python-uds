import can
import Uds
import UdsMessage
import time

payload = []
test2Response = [0x62, 0xF1, 0x8C, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]


def callback_onReceive_singleFrame(msg):
    print("Received Id: " + str(msg.arbitration_id))
    print("Data: " + str(msg.data))
    time.sleep(2)
    response = [0x04, 0x62, 0xF1, 0x8C, 0x01, 0x00, 0x00, 0x00]
    outMsg = can.Message()
    outMsg.arbitration_id = 0x650
    outMsg.data = response
    bus1.send(outMsg)
    time.sleep(1)


def callback_onReceive_multiFrameResponse_noBs(msg):
    global payload
    print("Received Id: " + str(msg.arbitration_id))
    print("Data: " + str(msg.data))
    N_PCI = ((msg.data[0] & 0xf0) >> 4)
    outMsg = can.Message()
    outMsg.arbitration_id = 0x650
    if(N_PCI == 0):
        outMsg.data = [0x10, 19] + test2Response[0:6]
        bus1.send(outMsg)
        time.sleep(0.01)
    if(N_PCI == 3):
        outMsg.data = [0x20] + test2Response[6:13]
        bus1.send(outMsg)
        time.sleep(0.01)
        outMsg.data = [0x21] + test2Response[13:19] + [0]
        bus1.send(outMsg)
        time.sleep(0.01)


def callback_onReceive_multiFrameSend(msg):
    print("Received Id: " + str(msg.arbitration_id))
    print("Data: " + str(msg.data))
    response = msg.data
    N_PCI = (response[0] & 0xF0) >> 4
    responsePayload = []
    outMsg = can.Message()
    outMsg.arbitration_id = 0x650
    if(N_PCI == 1):
        print("First frame received, responding CTS")
        responsePayload = [0x30, 5, 20, 00, 00, 00, 00, 00]
        outMsg.data = responsePayload
        bus1.send(outMsg)
    elif(N_PCI == 2):
        print("Consecutive frame received")
        if(
                (msg.data[7] == 75) |
                (msg.data[7] == 145)
        ):
            print("End of block, sending CTS")
            responsePayload = [0x30, 10, 10, 00, 00, 00, 00, 00]
            outMsg.data = responsePayload
            bus1.send(outMsg)


def callback_onReceive_multiFrameWithWait(msg):
    print("Received Id: " + str(msg.arbitration_id))
    print("Data: " + str(msg.data))
    response = msg.data
    N_PCI = (response[0] & 0xF0) >> 4
    responsePayload = []
    outMsg = can.Message()
    outMsg.arbitration_id = 0x650
    if(N_PCI == 1):
        print("First frame received, responding CTS")
        responsePayload = [0x30, 5, 20, 00, 00, 00, 00, 00]
        outMsg.data = responsePayload
        bus1.send(outMsg)
    elif(N_PCI == 2):
        print("Consecutive frame received")
        if(
                (msg.data[7] == 40) |
                (msg.data[7] == 75) |
                (msg.data[7] == 145) |
                (msg.data[7] == 180)
        ):
            print("End of block, sending CTS")
            responsePayload = [0x30, 10, 10, 00, 00, 00, 00, 00]
            outMsg.data = responsePayload
            bus1.send(outMsg)
        elif( msg.data[7] == 110 ):
            print("End of block, producing a Wait")
            responsePayload = [0x31, 0, 0, 0, 0, 0, 0, 0]
            outMsg.data = responsePayload
            bus1.send(outMsg)
            time.sleep(0.7)
            responsePayload = [0x30, 10, 10, 00, 00, 00, 00, 00]
            outMsg.data = responsePayload
            bus1.send(outMsg)


def callback_onReceive_multiFrameWith4Wait(msg):
    print("Received Id: " + str(msg.arbitration_id))
    print("Data: " + str(msg.data))
    response = msg.data
    N_PCI = (response[0] & 0xF0) >> 4
    responsePayload = []
    outMsg = can.Message()
    outMsg.arbitration_id = 0x650
    if(N_PCI == 1):
        print("First frame received, responding CTS")
        responsePayload = [0x30, 5, 20, 00, 00, 00, 00, 00]
        outMsg.data = responsePayload
        bus1.send(outMsg)
    elif(N_PCI == 2):
        print("Consecutive frame received")
        if(
                (msg.data[7] == 40) |
                (msg.data[7] == 75) |
                (msg.data[7] == 145) |
                (msg.data[7] == 180)
        ):
            print("End of block, sending CTS")
            responsePayload = [0x30, 10, 127, 00, 00, 00, 00, 00]
            outMsg.data = responsePayload
            bus1.send(outMsg)
        elif( msg.data[7] == 110 ):
            print("End of block, producing a Wait")
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

if __name__ == "__main__":
    bus1 = can.interface.Bus('test', bustype="virtual")
    listener = can.Listener()
    notifier = can.Notifier(bus1, [listener], 0)

    uds = Uds.Uds(0x600, 0x650)
    udsMsg = UdsMessage.UdsMessage([0x22, 0xF1, 0x8C])

    # print("Test 1")
    # listener.on_message_received = callback_onReceive_singleFrame
    # uds.send(udsMsg)
    # print(udsMsg.response_raw)
    #
    # time.sleep(1)
    #
    # print("Test 2")
    # listener.on_message_received = callback_onReceive_multiFrameResponse_noBs
    # uds.send(udsMsg)
    # print(udsMsg.response_raw)
    #
    # time.sleep(1)

    # print("Test 3")
    # listener.on_message_received = callback_onReceive_multiFrameSend
    # payloadRequest = []
    # for i in range(0, 200):
    #     payloadRequest.append(i)
    # udsMsg.request = payloadRequest
    # udsMsg.responseRequired = False
    # uds.send(udsMsg)
    #
    # time.sleep(1)

    # print("Test 4")
    # listener.on_message_received = callback_onReceive_multiFrameWithWait
    # payloadRequest = []
    # for i in range(0, 200):
    #     payloadRequest.append(i)
    # udsMsg.request = payloadRequest
    # udsMsg.responseRequired = False
    # uds.send(udsMsg)

    print("Test 5")
    listener.on_message_received = callback_onReceive_multiFrameWith4Wait
    payloadRequest = []
    for i in range(0, 200):
        payloadRequest.append(i)
    udsMsg.request = payloadRequest
    udsMsg.responseRequired = False
    uds.send(udsMsg)