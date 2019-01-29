from uds import createUdsConnection
from struct import pack, unpack
import hashlib
from time import sleep, time


class ihexData(object):

    def __init__(self):

        self.__startAddress = 0
        self.__size = 0
        self.__data = []

    @property
    def startAddress(self):
        return self.__startAddress

    @startAddress.setter
    def startAddress(self, value):
        self.__startAddress = value

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, value):
        self.__data = value

    def addData(self, value):
        self.__data += value

    def getDataFromAddress(self, address, size):
        raise NotImplemented("getDataFromAddress Not yet implemented")


class ihexFile(object):

    def __init__(self, filename=None, padding=0xFF, continuousBlocking=True):

        hexFile = open(filename, 'r')

        self.__blocks = []

        eof_flag = False
        linecount = 1

        currentAddress = None
        nextAddress = None

        currentBlock = None
        baseAddress = 0

        while not eof_flag:

            line = hexFile.readline()

            if line[0] != ":":
                raise Exception("Unexpected line on line {0}".format(linecount))

            lineArray = bytes.fromhex(line[1:])

            # get the main data
            index = 0
            dataLength = lineArray[index]
            index += 1
            address = (lineArray[index] << 8) | (lineArray[index+1])
            index += 2
            recordType = lineArray[index]
            index += 1
            data = lineArray[index: index+dataLength]
            index += dataLength
            checksum = lineArray[index]

            calculatedChecksum = 0

            for i in range(len(lineArray)-1):
                calculatedChecksum = (calculatedChecksum + lineArray[i]) % 256

            calculatedChecksum = ( ~calculatedChecksum + 1 ) %256

            if calculatedChecksum != checksum:
                raise Exception("Checksum on line {0} does not match. Actual: {1}, Calculated: {2}".format(linecount,
                                                                                                           checksum,
                                                                                                           calculatedChecksum))

            # print("Length: {0:#x}, Address: {1:#x}, recordType: {2:#x}, data: {3}, checksum: {4:#x}, calculatedChecksum: {5:#x}".format(dataLength,
            #                                                                                                                             address,
            #                                                                                                                             recordType,
            #                                                                                                                             data,
            #                                                                                                                             checksum,
            #                                                                                                                             calculatedChecksum))



            if recordType == 0x00:
                if currentAddress is None:
                    currentBlock.startAddress = baseAddress + address

                if nextAddress is not None:
                    if address != nextAddress:
                        if continuousBlocking:
                            paddingBlock = []
                            [paddingBlock.append(padding) for i in range(0, address-nextAddress)]
                            currentBlock.addData(paddingBlock)
                        else:
                            # print("new block")
                            pass
                currentBlock.addData(data)
                currentAddress = address
                nextAddress = address + dataLength



            elif recordType == 0x01:
                eof_flag = True
                if currentBlock is not None:
                    self.__blocks.append(currentBlock)
            elif recordType == 0x02:
                raise NotImplemented("Not implemented extended segment address")
            elif recordType == 0x03:
                raise NotImplemented("Start segment address not implemented")
            elif recordType == 0x04:
                # print("New block")
                if currentBlock is None:
                    currentBlock = ihexData()
                    baseAddress = (address << 16)
                else:
                    self.__blocks.append(currentBlock)

            elif recordType == 0x05:
                raise NotImplemented("Start linear address not implemented")

            linecount += 1

            pass

    def getBlocks(self):
        return self.__blocks


def calculateKeyFromSeed(seed, ecuKey):

    deviceSecret = [0x46, 0x45, 0x44, 0x43, 0x42, 0x41, 0x39, 0x38, 0x37, 0x36, 0x35, 0x34, 0x33, 0x32, 0x31, 0x30]

    md5Input = deviceSecret + seed + deviceSecret
    c = pack('%sB' % len(md5Input), *md5Input)
    d = hashlib.md5(c).digest()
    dUnpack = unpack('%sB' % 16, d)
    sendList = [val for val in dUnpack]

    return sendList


