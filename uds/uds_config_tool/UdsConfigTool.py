#!/usr/bin/env python

__author__ = "Richard Clubb"
__copyrights__ = "Copyright 2018, the python-uds project"
__credits__ = ["Richard Clubb"]

__license__ = "MIT"
__maintainer__ = "Richard Clubb"
__email__ = "richard.clubb@embeduk.com"
__status__ = "Development"


import xml.etree.ElementTree as ET

from uds.uds_config_tool.UtilityFunctions import isDiagServiceTransmissionOnly
from uds.uds_communications.Uds.Uds import Uds
from uds.uds_config_tool.SupportedServices.DiagnosticSessionControlContainer import DiagnosticSessionControlContainer
from uds.uds_config_tool.FunctionCreation.DiagnosticSessionControlMethodFactory import DiagnosticSessionControlMethodFactory
from uds.uds_config_tool.SupportedServices.ECUResetContainer import ECUResetContainer
from uds.uds_config_tool.FunctionCreation.ECUResetMethodFactory import ECUResetMethodFactory
from uds.uds_config_tool.SupportedServices.ReadDataByIdentifierContainer import ReadDataByIdentifierContainer
from uds.uds_config_tool.FunctionCreation.ReadDataByIdentifierMethodFactory import ReadDataByIdentifierMethodFactory
from uds.uds_config_tool.SupportedServices.WriteDataByIdentifierContainer import WriteDataByIdentifierContainer
from uds.uds_config_tool.FunctionCreation.WriteDataByIdentifierMethodFactory import WriteDataByIdentifierMethodFactory
from uds.uds_config_tool.SupportedServices.ClearDTCContainer import ClearDTCContainer
from uds.uds_config_tool.FunctionCreation.ClearDTCMethodFactory import ClearDTCMethodFactory
from uds.uds_config_tool.SupportedServices.ReadDTCContainer import ReadDTCContainer
from uds.uds_config_tool.FunctionCreation.ReadDTCMethodFactory import ReadDTCMethodFactory
from uds.uds_config_tool.SupportedServices.InputOutputControlContainer import InputOutputControlContainer
from uds.uds_config_tool.FunctionCreation.InputOutputControlMethodFactory import InputOutputControlMethodFactory
from uds.uds_config_tool.SupportedServices.RoutineControlContainer import RoutineControlContainer
from uds.uds_config_tool.FunctionCreation.RoutineControlMethodFactory import RoutineControlMethodFactory
from uds.uds_config_tool.SupportedServices.RequestDownloadContainer import RequestDownloadContainer
from uds.uds_config_tool.FunctionCreation.RequestDownloadMethodFactory import RequestDownloadMethodFactory

from uds.uds_config_tool.SupportedServices.SecurityAccessContainer import SecurityAccessContainer
from uds.uds_config_tool.FunctionCreation.SecurityAccessMethodFactory import SecurityAccessMethodFactory
from uds.uds_config_tool.SupportedServices.RequestUploadContainer import RequestUploadContainer
from uds.uds_config_tool.FunctionCreation.RequestUploadMethodFactory import RequestUploadMethodFactory
from uds.uds_config_tool.SupportedServices.TransferDataContainer import TransferDataContainer
from uds.uds_config_tool.FunctionCreation.TransferDataMethodFactory import TransferDataMethodFactory
from uds.uds_config_tool.SupportedServices.TransferExitContainer import TransferExitContainer
from uds.uds_config_tool.FunctionCreation.TransferExitMethodFactory import TransferExitMethodFactory
from uds.uds_config_tool.SupportedServices.TesterPresentContainer import TesterPresentContainer
from uds.uds_config_tool.FunctionCreation.TesterPresentMethodFactory import TesterPresentMethodFactory
from uds.uds_config_tool.ISOStandard.ISOStandard import IsoServices, IsoRoutineControlType, IsoInputOutputControlOptionRecord, IsoReadDTCSubfunction, IsoReadDTCStatusMask as Mask

from uds.uds_config_tool.ISOStandard.ISOStandard import IsoServices

