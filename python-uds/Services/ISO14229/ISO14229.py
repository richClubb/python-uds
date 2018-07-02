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


class DiagnosticId(IntEnum):
    bootSoftwareIdentificationDataIdentifierDataIdentifier = 0xF180
    applicationSoftwareIdentificationDataIdentifier = 0xF181
    applicationDataIdentificationDataIdentifier = 0xF182
    bootSoftwareFingerprintDataIdentifier = 0xF183
    applicationSoftwareFingerprintDataIdentifier = 0xF184
    applicationDataFingerprintDataIdentifier = 0xF185
    activeSessionDiagnosticDataIdentifier = 0xF186
    vehicleManufacturerSparePartNumberDataIdentifier = 0xF187
    vehicleManufacturerEcuSoftwareNumberDataIdentifier = 0xF188
    vehicleManufacturerEcuSoftwareVersionNumberDataIdentifier = 0xF189
    ecuSerialNumberDiagnosticIdentifier = 0xF18C


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


#__all__ = ['DiagnosticId', 'NegativeResponseCodes']

if __name__ == "__main__":
    print(DiagnosticId.ecuSerialNumberDiagnosticIdentifier)
