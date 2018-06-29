from enum import IntEnum

class DiagnostidId(IntEnum):
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
    ecuSerialNumberDiagosticIdentifier = 0xF18C
