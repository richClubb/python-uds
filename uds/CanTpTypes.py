#!/usr/bin/env python

__author__ = "Richard Clubb"
__copyrights__ = "Copyright 2018, the python-uds project"
__credits__ = ["Richard Clubb"]

__license__ = "MIT"
__maintainer__ = "Richard Clubb"
__email__ = "richard.clubb@embeduk.com"
__status__ = "Development"


from enum import Enum, IntEnum


class N_Result(Enum):
    N_OK = 0
    N_TIMEOUT_A = 1
    N_TIMEOUT_Bs = 2
    N_TIMEOUT_Cr = 3
    N_WRONG_SN = 4
    N_INVALID_FS = 5
    N_UNEXP_PDU = 6
    N_WFT_OVFLW = 7
    N_ERROR = 8


##
#
class CanTpMessageType(IntEnum):
    SINGLE_FRAME = 0
    FIRST_FRAME = 1
    CONSECUTIVE_FRAME = 2
    FLOW_CONTROL = 3
    MULTI_FRAME = 4


##
#
class CanTpFsType(IntEnum):
    CTS = 0
    WAIT = 1
    OVERFLOW = 2


class CanTpMessageState(IntEnum):
    FINISHED = 0
    WAITING_FC_CTS = 1
    WAITING_CF = 2
    SENDING_FC_CTS = 3
    IDLE = 4
    RECEIVING_CF = 5
    SENDING_SF = 6
    SENDING_FF = 7
    SENDING_CF = 8

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


##
# @brief exception for timeout waiting for FC
class CanTpTimeoutWaitingForFlowControl(Exception):
    def __init__(self, message):
        self.message = message


##
# @brief exception for the consecutive frame out of sequence