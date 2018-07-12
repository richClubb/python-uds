from Ecu import Ecu
from UdsMessage import UdsMessage
import can
import time


def callback_onReceive(msg):
    print(msg.data)
    if((msg.data[0] & 0xF0) == 0x10):
        y = can.Message(data=[0x30, 10, 10, 0, 0, 0, 0, 0], arbitration_id=0x650)
        bus.send(y)
    if(
            ((msg.data[7]) == 75)  |
            ((msg.data[7]) == 145) |
            ((msg.data[7]) == 215)
    ):
        y = can.Message(data=[0x30, 10, 10, 0, 0, 0, 0, 0], arbitration_id=0x650)
        time.sleep(0.05)
        bus.send(y)


if __name__ == "__main__":

    bus = can.interface.Bus('test', bustype="virtual")
    listener = can.Listener()
    listener.on_message_received = callback_onReceive
    notifier = can.Notifier(bus, [listener], 0)

    payload = []
    for i in range(0,255):
        payload.append(i)
    x = UdsMessage(payload)
    testEcu = Ecu(0x600, 0x650)
    testEcu.send(x)
    time.sleep(1)