def get_serviceIdFromXmlElement(diagServiceElement, xmlElements):

    requestKey = diagServiceElement.find('REQUEST-REF').attrib['ID-REF']
    requestElement = xmlElements[requestKey]
    params = requestElement.find('PARAMS')
    for i in params:
        try:
            if(i.attrib['SEMANTIC'] == 'SERVICE-ID'):
                return int(i.find('CODED-VALUE').text)
        except:
            pass

    return None


def fill_dictionary(xmlElement):
    temp_dictionary = {}
    for i in xmlElement:
        temp_dictionary[i.attrib['ID']] = i

    return temp_dictionary


def createUdsConnection(xmlFile, ecuName, ihexFile=None, **kwargs):

    root = ET.parse(xmlFile)

    # create any supported containers
    diagnosticSessionControlContainer = DiagnosticSessionControlContainer()
    ecuResetContainer = ECUResetContainer()
    rdbiContainer = ReadDataByIdentifierContainer()
    wdbiContainer = WriteDataByIdentifierContainer()
    clearDTCContainer = ClearDTCContainer()
    readDTCContainer = ReadDTCContainer()
    inputOutputControlContainer = InputOutputControlContainer()
    routineControlContainer = RoutineControlContainer()
    requestDownloadContainer = RequestDownloadContainer()
    securityAccessContainer = SecurityAccessContainer()
    requestUploadContainer = RequestUploadContainer()
    transferDataContainer = TransferDataContainer()
    transferExitContainer = TransferExitContainer()
    testerPresentContainer = TesterPresentContainer()
    sessionService_flag = False
    ecuResetService_flag = False
    rdbiService_flag = False
    wdbiService_flag = False
    securityAccess_flag = False
    clearDTCService_flag = False
    readDTCService_flag = False
    ioCtrlService_flag = False
    routineCtrlService_flag = False
    reqDownloadService_flag = False
    reqUploadService_flag = False
    transDataService_flag = False
    transExitService_flag = False
    testerPresentService_flag = False
    xmlElements = {}

    for child in root.iter():
        currTag = child.tag
        try:
            xmlElements[child.attrib['ID']] = child
        except KeyError:
            pass

    for key, value in xmlElements.items():
        if value.tag == 'DIAG-SERVICE':
            serviceId = get_serviceIdFromXmlElement(value, xmlElements)
            sdg = value.find('SDGS').find('SDG')
            humanName = ""
            for sd in sdg:
                try:
                    if sd.attrib['SI'] == 'DiagInstanceName':
                        humanName = sd.text
                except KeyError:
                    pass


            if serviceId == IsoServices.DiagnosticSessionControl:
                sessionService_flag = True

                requestFunc = DiagnosticSessionControlMethodFactory.create_requestFunction(value, xmlElements)
                diagnosticSessionControlContainer.add_requestFunction(requestFunc, humanName)

                negativeResponseFunction = DiagnosticSessionControlMethodFactory.create_checkNegativeResponseFunction(value, xmlElements)
                diagnosticSessionControlContainer.add_negativeResponseFunction(negativeResponseFunction, humanName)

                checkFunc = DiagnosticSessionControlMethodFactory.create_checkPositiveResponseFunction(value, xmlElements)
                diagnosticSessionControlContainer.add_checkFunction(checkFunc, humanName)

                positiveResponseFunction = DiagnosticSessionControlMethodFactory.create_encodePositiveResponseFunction(value, xmlElements)
                diagnosticSessionControlContainer.add_positiveResponseFunction(positiveResponseFunction, humanName)

            elif serviceId == IsoServices.EcuReset:
                ecuResetService_flag = True

                requestFunc = ECUResetMethodFactory.create_requestFunction(value, xmlElements)
                ecuResetContainer.add_requestFunction(requestFunc, humanName)

                negativeResponseFunction = ECUResetMethodFactory.create_checkNegativeResponseFunction(value, xmlElements)
                ecuResetContainer.add_negativeResponseFunction(negativeResponseFunction, humanName)

                try:
                    transmissionMode = value.attrib['TRANSMISSION-MODE']
                    if transmissionMode == "SEND-ONLY":
                        sendOnly_flag = True
                except:
                    sendOnly_flag = False

                if sendOnly_flag:
                    checkFunc = None
                    positiveResponseFunction = None
                else:
                    checkFunc = ECUResetMethodFactory.create_checkPositiveResponseFunction(value, xmlElements)
                    positiveResponseFunction = ECUResetMethodFactory.create_encodePositiveResponseFunction(value, xmlElements)

                ecuResetContainer.add_checkFunction(checkFunc, humanName)
                ecuResetContainer.add_positiveResponseFunction(positiveResponseFunction, humanName)
                pass

            elif serviceId == IsoServices.ReadDataByIdentifier:
                rdbiService_flag = True

                # The new code extends the range of functions required, in order to handle RDBI working for concatenated lists of DIDs ...
                requestFunctions = ReadDataByIdentifierMethodFactory.create_requestFunctions(value, xmlElements)
                rdbiContainer.add_requestSIDFunction(requestFunctions[0], humanName)  # ... note: this will now need to handle replication of this one!!!!
                rdbiContainer.add_requestDIDFunction(requestFunctions[1], humanName)


                negativeResponseFunction = ReadDataByIdentifierMethodFactory.create_checkNegativeResponseFunction(value, xmlElements)
                rdbiContainer.add_negativeResponseFunction(negativeResponseFunction, humanName)


                checkFunctions = ReadDataByIdentifierMethodFactory.create_checkPositiveResponseFunctions(value, xmlElements)
                rdbiContainer.add_checkSIDResponseFunction(checkFunctions[0], humanName)
                rdbiContainer.add_checkSIDLengthFunction(checkFunctions[1], humanName)
                rdbiContainer.add_checkDIDResponseFunction(checkFunctions[2], humanName)
                rdbiContainer.add_checkDIDLengthFunction(checkFunctions[3], humanName)


                positiveResponseFunction = ReadDataByIdentifierMethodFactory.create_encodePositiveResponseFunction(value, xmlElements)
                rdbiContainer.add_positiveResponseFunction(positiveResponseFunction, humanName)

            elif serviceId == IsoServices.SecurityAccess:
                if isDiagServiceTransmissionOnly(value) == False:
                    requestFunction = SecurityAccessMethodFactory.create_requestFunction(value, xmlElements)
                    securityAccessContainer.add_requestFunction(requestFunction, humanName)

                    negativeResponseFunction = SecurityAccessMethodFactory.create_checkNegativeResponseFunction(value, xmlElements)
                    securityAccessContainer.add_negativeResponseFunction(negativeResponseFunction, humanName)

                    checkFunction = SecurityAccessMethodFactory.create_checkPositiveResponseFunction(value, xmlElements)
                    securityAccessContainer.add_positiveResponseFunction(checkFunction, humanName)

                    securityAccess_flag = True

            elif serviceId == IsoServices.WriteDataByIdentifier:

                wdbiService_flag = True
                requestFunc = WriteDataByIdentifierMethodFactory.create_requestFunction(value, xmlElements)
                wdbiContainer.add_requestFunction(requestFunc, humanName)

                negativeResponseFunction = WriteDataByIdentifierMethodFactory.create_checkNegativeResponseFunction(value, xmlElements)
                wdbiContainer.add_negativeResponseFunction(negativeResponseFunction, humanName)

                checkFunc = WriteDataByIdentifierMethodFactory.create_checkPositiveResponseFunction(value, xmlElements)
                wdbiContainer.add_checkFunction(checkFunc, humanName)

                positiveResponseFunction = WriteDataByIdentifierMethodFactory.create_encodePositiveResponseFunction(value, xmlElements)
                wdbiContainer.add_positiveResponseFunction(positiveResponseFunction, humanName)

            elif serviceId == IsoServices.ClearDiagnosticInformation:
                clearDTCService_flag = True
                requestFunc = ClearDTCMethodFactory.create_requestFunction(value, xmlElements)
                clearDTCContainer.add_requestFunction(requestFunc, humanName)

                negativeResponseFunction = ClearDTCMethodFactory.create_checkNegativeResponseFunction(value, xmlElements)
                clearDTCContainer.add_negativeResponseFunction(negativeResponseFunction, humanName)

                checkFunc = ClearDTCMethodFactory.create_checkPositiveResponseFunction(value, xmlElements)
                clearDTCContainer.add_checkFunction(checkFunc, humanName)

                positiveResponseFunction = ClearDTCMethodFactory.create_encodePositiveResponseFunction(value, xmlElements)
                clearDTCContainer.add_positiveResponseFunction(positiveResponseFunction, humanName)

            elif serviceId == IsoServices.ReadDTCInformation:
                readDTCService_flag = True
                requestFunction, qualifier = ReadDTCMethodFactory.create_requestFunction(value, xmlElements)
                if qualifier != "":
                    readDTCContainer.add_requestFunction(requestFunction, "FaultMemoryRead"+qualifier)

                    negativeResponseFunction = ReadDTCMethodFactory.create_checkNegativeResponseFunction(value, xmlElements)
                    readDTCContainer.add_negativeResponseFunction(negativeResponseFunction, "FaultMemoryRead"+qualifier)

                    checkFunction = ReadDTCMethodFactory.create_checkPositiveResponseFunction(value, xmlElements)
                    readDTCContainer.add_checkFunction(checkFunction, "FaultMemoryRead"+qualifier)

                    positiveResponseFunction = ReadDTCMethodFactory.create_encodePositiveResponseFunction(value, xmlElements)
                    readDTCContainer.add_positiveResponseFunction(positiveResponseFunction, "FaultMemoryRead"+qualifier)

            elif serviceId == IsoServices.InputOutputControlByIdentifier:
                ioCtrlService_flag = True
                requestFunc, qualifier  = InputOutputControlMethodFactory.create_requestFunction(value, xmlElements)
                if qualifier != "":
                    inputOutputControlContainer.add_requestFunction(requestFunc, humanName+qualifier)

                    negativeResponseFunction = InputOutputControlMethodFactory.create_checkNegativeResponseFunction(value, xmlElements)
                    inputOutputControlContainer.add_negativeResponseFunction(negativeResponseFunction, humanName+qualifier)

                    checkFunc = InputOutputControlMethodFactory.create_checkPositiveResponseFunction(value, xmlElements)
                    inputOutputControlContainer.add_checkFunction(checkFunc, humanName+qualifier)

                    positiveResponseFunction = InputOutputControlMethodFactory.create_encodePositiveResponseFunction(value, xmlElements)
                    inputOutputControlContainer.add_positiveResponseFunction(positiveResponseFunction, humanName+qualifier)

            elif serviceId == IsoServices.RoutineControl:
                routineCtrlService_flag = True
                # We need a qualifier, as the human name for the start stop, and results calls are all the same, so they otherwise overwrite each other
                requestFunc, qualifier = RoutineControlMethodFactory.create_requestFunction(value, xmlElements)
                if qualifier != "":
                    routineControlContainer.add_requestFunction(requestFunc, humanName+qualifier)

                    negativeResponseFunction = RoutineControlMethodFactory.create_checkNegativeResponseFunction(value, xmlElements)
                    routineControlContainer.add_negativeResponseFunction(negativeResponseFunction, humanName+qualifier)

                    checkFunc = RoutineControlMethodFactory.create_checkPositiveResponseFunction(value, xmlElements)
                    routineControlContainer.add_checkFunction(checkFunc, humanName+qualifier)

                    positiveResponseFunction = RoutineControlMethodFactory.create_encodePositiveResponseFunction(value, xmlElements)
                    routineControlContainer.add_positiveResponseFunction(positiveResponseFunction, humanName+qualifier)

            elif serviceId == IsoServices.RequestDownload:
                reqDownloadService_flag = True
                requestFunc = RequestDownloadMethodFactory.create_requestFunction(value, xmlElements)
                requestDownloadContainer.add_requestFunction(requestFunc, humanName)

                negativeResponseFunction = RequestDownloadMethodFactory.create_checkNegativeResponseFunction(value, xmlElements)
                requestDownloadContainer.add_negativeResponseFunction(negativeResponseFunction, humanName)

                checkFunc = RequestDownloadMethodFactory.create_checkPositiveResponseFunction(value, xmlElements)
                requestDownloadContainer.add_checkFunction(checkFunc, humanName)

                positiveResponseFunction = RequestDownloadMethodFactory.create_encodePositiveResponseFunction(value, xmlElements)
                requestDownloadContainer.add_positiveResponseFunction(positiveResponseFunction, humanName)

            elif serviceId == IsoServices.RequestUpload:
                reqUploadService_flag = True
                requestFunc = RequestUploadMethodFactory.create_requestFunction(value, xmlElements)
                requestUploadContainer.add_requestFunction(requestFunc, humanName)

                negativeResponseFunction = RequestUploadMethodFactory.create_checkNegativeResponseFunction(value, xmlElements)
                requestUploadContainer.add_negativeResponseFunction(negativeResponseFunction, humanName)

                checkFunc = RequestUploadMethodFactory.create_checkPositiveResponseFunction(value, xmlElements)
                requestUploadContainer.add_checkFunction(checkFunc, humanName)

                positiveResponseFunction = RequestUploadMethodFactory.create_encodePositiveResponseFunction(value, xmlElements)
                requestUploadContainer.add_positiveResponseFunction(positiveResponseFunction, humanName)

            elif serviceId == IsoServices.TransferData:
                transDataService_flag = True
                requestFunc = TransferDataMethodFactory.create_requestFunction(value, xmlElements)
                transferDataContainer.add_requestFunction(requestFunc, humanName)

                negativeResponseFunction = TransferDataMethodFactory.create_checkNegativeResponseFunction(value, xmlElements)
                transferDataContainer.add_negativeResponseFunction(negativeResponseFunction, humanName)

                checkFunc = TransferDataMethodFactory.create_checkPositiveResponseFunction(value, xmlElements)
                transferDataContainer.add_checkFunction(checkFunc, humanName)

                positiveResponseFunction = TransferDataMethodFactory.create_encodePositiveResponseFunction(value, xmlElements)
                transferDataContainer.add_positiveResponseFunction(positiveResponseFunction, humanName)

            elif serviceId == IsoServices.RequestTransferExit:
                transExitService_flag = True
                requestFunc = TransferExitMethodFactory.create_requestFunction(value, xmlElements)
                transferExitContainer.add_requestFunction(requestFunc, humanName)

                negativeResponseFunction = TransferExitMethodFactory.create_checkNegativeResponseFunction(value, xmlElements)
                transferExitContainer.add_negativeResponseFunction(negativeResponseFunction, humanName)

                checkFunc = TransferExitMethodFactory.create_checkPositiveResponseFunction(value, xmlElements)
                transferExitContainer.add_checkFunction(checkFunc, humanName)

                positiveResponseFunction = TransferExitMethodFactory.create_encodePositiveResponseFunction(value, xmlElements)
                transferExitContainer.add_positiveResponseFunction(positiveResponseFunction, humanName)

            elif serviceId == IsoServices.TesterPresent:
                # Note: Tester Present is presented here as an exposed service, but it will typically not be called directly, as we'll hook it 
                # in to keep the session alive automatically if requested (details to come, but this is just getting the comms into place).
                testerPresentService_flag = True
                requestFunc = TesterPresentMethodFactory.create_requestFunction(value, xmlElements)
                testerPresentContainer.add_requestFunction(requestFunc, "TesterPresent")

                negativeResponseFunction = TesterPresentMethodFactory.create_checkNegativeResponseFunction(value, xmlElements)
                testerPresentContainer.add_negativeResponseFunction(negativeResponseFunction, "TesterPresent")

                checkFunc = TesterPresentMethodFactory.create_checkPositiveResponseFunction(value, xmlElements)
                testerPresentContainer.add_checkFunction(checkFunc, "TesterPresent")

                positiveResponseFunction = TesterPresentMethodFactory.create_encodePositiveResponseFunction(value, xmlElements)
                testerPresentContainer.add_positiveResponseFunction(positiveResponseFunction, "TesterPresent")


    #need to be able to extract the reqId and resId
    outputEcu = Uds(ihexFile=ihexFile, **kwargs)

    # Bind any ECU Reset services that have been found
    if sessionService_flag:
        setattr(outputEcu, 'diagnosticSessionControlContainer', diagnosticSessionControlContainer)
        diagnosticSessionControlContainer.bind_function(outputEcu)

    # Bind any ECU Reset services that have been found
    if ecuResetService_flag:
        setattr(outputEcu, 'ecuResetContainer', ecuResetContainer)
        ecuResetContainer.bind_function(outputEcu)

    # Bind any rdbi services that have been found
    if rdbiService_flag:
        setattr(outputEcu, 'readDataByIdentifierContainer', rdbiContainer)
        rdbiContainer.bind_function(outputEcu)

    # Bind any security access services have been found
    if securityAccess_flag:
        setattr(outputEcu, 'securityAccessContainer', securityAccessContainer)
        securityAccessContainer.bind_function(outputEcu)

    # Bind any wdbi services have been found
    if wdbiService_flag:
        setattr(outputEcu, 'writeDataByIdentifierContainer', wdbiContainer)
        wdbiContainer.bind_function(outputEcu)

    # Bind any clear DTC services that have been found
    if clearDTCService_flag:
        setattr(outputEcu, 'clearDTCContainer', clearDTCContainer)
        clearDTCContainer.bind_function(outputEcu)

    # Bind any read DTC services that have been found
    if readDTCService_flag:
        setattr(outputEcu, 'readDTCContainer', readDTCContainer)
        readDTCContainer.bind_function(outputEcu)

    # Bind any input output control services that have been found
    if ioCtrlService_flag:
        setattr(outputEcu, 'inputOutputControlContainer', inputOutputControlContainer)
        inputOutputControlContainer.bind_function(outputEcu)

    # Bind any routine control services that have been found
    if routineCtrlService_flag:
        setattr(outputEcu, 'routineControlContainer', routineControlContainer)
        routineControlContainer.bind_function(outputEcu)

    # Bind any request download services that have been found
    if reqDownloadService_flag:
        setattr(outputEcu, 'requestDownloadContainer', requestDownloadContainer)
        requestDownloadContainer.bind_function(outputEcu)

    # Bind any request upload services that have been found
    if reqUploadService_flag:
        setattr(outputEcu, 'requestUploadContainer', requestUploadContainer)
        requestUploadContainer.bind_function(outputEcu)

    # Bind any transfer data services that have been found
    if transDataService_flag:
        setattr(outputEcu, 'transferDataContainer', transferDataContainer)
        transferDataContainer.bind_function(outputEcu)

    # Bind any transfer exit data services that have been found
    if transExitService_flag:
        setattr(outputEcu, 'transferExitContainer', transferExitContainer)
        transferExitContainer.bind_function(outputEcu)

    # Bind any tester present services that have been found
    if testerPresentService_flag:
        setattr(outputEcu, 'testerPresentContainer', testerPresentContainer)
        testerPresentContainer.bind_function(outputEcu)

    return outputEcu


