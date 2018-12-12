"""This file is an experiment and should not be used for any serious coding"""

from uds import Uds
import xml.etree.ElementTree as ET
from uds import DecodeFunctions

from types import MethodType

def get_diagServiceServiceId(diagServiceElement, requests):

    requestElementRef = diagServiceElement.find('REQUEST-REF').attrib['ID-REF']

    requestElement = requests[requestElementRef]
    requestElementParamsElement = requestElement.find('PARAMS')

    try:
        for i in requestElementParamsElement:
            if(i.attrib['SEMANTIC'] == 'SERVICE-ID'):
                return int(i.find('CODED-VALUE').text)
    except AttributeError:
        return None

    return None

def create_sessionControlRequest_function(xmlElement):

    serviceId = None
    subFunction = None
    params = xmlElement.find('PARAMS')
    for param in params:
        if(param.attrib['SEMANTIC'] == 'SERVICE-ID'):
            serviceId = int(param.find('CODED-VALUE').text)
        if(param.attrib['SEMANTIC'] == 'SUBFUNCTION'):
            subFunction = int(param.find('CODED-VALUE').text)

    req = [serviceId, subFunction]
    functionName = str("request_{0}").format((xmlElement.find('SHORT-NAME')).text)

    func = str("def {0}():\n"
               "    return {1}").format(functionName, req)
    exec(func)
    return locals()[functionName]


def create_readDataByIdentifierRequest_function(xmlElement):

    serviceId = None
    diagnosticId = None

    params = xmlElement.find('PARAMS')

    for param in params:
        semantic = param.attrib['SEMANTIC']
        if(semantic == 'SERVICE-ID'):
            serviceId = int(param.find('CODED-VALUE').text)
        if(semantic == 'ID'):
            diagnosticId = int(param.find('CODED-VALUE').text)

    req = [serviceId] + DecodeFunctions.intArrayToIntArray([diagnosticId], 'int16', 'int8')
    functionName = str("request_{0}").format(xmlElement.find('SHORT-NAME').text)

    func = str("def {0}():\n"
               "    return {1}").format(functionName, req)
    exec(func)
    return locals()[functionName]


def create_writeDataByIdentifierRequest_function(xmlElement, dataObjects):

    serviceId = None
    diagnosticId = None

    params = xmlElement.find('PARAMS')

    checkFunction = ""
    encodeFunction = ""
    inputParams = []
    index = 1

    for param in params:
        semantic = param.attrib['SEMANTIC']
        if (semantic == 'SERVICE-ID'):
            serviceId = int(param.find('CODED-VALUE').text)
        if (semantic == 'ID'):
            diagnosticId = int(param.find('CODED-VALUE').text)
        if (semantic == 'DATA'):
            dataObject = dataObjects[param.find('DOP-REF').attrib['ID-REF']]
            diagCodedType = dataObject.find('DIAG-CODED-TYPE')
            dataType = diagCodedType.attrib['BASE-DATA-TYPE']
            length = int(diagCodedType.find('BIT-LENGTH').text)
            if(dataType == 'A_ASCIISTRING'):
                inputParam = str('aString{0}').format(index)
                inputParams.append(inputParam)
                index += 1
                checkFunction += str(
                    'if(len({1})) != {0}: raise Exception(str(\"incorrect length of input string. Got: {{0}}: Expected {0}\").format(len({1})))').format(
                    int(length / 8), inputParam)
                encodeFunction += str(' + DecodeFunctions.stringToIntList({0}, None)').format(inputParam)
            elif(dataType == 'A_UINT32'):
                inputParam = str('aInt{0}').format(index)
                inputParams.append(inputParam)
                index += 1
                numOfBytes = int(length / 8)
                if(numOfBytes == 1):
                    inputType = 'int8'
                elif(numOfBytes == 2):
                    inputType = 'int16'
                elif(numOfBytes == 3):
                    inputType = 'int24'
                elif(numOfBytes == 4):
                    inputType = 'int32'
                encodeFunction += str(' + DecodeFunctions.intArrayToUInt8Array([{0}], \'{1}\')').format(inputParam,
                                                                                                      inputType)
            else:
                print("Unknown datatype")

    req = [serviceId] + DecodeFunctions.intArrayToIntArray([diagnosticId], 'int16', 'int8')
    functionName = str("request_{0}").format(xmlElement.find('SHORT-NAME').text)

    try:
        func = str("def {0}({1}):\n"
                   "    {2}\n"
                   "    return {3}{4}").format(functionName,
                                                  ", ".join(inputParams),
                                                  checkFunction,
                                                  req,
                                                  encodeFunction)
    except:
        pass
    exec(func)
    return locals()[functionName]


