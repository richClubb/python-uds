from uds import Uds
from can import Bus, Listener, Notifier
from time import sleep

def callback_onReceive(msg):

    if(msg.arbitration_id == 0x600):
        print("Bootloader Receive:", list(msg.data))
    if(msg.arbitration_id == 0x7E0):
        print("PCM Receive:", list(msg.data))


if __name__ == "__main__":

    recvBus = Bus("virtualInterface", bustype="virtual")

    listener = Listener()
    notifier = Notifier(recvBus, [listener], 0)

    listener.on_message_received = callback_onReceive

    a = Uds()

    a.send([0x22, 0xf1, 0x8C], responseRequired=False)

    sleep(2)

