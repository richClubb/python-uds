#!/usr/bin/env python

__author__ = "Richard Clubb"
__copyrights__ = "Copyright 2019, the python-uds project"
__credits__ = ["Richard Clubb"]

__license__ = "MIT"
__maintainer__ = "Richard Clubb"
__email__ = "richard.clubb@embeduk.com"
__status__ = "Development"


from uds import createUdsConnection
from uds.uds_config_tool import DecodeFunctions
from struct import pack, unpack
from time import sleep, time
from enum import IntEnum
import hashlib
import os


class ihexRecordType(IntEnum):

    Data = 0x00
    EndOfFile = 0x01
    ExtendedSegmentAddress = 0x02
    StartSegmentAddress = 0x03
    ExtendedLinearAddress = 0x04
    StartLinearAddress = 0x05


class ihexData(object):

    def __init__(self):

        self.__startAddress = 0
        self.__size = 0
        self.__data = []
        self.__sendChunksize = None
        self.__sendChunks = None

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

    @property
    def dataLength(self):
        return len(self.__data)

    @property
    def transmitChunksize(self):
        return self.__sendChunksize

    @startAddress.setter
    def transmitChunksize(self, value):
        # TODO: need to check permitted ranges if any!!!
        if self.__sendChunksize != value:
            self.__sendChunks = None  # ... send chunks needs re-calculating if required, so force this by setting to null here.
        self.__sendChunksize = value

    def transmitChunks(self, sendChunksize=None):  # ... initialising or re-setting of the chunk size is allowed here for convenience.
        if sendChunksize is not None:
            self.transmitChunksize = sendChunksize
        if self.__sendChunksize is not None and self.__data != []:
            self.__sendChunks = []
            chunk = []
            count = 0
            for i in range(0, len(self.__data)):
                chunk.append(self.__data[i])
                count += 1
                if count == self.__sendChunksize:
                    self.__sendChunks.append(chunk)
                    chunk = []
                    count = 0
            if len(chunk) != 0:
                self.__sendChunks.append(chunk)
        if self.__sendChunks is None:
            return []		
        return self.__sendChunks

    @property
    def transmitLength(self):  # ... this is dataLength encoded
        return DecodeFunctions.intArrayToIntArray([self.dataLength], 'int32', 'int8')  # ... length calc'd as [0x00, 0x01, 0x4F, 0xe4] as expected

    def addData(self, value):
        self.__data += value
        self.__sendChunks = None

    def getDataFromAddress(self, address, size):
        raise NotImplemented("getDataFromAddress Not yet implemented")

    @property
    def transmitAddress(self):
        return DecodeFunctions.intArrayToIntArray([self.__startAddress], 'int32', 'int8')


class ihexFile(object):

    def __init__(self, filename=None, padding=0xFF, continuousBlocking=True):

        hexFile = open(filename, 'r')

        self.__blocks = []

        eof_flag = False
        linecount = 1

        nextAddress = None

        currentBlock = None
        baseAddress = 0

        self.__sendChunksize = None

        while not eof_flag:
            line = hexFile.readline()
            linecount += 1

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

            if recordType == ihexRecordType.Data:   # ... We match data first as it's the most common record type, so more efficient
                if nextAddress is None:
                    print(("address components",baseAddress,address))
                    currentBlock.startAddress = baseAddress + address

                # As each line of data is individually addressed, there may be disconuities present in the data. 
                # If so (i.e. a gap in the addressing), and a continuous record is required, then pad the data.
                # NOTE: by default, padding is expected.
                if nextAddress is not None:
                    if address != nextAddress:
                        if continuousBlocking:
                            paddingBlock = []
                            [paddingBlock.append(padding) for i in range(0, address-nextAddress)]
                            currentBlock.addData(paddingBlock)

                currentBlock.addData(data)
                nextAddress = address + dataLength


            elif recordType == ihexRecordType.ExtendedLinearAddress:   # ... new block - append any existing block to the blocklist or initialise the current block record
                print(("DEBUG - Extended Linear Address (new block) - ",linecount))

                if currentBlock is not None:
                    # IMPORTANT NOTE (possible TODO): Richard indicated that the last data line may need some tail end padding - if that's the case, we would know about it
                    # till here, so the need for such padidng would have to be detected here and added (e.g. check a "required" flag, and if true, run a moduls op on 
                    # block length to detect if padding needed, then add padding bytes, as above in continuousBlocking case).
                    self.__blocks.append(currentBlock)
                currentBlock = ihexData()  #... start the new block
                print(("DEBUG - --- - ",data))
                baseAddress = ((data[0]<< 8) + data[1]) << 16
                #baseAddress = (address << 16)
                nextAddress = None


            elif recordType == ihexRecordType.EndOfFile: # ... add the final block to the block list
                eof_flag = True
                if currentBlock is not None:
                    self.__blocks.append(currentBlock)


            elif recordType == ihexRecordType.ExtendedSegmentAddress:
                raise NotImplemented("Not implemented extended segment address")

            elif recordType == ihexRecordType.StartSegmentAddress:
                raise NotImplemented("Start segment address not implemented")

            elif recordType == ihexRecordType.StartLinearAddress:
                raise NotImplemented("Start linear address not implemented")

    @property
    def dataLength(self):
        return sum([self.__blocks[i].dataLength for i in range(self.numBlocks)])

    @property
    def numBlocks(self):
        return len(self.__blocks)

    @property
    def block(self):
        return self.__blocks


    @property
    def transmitChunksize(self):
        return self.__sendChunksize

    @transmitChunksize.setter
    def transmitChunksize(self, value):
        # TODO: need to check permitted ranges if any!!!
        self.__sendChunksize = value
        for block in self.__blocks:
            block.transmitChunksize = value

    def transmitChunks(self, sendChunksize=None):  # ... initialising or re-setting of the chunk size is allowed here for convenience.
        if sendChunksize is not None:
            self.transmitChunksize = sendChunksize		
        return sum([self.__blocks[i].transmitChunks() for i in range(self.numBlocks)],[])

    @property
    def transmitLength(self):  # ... this is dataLength encoded
        return DecodeFunctions.intArrayToIntArray([self.dataLength], 'int32', 'int8')

    @property
    def transmitAddress(self):
        return self.__blocks[0].transmitAddress


