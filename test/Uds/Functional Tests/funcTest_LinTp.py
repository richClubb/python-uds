from uds import LinTp
from time import sleep

if __name__ == "__main__":

    connection = LinTp(nodeAddress=0x0A)

    sleep(0.1)
    a = [0xb2, 0x01, 0xFF, 0x7F, 0xFF, 0x7F]
    try:

        connection.send(a)
        b = connection.recv(1)
        print(b)
    except:
        pass

    a = [0x22, 0xF1, 0x8C]
    try:

        connection.send(a)
        b = connection.recv(1)
        print(b)
    except:
        pass


    connection.closeConnection()
