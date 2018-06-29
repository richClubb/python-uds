from UdsService import UdsService
from ISO14229 import DiagnostidId
from UdsMessage import UdsMessage

"""

"""
class ReadDataByIdentifier(UdsService):

    """

    """
    def __init__(self):
        super(ReadDataByIdentifier, self).__init__()
        self.__serviceId = 0x22

    """
    
    """
    def ecuSerialNumber(self):
        outputMsg = UdsMessage(servId=self.__serviceId)
        outputMsg.payload = [DiagnostidId.ecuSerialNumberDiagosticIdentifier]
        return outputMsg