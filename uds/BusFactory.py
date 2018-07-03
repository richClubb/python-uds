#!/usr/bin/env python

__author__ = "Richard Clubb"
__copyrights__ = "Copyright 2018, the python-uds project"
__credits__ = ["Richard Clubb"]

__license__ = "MIT"
__maintainer__ = "Richard Clubb"
__email__ = "richard.clubb@embeduk.com"
__status__ = "Development"

import can


##
# @brief factory class to create the instances of the bus objects
class BusFactory(object):

    def createBus(hwIf=None, baudRate=None):
        if(hwIf == 'PEAK_CAN_USB'):
            return can.interfaces.pcan.PcanBus(channel='PCAN_USBBUS1',
                                               bitrate=500)
        elif(hwIf == 'VECTOR'):
            return can.interfaces.vector.VectorBus()

        else:
            raise NotImplementedError("hwIf not known")