if __name__ == "__main__":

    #secondaryBootloaderContainer = chunkIhexFile("TGT-ASSY-1383_v2.1.0_sbl.hex")
    #print(secondaryBootloaderContainer)
    secondaryBootloader = ihexFile("TGT-ASSY-1383_v2.1.0_sbl.hex")
    blocks = secondaryBootloader.getBlocks()
    blockData = blocks[0].data
    smallerChunks = []
    chunk = []
    count = 0
    for i in range(0, len(blockData)):
        chunk.append(blockData[i])
        count += 1
        if count == 1280:
            smallerChunks.append(chunk)
            chunk = []
            count = 0

    if len(chunk) != 0:
        smallerChunks.append(chunk)

    e400 = createUdsConnection("Bootloader.odx", "Bootloader", reqId=0x600, resId=0x650, interface="peak")

    a = e400.readDataByIdentifier("ECU Serial Number")
    print("Serial Number: {0}".format(a["ECU Serial Number"]))

    a = e400.readDataByIdentifier("PBL Part Number")
    print("PBL Part Number: {0}".format(a["PBL Part Number"]))

    a = e400.readDataByIdentifier("PBL Version Number")
    print("PBL Version Number: {0}".format(a["PBL Version Number"]))

    a = e400.diagnosticSessionControl("Programming Session")
    print("In Programming Session")

    a = e400.securityAccess("Programming Request")
    print("Security Key: {0}".format(a))

    b = calculateKeyFromSeed(a, [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
    print("Calculated Key: {0}".format(b))

    a = e400.securityAccess("Programming Key", b)
    print("Security Access Granted")

    print("Setting up transfer of Secondary Bootloader")
    a = e400.requestDownload([0], [0x40, 0x03, 0xe0, 0x00], [0x00, 0x00, 0x0e, 0x56])
    #print(a)

    print("Transferring Secondary Bootloader")
    for i in range(len(smallerChunks)):
        a = e400.transferData(i+1, smallerChunks[i])

    print("Finished Transfer")
    a = e400.transferExit()

    print("Jumping to Secondary Bootloader")
    a = e400.routineControl("Start Secondary Bootloader", 1, [0x4003e000])
    #print(a)

    print("Erasing Memory")
    a = e400.routineControl("Erase Memory", 1, [("memoryAddress",[0x00080000]), ("memorySize",[0x000162e4])])
    #print(a)

    working = True
    while working:

        a = e400.routineControl("Erase Memory", 3)
        #print(a)
        if(a['Erase Memory Status']) == [0x30]:
            print("Erased memory")
            working = False
        elif(a['Erase Memory Status'] == [0x31]):
            print("ABORTED")
            raise Exception("Erase memory unsuccessful")
        sleep(0.001)

    application = ihexFile("e400_uds_test_app_e400.ihex")
    blocks = application.getBlocks()
    blockData = blocks[0].data
    smallerChunks = []
    chunk = []
    count = 0
    for i in range(0, len(blockData)):
        chunk.append(blockData[i])
        count += 1
        if count == 1280:
            smallerChunks.append(chunk)
            chunk = []
            count = 0

    if len(chunk) != 0:
        smallerChunks.append(chunk)

    print("Setting up transfer for Application")
    a = e400.requestDownload([0], [0x00, 0x08, 0x00, 0x00], [0x00, 0x01, 0x62, 0xe4])

    print("Transferring Application")
    for i in range(0, len(smallerChunks)):

        a = e400.transferData(i+1, smallerChunks[i])

    print("Transfer Exit")
    a = e400.transferExit()

    a = e400.routineControl("Check Valid Application", 0x01)

    working = True
    while working:
        # a = e400.send([0x31, 0x03, 0x03, 0x04])
        # print(a)
        # if a[4] == 0x30:
        #     working = False
        #     print("Success")
        # elif a[4] == 0x31:
        #     working = False
        #     print("Aborted")
        a = e400.routineControl("Check Valid Application", 0x03)

        routineStatus = a["Valid Application Status"][0]
        applicationPresent = a["Valid Application Present"][0]

        if routineStatus == 0x30:
            working = False
            print("Routine Finished")

            if applicationPresent == 0x01:
                print("Application Invalid")
            elif applicationPresent == 0x02:
                print("Application Valid")
        elif routineStatus == 0x31:
            working = False
            print("Aborted")
        elif routineStatus == 0x32:
            #print("Working")
            pass

        sleep(0.01)


    e400.ecuReset("Hard Reset", suppressResponse=True)



