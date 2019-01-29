#!/usr/bin/env python

__author__ = "Richard Clubb"
__copyrights__ = "Copyright 2019, the python-uds project"
__credits__ = ["Richard Clubb"]

__license__ = "MIT"
__maintainer__ = "Richard Clubb"
__email__ = "richard.clubb@embeduk.com"
__status__ = "Development"


from uds.uds_config_tool import DecodeFunctions
from uds.uds_config_tool.ISOStandard.ISOStandard import IsoDataFormatIdentifier
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
                hexFile.close()
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
                hexFile.close()
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
                if currentBlock is not None:
                    # IMPORTANT NOTE (possible TODO): Richard indicated that the last data line may need some tail end padding - if that's the case, we would know about it
                    # till here, so the need for such padidng would have to be detected here and added (e.g. check a "required" flag, and if true, run a moduls op on 
                    # block length to detect if padding needed, then add padding bytes, as above in continuousBlocking case).
                    self.__blocks.append(currentBlock)
                currentBlock = ihexData()  #... start the new block
                baseAddress = ((data[0]<< 8) + data[1]) << 16
                nextAddress = None


            elif recordType == ihexRecordType.EndOfFile: # ... add the final block to the block list
                eof_flag = True
                if currentBlock is not None:
                    self.__blocks.append(currentBlock)


            elif recordType == ihexRecordType.ExtendedSegmentAddress:
                hexFile.close()
                raise NotImplemented("Not implemented extended segment address")

            elif recordType == ihexRecordType.StartSegmentAddress:
                hexFile.close()
                raise NotImplemented("Start segment address not implemented")

            elif recordType == ihexRecordType.StartLinearAddress:
                hexFile.close()
                raise NotImplemented("Start linear address not implemented")
        hexFile.close()

    @property
    def dataLength(self):
        return sum([self.__blocks[i].dataLength for i in range(self.numBlocks)])

    @property
    def numBlocks(self):
        return len(self.__blocks)

    @property
    def blocks(self):
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


if __name__ == "__main__":

    app_blocks = ihexFile("../../test/Uds-Config-Tool/Functional Tests/e400_uds_test_app_e400.hex")
    #print(("found num blocks : ",  app_blocks.numBlocks))
    #print(("len block data[0] : ", app_blocks.block[0].dataLength))
    #print(("len block data[1] : ", app_blocks.block[1].dataLength))

    #smallerChunks = app_blocks.block[0].transmitChunks(sendChunksize=1280)  # ... breaking the data block to transmittable chunks
    #print(("found num small blocks : ", len(smallerChunks)))
    #smallerChunks = app_blocks.block[1].transmitChunks(sendChunksize=1280)  # ... breaking the data block to transmittable chunks
    #print(("found num small blocks : ", len(smallerChunks)))

    #transmitChunks = sum([app_blocks.block[i].transmitChunks(sendChunksize=1280) for i in range(app_blocks.numBlocks)],[])
    #print(("transmit total chunks : ", len(transmitChunks)))
	
    #print(("transmit start address (all) : ", app_blocks.transmitAddress))
    #print(("transmit start address (block 0) : ", app_blocks.block[0].transmitAddress))
    #print(("transmit start address (block 1) : ", app_blocks.block[1].transmitAddress))

    #transmitLength = sum([len(app_blocks.block[i].data) for i in range(app_blocks.numBlocks)])
    #print(("data length (total) : ",      app_blocks.dataLength))
    #print(("transmit length (total) : ",  app_blocks.transmitLength))
    #print(("transmit length (block 0): ", app_blocks.block[0].transmitLength))

    """ Examples - see also unittest_TransDataFunctions.py for ihex test cases ...
    app_blocks = ihexFile("../../test/Uds-Config-Tool/Functional Tests/TGT-ASSY-1383_v2.1.0_sbl.hex")
    e400 = createUdsConnection("Bootloader.odx", "Bootloader", reqId=0x600, resId=0x650, interface="peak")
    a = e400.requestDownload([IsoDataFormatIdentifier.noCompressionMethod], app_blocks.transmitAddress, app_blocks.transmitLength)
	....
	app_blocks.transmitChunksize = 1280
	a = e400.transferData(transferBlock=app_blocks.block[0])
	# ... or ...
	a = e400.transferData(transferBlocks=app_blocks)
    ....
    a = e400.transferExit()
    """
	
	