class RequestMethodFactory(object):

    def createRequestMethod(xmlElement, dataObjects):
        function = None

        # extract the service ID to find out how this needs to be decoded
        paramsElement = xmlElement.find('PARAMS')
        params = {}
        shortName = xmlElement.find('SHORT-NAME').text
        id = xmlElement.attrib['ID']
        for param in paramsElement:
            try:
                params[param.attrib['SEMANTIC']] = param
            except:
                print("Found param with no semantic field")
                pass

        serviceId = int(params['SERVICE-ID'].find('CODED-VALUE').text)

        a = None
        # call the relevant method to create the dynamic function
        if(serviceId == 0x10):
            a = create_sessionControlRequest_function(xmlElement)
        if(serviceId == 0x22):
            a = create_readDataByIdentifierRequest_function(xmlElement)
        elif(serviceId == 0x2E):
            try:
                a = create_writeDataByIdentifierRequest_function(xmlElement, dataObjects)
            except:
                print("Failed to create WDBI function")

        if a is not None:
            if(serviceId != 0x2E):
                print(a())
            else:
                try:
                    print(a("0000000000000009"))
                except:
                    pass
                try:
                    print(a(0x01, "000000000000000000000000"))
                except:
                    pass
                pass
        pass

        return a

class PositiveResponseFactory(object):

    def __init__(self, xmlElement, dataObjectElements):
        pass


class NegativeResponse(object):

    pass


def fillDictionary(xmlElement):
    dict = {}

    for i in xmlElement:
        dict[i.attrib['ID']] = i

    return dict

def create_udsConnection(xmlElement, ecuName):

    dataObjectPropsElement = None
    diagCommsElement = None
    requestsElement = None
    posResponsesElement = None
    negResponsesElement = None

    for child in xmlElement.iter():
        if (child.tag == 'DATA-OBJECT-PROPS'):
            dataObjectPropsElement = child
        elif (child.tag == 'DIAG-COMMS'):
            diagCommsElement = child
        elif (child.tag == 'REQUESTS'):
            requestsElement = child
        elif (child.tag == 'POS-RESPONSES'):
            posResponsesElement = child
        elif (child.tag == 'NEG-RESPONSES'):
            negResponsesElement = child

    dataObjectProps = fillDictionary(dataObjectPropsElement)
    requests = fillDictionary(requestsElement)
    posResponses = fillDictionary(posResponsesElement)
    negResponses = fillDictionary(negResponsesElement)

    requestFunctions = {}
    checkFunctions = {}
    positiveResponseFunctions = {}
    negativeResponseFunctions = {}

    for i in diagCommsElement:
        requestRef = None
        posResponseRef = None
        negResponseRef = None
        shortName = i.find('SHORT-NAME').text

        test = get_diagServiceServiceId(i, requests)

        dictEntry = ""
        sdgs = i.find('SDGS')
        sdg = sdgs.find('SDG')
        for j in sdg:
            if j.tag == 'SD':
                if j.attrib['SI'] == 'DiagInstanceName':
                    dictEntry = j.text

        print(dictEntry)
        requestRef = i.find('REQUEST-REF')
        try:
            posResponseRef = (i.find('POS-RESPONSE-REFS')).find('POS-RESPONSE-REF')
            negResponseRef = (i.find('NEG-RESPONSE-REFS')).find('NEG-RESPONSE-REF')
        except (KeyError, AttributeError):
            posResponseRef = None
            negResponseRef = None

        requestElement = requests[requestRef.attrib['ID-REF']]
        requestFunction = RequestMethodFactory.createRequestMethod(requestElement, dataObjectProps)

        if(posResponseRef != None):
            posResponseElement = posResponses[posResponseRef.attrib['ID-REF']]
            posResponse = PositiveResponseFactory(posResponseElement, dataObjectProps)
        if(negResponseRef != None):
            negResponseElement = negResponses[negResponseRef.attrib['ID-REF']]

        requestFunctions[shortName] = requestFunction


    temp_ecu = Uds()

    setattr(temp_ecu, '__requestFunctions', requestFunctions)

    print(requestFunctions)

    temp_ecu.readDataByIdentifier = MethodType(readDataByIdentifier, temp_ecu)

    print("successfully created ECU")

    return temp_ecu



def readDataByIdentifier(self, diagnosticIdentifier):

    requestFunction = self.__requestFunctions[diagnosticIdentifier]
    # checkFunction = self.__checkFunctions[diagnosticIdentifier]
    # negativeResponseFunction = self.__negativeResponseFunctions[diagnosticIdentifier]
    # positiveResponseFunction = self.__positiveResponseFunctions[diagnosticIdentifier]

    print(requestFunction())

if __name__ == "__main__":

    tree = ET.parse('Bootloader.odx')

    bootloader = create_udsConnection(tree, 'bootloader')

    print(bootloader.readDataByIdentifier('ECU_Serial_Number_Read'))

    pass