if __name__ == "__main__":

    a = createUdsConnection('Bootloader.odx', 'bootloader')

    a.diagnosticSessionControl('Default Session')
    a.ecuReset('Hard Reset',suppressResponse=False)
    a.readDataByIdentifier('ECU Serial Number')
    a.writeDataByIdentifier('ECU Serial Number','ABC0011223344556')
    a.clearDTC([0xF1, 0xC8, 0x55])
    #a.readDTC(IsoReadDTCSubfunction.reportNumberOfDTCByStatusMask, DTCStatusMask=Mask.confirmedDtc + Mask.testFailedSinceLastClear)
    #a.readDTC(IsoReadDTCSubfunction.reportDTCByStatusMask, DTCStatusMask=Mask.confirmedDtc + Mask.testFailedSinceLastClear)
    #a.readDTC(IsoReadDTCSubfunction.reportDTCSnapshotIdentification, DTCMaskRecord=[0xF1, 0xC8, 0x55], DTCSnapshotRecordNumber=0x34)
    #a.readDTC(IsoReadDTCSubfunction.reportDTCSnapshotRecordByDTCNumber, DTCMaskRecord=[0xF1, 0xC8, 0x55], DTCSnapshotRecordNumber=0x34)
    #a.readDTC(IsoReadDTCSubfunction.reportDTCSnapshotRecordByRecordNumber, DTCSnapshotRecordNumber=0x34)
    #a.readDTC(IsoReadDTCSubfunction.reportDTCExtendedDataRecordByDTCNumber, DTCMaskRecord=[0xF1, 0xC8, 0x55], DTCExtendedRecordNumber=0x12)
    #a.readDTC(IsoReadDTCSubfunction.reportNumberOfDTCBySeverityMaskRecord, DTCStatusMask=Mask.confirmedDtc + Mask.testFailedSinceLastClear, DTCSeverityMaskRecord=Mask.confirmedDtc)
    #a.readDTC(IsoReadDTCSubfunction.reportDTCBySeverityMaskRecord, DTCStatusMask=Mask.confirmedDtc + Mask.testFailedSinceLastClear, DTCSeverityMaskRecord=Mask.confirmedDtc)
    #a.readDTC(IsoReadDTCSubfunction.reportSeverityInformationOfDTC, DTCMaskRecord=[0xF1, 0xC8, 0x55])
    #a.readDTC(IsoReadDTCSubfunction.reportSupportedDTC)
    #a.readDTC(IsoReadDTCSubfunction.reportFirstTestFailedDTC)
    #a.readDTC(IsoReadDTCSubfunction.reportFirstConfirmedDTC)
    #a.readDTC(IsoReadDTCSubfunction.reportMostRecentTestFailedDTC)
    #a.readDTC(IsoReadDTCSubfunction.reportMostRecentConfirmedDTC)
    #a.readDTC(IsoReadDTCSubfunction.reportMirrorMemoryDTCByStatusMask, DTCStatusMask=Mask.confirmedDtc + Mask.testFailedSinceLastClear)
    #a.readDTC(IsoReadDTCSubfunction.reportMirrorMemoryDTCExtendedDataRecordByDTCNumber, DTCMaskRecord=[0xF1, 0xC8, 0x55], DTCExtendedRecordNumber=0x12)
    #a.readDTC(IsoReadDTCSubfunction.reportNumberOfMirrorMemoryDTCByStatusMask, DTCStatusMask=Mask.confirmedDtc + Mask.testFailedSinceLastClear)
    #a.readDTC(IsoReadDTCSubfunction.reportNumberOfEmissionsRelatedOBDDTCByStatusMask, DTCStatusMask=Mask.confirmedDtc + Mask.testFailedSinceLastClear)
    #a.readDTC(IsoReadDTCSubfunction.reportEmissionsRelatedOBDDTCByStatusMask, DTCStatusMask=Mask.confirmedDtc + Mask.testFailedSinceLastClear)
    a.inputOutputControl('Booster Target Speed',IsoInputOutputControlOptionRecord.adjust,[8000])
    a.routineControl('Erase Memory',IsoRoutineControlType.startRoutine,[('memoryAddress',[0x01]),('memorySize',[0xF000])])
    a.requestDownload(FormatIdentifier=[0x00],MemoryAddress=[0x40, 0x03, 0xE0, 0x00],MemorySize=[0x00, 0x00, 0x0E, 0x56])
    #a.requestUpload(FormatIdentifier=[0x00],MemoryAddress=[0x40, 0x03, 0xE0, 0x00],MemorySize=[0x00, 0x00, 0x0E, 0x56])   # Not tested or runnable at present
    a.transferData(0x01,[0xF1,0xF2,0xF3,0xF4,0xF5,0xF6,0xF7,0xF8,0xF9,0xFA,0xFB,0xFC,0xFD,0xFE,0xFF])
    a.transferExit([0xF1,0xF2,0xF3,0xF4,0xF5,0xF6,0xF7,0xF8,0xF9,0xFA,0xFB,0xFC,0xFD,0xFE,0xFF])
    a.testerPresent(suppressResponse=False)
