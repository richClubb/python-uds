#!/usr/bin/env python

__author__ = "Richard Clubb"
__copyrights__ = "Copyright 2018, the python-uds project"
__credits__ = ["Richard Clubb"]

__license__ = "MIT"
__maintainer__ = "Richard Clubb"
__email__ = "richard.clubb@embeduk.com"
__status__ = "Development"


from enum import Enum, IntEnum


##
# possibly incomplete
class LinTpState(Enum):
    IDLE = 0
    SEND_SINGLE_FRAME = 1
    SEND_FIRST_FRAME = 2
    SEND_CONSECUTIVE_FRAME = 3
    RECEIVING_CONSECUTIVE_FRAME = 4


class LinTpMessageType(IntEnum):
    SINGLE_FRAME = 0
    FIRST_FRAME = 1
    CONSECUTIVE_FRAME = 2


# Needs checking!!!
LINTP_MAX_PAYLOAD_LENGTH = 4095
N_PCI_INDEX = 0
SINGLE_FRAME_DL_INDEX = 0
SINGLE_FRAME_DATA_START_INDEX = 1
FIRST_FRAME_DL_INDEX_HIGH = 0
FIRST_FRAME_DL_INDEX_LOW = 1
FIRST_FRAME_DATA_START_INDEX = 2
CONSECUTIVE_FRAME_SEQUENCE_NUMBER_INDEX = 0
CONSECUTIVE_FRAME_SEQUENCE_DATA_START_INDEX = 1