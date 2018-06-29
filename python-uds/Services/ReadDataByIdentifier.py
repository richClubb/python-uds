from UdsService import UdsService
from ISO14229 import DiagnostidId
from UdsMessage import UdsMessage

class ReadDataByIdentifier(UdsService):

    def __init__(self):
        super(ReadDataByIdentifier, self).__init__()

    def ecuSerialNumber(self):
        outputMsg = UdsMessage()
        outputMsg.
