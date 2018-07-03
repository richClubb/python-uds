#!/usr/bin/env python

__author__ = "Richard Clubb"
__copyrights__ = "Copyright 2018, the python-uds project"
__credits__ = ["Richard Clubb"]

__license__ = "MIT"
__maintainer__ = "Richard Clubb"
__email__ = "richard.clubb@embeduk.com"
__status__ = "Development"

from enum import IntEnum


##
# @brief needs filling in
class StandardPid(IntEnum):
    pidSupported_01_20 = 0x00
    monitorSupportedSinceDtcCleared = 0x01
    freezeDtc = 0x02
    fuelSystemStatus = 0x03
    calculatedEngineLoad = 0x04
    engineCoolantTemperature = 0x05
    shortTermFuelTrim_bank1 = 0x06
    longTermFuelTrim_bank1 = 0x07
    shortTermFuelTrim_bank2 = 0x08
    longTermFuelTrim_bank2 = 0x09
    fuelPressure = 0x0A
    intakeManifoldAbsolutePressure = 0x0B
    engineRpm = 0x0C
    vehicleSpeed = 0x0D
    timingAdvance = 0x0E
    intakeAirTemperature = 0x0F
    mafAirFlowRate = 0x10
    throttlePosition = 0x11
    commandedSecondaryAirStatus = 0x12
    oxygenSensorsPresentIn2Banks = 0x13
    oxygenSensor1 = 0x14
    oxygenSensor2 = 0x15
    oxygenSensor3 = 0x16
    oxygenSensor4 = 0x17
    oxygenSensor5 = 0x18
    oxygenSensor6 = 0x19
    oxygenSensor7 = 0x1A
    oxygenSensor8 = 0x1B
    obdStandard = 0x1C
    oxygenSensorsPresentIn4Banks = 0x1D
    auxiliaryInputStatus = 0x1E
    runTimeSinceEngineStart = 0x1F
    """ 
        0x21 - 0xC4
        Needs finishing added in the major section 
    """
    pidSupported_21_40 = 0x20
    pidSupported_41_60 = 0x40
    pidSupported_61_80 = 0x60
    pidSupported_81_A0 = 0x80
    pidSupported_A1_C0 = 0xA0
    pidSupported_C1_E0 = 0xC0
