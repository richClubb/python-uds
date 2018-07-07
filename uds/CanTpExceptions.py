

##
#
class CanTpPayloadTooLargeForSfError(Exception):

    def __init__(self, message):
        self.message = message

##
#
class CanTpPayloadTooSmallForMfError(Exception):

    def __init__(self, message):
        self.message = message


##
# @brief exception for payload exceeding maximum payload size for a CAN Tp Message
class CanTpPayloadTooLarge(Exception):

    def __init__(self, message):
        self.message = message