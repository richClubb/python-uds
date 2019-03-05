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


class CanTpAddressingTypes(Enum):
    NORMAL = 0
    NORMAL_FIXED = 1
    EXTENDED = 2
    MIXED = 3


##
# defines the state of the send or receive method.
class CanTpState(Enum):
    IDLE = 0
    SEND_SINGLE_FRAME = 1
    SEND_FIRST_FRAME = 2
    SEND_CONSECUTIVE_FRAME = 3
    SEND_FLOW_CONTROL = 4
    WAIT_FLOW_CONTROL = 5
    WAIT_STMIN_TIMEOUT = 6
    WAIT_WAIT_TIMEOUT = 7
    RECEIVING_CONSECUTIVE_FRAME = 8


class CanTpMessageType(IntEnum):
    SINGLE_FRAME = 0
    FIRST_FRAME = 1
    CONSECUTIVE_FRAME = 2
    FLOW_CONTROL = 3


class CanTpFsTypes(IntEnum):
    CONTINUE_TO_SEND = 0x00
    WAIT = 0x01
    OVERFLOW = 0x02


class CanTpMTypes(Enum):
    DIAGNOSTICS = 0x01
    REMOTE_DIAGNOSTICS = 0x02


CANTP_MAX_PAYLOAD_LENGTH = 4095                    # hardcoded maximum based on the ISO 15765 standard
N_PCI_INDEX = 0
SINGLE_FRAME_DL_INDEX = 0
SINGLE_FRAME_DATA_START_INDEX = 1
FIRST_FRAME_DL_INDEX_HIGH = 0
FIRST_FRAME_DL_INDEX_LOW = 1
FIRST_FRAME_DATA_START_INDEX = 2
FC_BS_INDEX = 1
FC_STMIN_INDEX = 2
CONSECUTIVE_FRAME_SEQUENCE_NUMBER_INDEX = 0
CONSECUTIVE_FRAME_SEQUENCE_DATA_START_INDEX = 1
FLOW_CONTROL_BS_INDEX = 1
FLOW_CONTROL_STMIN_INDEX = 2
