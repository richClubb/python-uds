import Uds
import xml.etree.ElementTree as ET
from SupportedServices.ReadDataByIdentifierContainer import ReadDataByIdentifierContainer
from FunctionCreation.ReadDataByIdentifierMethodFactory import  ReadDataByIdentifierMethodFactory

supportedServices = {22, }

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

def createUdsConnection(xmlFile, ecuName):

    root = ET.parse(xmlFile)

    rdbiContainer = ReadDataByIdentifierContainer()

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

            if(serviceId == 0x22):
                requestFunc = ReadDataByIdentifierMethodFactory.create_requestFunction(value, xmlElements)
                rdbiContainer.add_requestFunction(requestFunc, humanName)

                negativeResponseFunction = ReadDataByIdentifierMethodFactory.create_checkNegativeResponseFunction(value,
                                                                                                                  xmlElements)
                rdbiContainer.add_negativeResponseFunction(negativeResponseFunction, humanName)
                checkFunc = ReadDataByIdentifierMethodFactory.create_checkPositiveResponseFunction(value, xmlElements)

                rdbiContainer.add_checkFunction(checkFunc, humanName)

                positiveResponseFunction = ReadDataByIdentifierMethodFactory.create_encodePositiveResponseFunction(value, xmlElements)
                rdbiContainer.add_positiveResponseFunction(positiveResponseFunction, humanName)

                # print("\n")

    outputEcu = Uds.Uds(0x600, 0x650)

    setattr(outputEcu, 'readDataByIdentifierContainer', rdbiContainer)
    rdbiContainer.bind_readDataByIdentifierFunction(outputEcu)

    return outputEcu


if __name__ == "__main__":

    a = createUdsConnection('Bootloader.odx', 'bootloader')

    a.readDataByIdentifier('ECU Serial Number')
    pass
