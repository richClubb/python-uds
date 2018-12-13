
##
# param: a diag service element
# return: a dictionary with the sdgs data elements
def getSdgsData(diagServiceElement):

    output = {}

    sdgs = diagServiceElement.find("SDGS")
    sdg = sdgs.find("SDG")
    for i in sdg:
        try:
            output[i.attrib['SI']] = i.text
        except:
            pass
    return output

##
# param: a diagServiceElement, an string representing the si attribute
# return: a specific entry from the sdgs params, or none if it does not exist
def getSdgsDataItem(diagServiceElement, itemName):

    outputDict = getSdgsData(diagServiceElement)

    try:
        output = outputDict[itemName]
    except:
        output = None

    return output

##
# param: an xml element
# return: a string with the short name, or None if no short name exists
def getShortName(xmlElement):

    try:
        output = xmlElement.find('SHORT-NAME').text
    except:
        output = None

    return output


##
# param: an xml element
# return: a string with the long name, or None if no long name exists
def getLongName(xmlElement):
    try:
        output = xmlElement.find('LONG-NAME').text
    except:
        output = None

    return output


##
# param: a diag service element, a list of other xmlElements
# return: an integer
def getServiceIdFromDiagService(diagServiceElement, xmlElements):

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


##
# param: a diag service element, a list of other xmlElements
# return: an integer
def getResponseIdFromDiagService(diagServiceElement, xmlElements):

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


##
# params: an xmlElement, the name of a semantic to match
# return: a single parameter matching the semantic, or a list of parameters which match the semantic
def getParamWithSemantic(xmlElement, semanticName):

    output = None

    try:
        params = xmlElement.find("PARAMS")
    except AttributeError:
        return output

    paramsList = []

    for i in params:
        paramSemantic = i.attrib["SEMANTIC"]
        if paramSemantic == semanticName:
            paramsList.append(i)

    if len(paramsList) == 0:
        output = None
    elif len(paramsList) == 1:
        output = paramsList[0]
    else:
        output = paramsList
    return output

##
# params: a diagnostic service element xml entry, and the dictionary of all possible xml elements
# return: if only 1 element, then a single xml element, else a list of xml elements, or none if no positive responses
def getPositiveResponse(diagServiceElement, xmlElements):

    positiveResponseList = []
    try:
        positiveResponseReferences = diagServiceElement.find("POS-RESPONSE-REFS")
    except:
        return None

    if positiveResponseReferences is None:
        return None
    else:
        for i in positiveResponseReferences:
            try:
                positiveResponseList.append(xmlElements[i.attrib["ID-REF"]])
            except:
                pass

    positiveResponseList_length = len(positiveResponseList)
    if positiveResponseList_length == 0:
        return None
    if positiveResponseList_length:
        return positiveResponseList[0]
    else:
        return positiveResponseList


def getDiagObjectProp(paramElement, xmlElements):

    try:
        dopElement = xmlElements[paramElement.find("DOP-REF").attrib["ID-REF"]]
    except:
        dopElement = None

    return dopElement

def getBitLengthFromDop(diagObjectPropElement):

    try:
        bitLength = int(diagObjectPropElement.find("DIAG-CODED-TYPE").find("BIT-LENGTH").text)
    except:
        bitLength = None

    return bitLength

def isDiagServiceTransmissionOnly(diagServiceElement):

    output = getSdgsDataItem(diagServiceElement, "PositiveResponseSuppressed")

    if output is not None:
        if output == "yes":
            return True

    return False


if __name__ == "__main__":

    pass
