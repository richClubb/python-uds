#!/usr/bin/env python

__author__ = "Richard Clubb"
__copyrights__ = "Copyright 2018, the python-uds project"
__credits__ = ["Richard Clubb"]

__license__ = "MIT"
__maintainer__ = "Richard Clubb"
__email__ = "richard.clubb@embeduk.com"
__status__ = "Development"

__all__ = ['DiagnosticId', 'NegativeResponseCodes']

from enum import IntEnum


##
# @brief A enumeration class to document the necessary DIDs
class DiagnosticId(IntEnum):
    bootSoftwareIdentificationDataIdentifierDataIdentifier = 0xF180  ## @enum Test
    applicationSoftwareIdentificationDataIdentifier = 0xF181
    applicationDataIdentificationDataIdentifier = 0xF182
    bootSoftwareFingerprintDataIdentifier = 0xF183
    applicationSoftwareFingerprintDataIdentifier = 0xF184
    applicationDataFingerprintDataIdentifier = 0xF185
    activeSessionDiagnosticDataIdentifier = 0xF186
    vehicleManufacturerSparePartNumberDataIdentifier = 0xF187
    vehicleManufacturerEcuSoftwareNumberDataIdentifier = 0xF188
    vehicleManufacturerEcuSoftwareVersionNumberDataIdentifier = 0xF189
    systemSupplierIdentifierDataIdentifier = 0xF18A
    ecuManufacturingDateDataIdentifier = 0xF18B
    ecuSerialNumberDiagnosticIdentifier = 0xF18C
    supportedFunctionalUnitsDataIdentifier = 0xF18D
    vehicleManufacturerKitAssemblyPartNumberDataIdentifier = 0xF18E
    """
    0xF18F - ISOSAEReservedStandardized
    """
    vinDataIdentifier = 0xF190
    vehicleManufacturerEcuHardwareNumberDataIdentifier = 0xF191
    systemSupplierEcuHardwareNumberDataIdentifier = 0xF192
    systemSupplierEcuHardwareVersionNumberDataIdentifier = 0xF193
    systemSupplierEcuSoftwareNumberDataIdentifier = 0xF194
    systemSupplierEcuSoftwareVersionNumberDataIdentifier = 0xF195
    exhaustRegulationOrTypeApprovalNumberDataIdentifier = 0xF196
    systemNameOrEngineTypeDataIdentifier = 0xF197
    repairShopCodeOrTesterSerialNumberDataIdentifier = 0xF198
    programmingDataDataIdentifier = 0xF199
    calibrationRepairShopCodeOrCalibrationEquipmentSerialNumberDataIdentifier = 0xF19A
    calibrationDateDataIdentifier = 0xF19B
    calibrationEquipmentSoftwareNumberDataIdentifier = 0xF19C
    ecuInstallationDateDataIdentifier = 0xF19D
    odxFileDataIdentifier = 0xF19E
    entityDataIdentifier = 0xF19F
    """
    0xF1A0 - 0xF1EF - Identification option vehicle manufacturer specific
    ## more remaining   
    """
    numberOfEdrDevices = 0xFA10
    edrIdentification = 0xFA11
    edrDeviceAddressInformation = 0xFA12
    """
    more remaining
    """
    udsVersionDataIdentifier = 0xFF00




##
# @enum definition of the negative response codes
# @brief a class to document all the standard negative response codes
class NegativeResponseCodes(IntEnum):
    positiveResponse = 0x00
    """
    0x01 - 0x0F - ISOSAEReserved
    """
    generalReject = 0x10
    serviceNotSupported = 0x11
    subFunctionNotSupported = 0x12
    incorrectMessageLengthOrInvalidFormat = 0x13
    responseTooLong = 0x14
    """
    0x15 - 0x20 - ISOSAEReserved
    """
    busyRepeatRequest = 0x21
    conditionsNotCorrect = 0x22
    """
    0x23 - ISOSAEReserved
    """
    requestSequenceError = 0x24
    noResponseFromSubnetComponent = 0x25
    failurePreventsExecutionOfRequestedAction = 0x26
    """
    0x27 - 0x30 - ISOSAEReserved
    """
    requestOutOfRange = 0x31
    """
    0x32 - ISOSAEReserved
    """
    securityAccessDenied = 0x33
    """
    0x34 - ISOSAEReserved
    """
    invalidKey = 0x35
    exceedNumberOfAttempts = 0x36
    requiredTimeDelayNotExpired = 0x37
    """
    0x38 - 0x4F - reservedByExtendedDataLinkSecurityDocument
    0x50 - 0x6F - ISOSAEReserved
    """
    uploadDownloadNotAccepted = 0x70
    transferDataSuspended = 0x71
    generalProgrammingFailure = 0x72
    wrongBlockSequenceCounter = 0x73
    """
    0x74 - 0x77 - ISOSAEReserved
    """
    requestCorrectlyReceivedResponsePending = 0x78
    """
    0x79 - 0x7D - ISOSAEReserved
    """
    subFunctionNotSupportedInActiveSession = 0x7E
    serviceNotSupportedInActiveSession = 0x7F
    """
    0x80 - ISOSAEReserved
    """
    rpmTooHigh = 0x81
    rpmTooLow = 0x82
    engineIsRunning = 0x83
    engineNotRunning = 0x84
    engineRunTimeTooLow = 0x85
    temperatureTooHigh = 0x86
    temperatureTooLow = 0x87
    vehicleSpeedTooHigh = 0x88
    vehicleSpeedTooLow = 0x89
    throttlePedalTooHigh = 0x8A
    throttlePedalTooLow = 0x8B
    transmissionRangeNotInNeutral = 0x8C
    transmissionRangeNotInGear = 0x8D
    """
    0x8E - ISOSAEReserved
    """
    brakeSwitchNotClosed = 0x8F
    shifterLeverNotInPark = 0x90
    torqueConverterClutchLocked = 0x91
    voltageTooHigh = 0x92
    voltageTooLow = 0x93
    """
    0x94 - 0xEF - reserved for specific conditions not correct
    0xF0 - 0xFE - vehicleManufacturerSpecificConditionsNotCorrect
    """


if __name__ == "__main__":
    print(DiagnosticId.ecuSerialNumberDiagnosticIdentifier)
