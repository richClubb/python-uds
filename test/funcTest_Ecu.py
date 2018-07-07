from Ecu import Ecu
from UdsMessage import UdsMessage
import can
import time

def callback_onReceive(mesg):
    print("Output")
    print(mesg.data)

if __name__ == "__main__":

    bus = can.interface.Bus('test', bustype="virtual")
    listener = can.Listener()
    listener.on_message_received = callback_onReceive
    notifier = can.Notifier(bus, [listener], 0)

    x = UdsMessage([1,2,3,4])

    testEcu = Ecu(0x600, 0x650)

    testEcu.send(x)

    time.sleep(2)

    y = can.Message([1,5,4,3,2])
    bus.send(y)

    time.sleep(2)