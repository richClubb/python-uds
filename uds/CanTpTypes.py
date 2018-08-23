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


class CanTpState(Enum):
    IDLE = 0
    RECEIVING_SINGLE_FRAME = 1
    RECEIVING_FIRST_FRAME = 2
    RECEIVING_CONSECUTIVE_FRAME = 3
    SENDING_FC_CTS = 4
    FINISHED = 5


class CanTpMessageState(Enum):
    END_OF_MESSAGE = 0
    END_OF_BLOCK = 1
    SINGLE_FRAME = 2
    FIRST_FRAME = 3
    CONSECUTIVE_FRAME = 4
    INIT = 5


class CanTpMessageType(IntEnum):
    SINGLE_FRAME = 0
    FIRST_FRAME = 1
    CONSECUTIVE_FRAME = 2
    FLOW_CONTROL = 3


class CanTpFsType(IntEnum):
    CONTINUE_TO_SEND = 0
    WAIT = 1
    OVERFLOW = 2

##
# @brief exception for the consecutive frame out of sequence