"""
def calculateKeyFromSeed(seed, ecuKey):

    deviceSecret = [0x46, 0x45, 0x44, 0x43, 0x42, 0x41, 0x39, 0x38, 0x37, 0x36, 0x35, 0x34, 0x33, 0x32, 0x31, 0x30]

    md5Input = deviceSecret + seed + deviceSecret
    c = pack('%sB' % len(md5Input), *md5Input)
    d = hashlib.md5(c).digest()
    dUnpack = unpack('%sB' % 16, d)
    sendList = [val for val in dUnpack]

    return sendList
"""

if __name__ == "__main__":

    # ????????????? needs to know about the ecu's chunk size - e.g. 1280 for E400
    app_blocks = ihexFile("../../test/Uds-Config-Tool/Functional Tests/e400_uds_test_app_e400.hex")
    print("")
    print(("found num blocks : ",app_blocks.numBlocks))
    print(("len block data[0] : ",app_blocks.block[0].dataLength))
    print(("len block data[1] : ",app_blocks.block[1].dataLength))

    # TODO: The transmission  chunk size here needs to be against the connection instance, and not against the block !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    smallerChunks = app_blocks.block[0].transmitChunks(sendChunksize=1280)  # ... breaking the data block to transmittable chunks
    print(("found num small blocks : ",len(smallerChunks)))
    smallerChunks = app_blocks.block[1].transmitChunks(sendChunksize=1280)  # ... breaking the data block to transmittable chunks
    print(("found num small blocks : ",len(smallerChunks)))

    # TODO: Do we transmit per block, or all block together? If the latter, then we need something more like ...  !!!!!!!!!!!!!!!!!!
    transmitChunks = sum([app_blocks.block[i].transmitChunks(sendChunksize=1280) for i in range(app_blocks.numBlocks)],[])
    print(("transmit total chunks : ",len(transmitChunks)))
	
    print(("transmit start address (all) : ",app_blocks.transmitAddress))

    print(("transmit start address (block 0) : ",app_blocks.block[0].transmitAddress))
    print(("transmit start address (block 1) : ",app_blocks.block[1].transmitAddress))
    #a = e400.requestDownload([0], app_blocks[0].startAddressAsIntArray(), [0x00, 0x01, 0x4F, 0xe4])  # ... start address calc'd as [0x00, 0x08, 0x00, 0x00] as expected
    #a = e400.requestDownload([0], [0x00, 0x08, 0x00, 0x00], [0x00, 0x01, 0x4F, 0xe4])
    # need to match [0x00, 0x01, 0x4F, 0xe4] for memory size
    #transmitLength = sum([len(app_blocks.block[i].data) for i in range(app_blocks.numBlocks)])
    print(("data length (total) : ",app_blocks.dataLength))
    print(("transmit length (total) : ",app_blocks.transmitLength))  # ... length calc'd as [0x00, 0x01, 0x4F, 0xe4] as expected

    print(("transmit length (block 0): ",app_blocks.block[0].transmitLength))  # ... length calc'd as [0x00, 0x01, 0x4F, 0xe4] as expected

    """
    app_blocks = ihexFile("../../test/Uds-Config-Tool/Functional Tests/TGT-ASSY-1383_v2.1.0_sbl.hex")
    a = e400.requestDownload([IsoDataFormatIdentifier.noCompressionMethod], app_blocks.transmitAddress, app_blocks.transmitLength)
    transmitChunks = app_blocks.transmitChunks(sendChunksize=1280)
    e400 = createUdsConnection("Bootloader.odx", "Bootloader", reqId=0x600, resId=0x650, interface="peak")
	....
    for i in range(len(transmitChunks)):
        a = e400.transferData(i+1, transmitChunks[i])
    ....
    a = e400.transferExit()
    """
	
	
    """
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

    startTime = time()
    in_bootloader_flag = 0
    while in_bootloader_flag == 0:
        try:
            if (time() - startTime) > 5:
                in_bootloader_flag = 1
                print("Timeout")
            a = e400.diagnosticSessionControl("Programming Session")
            in_bootloader_flag = 1
        except:
            pass

    sleep(2)

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
    a = e400.routineControl("Erase Memory", 1, [("memoryAddress",[0x00080000]), ("memorySize",[0x000088AD])])
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
    a = e400.requestDownload([0], [0x00, 0x08, 0x00, 0x00], [0x00, 0x01, 0x4F, 0xe4])

    print("Transferring Application")
    for i in range(0, 68):

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
    """

