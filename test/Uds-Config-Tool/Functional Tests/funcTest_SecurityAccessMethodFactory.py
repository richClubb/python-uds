
from uds.uds_config_tool.FunctionCreation.SecurityAccessMethodFactory import SecurityAccessMethodFactory
from uds.uds_config_tool.UtilityFunctions import getSdgsDataItem


if __name__ == "__main__":

    import xml.etree.ElementTree as ET
    import inspect

    filename = "Bootloader.odx"

    root = ET.parse(filename)

    xmlElements = {}

    for child in root.iter():
        currTag = child.tag
        try:
            xmlElements[child.attrib['ID']] = child
        except KeyError:
            pass

    for key, value in xmlElements.items():

        if value.tag == "DIAG-SERVICE":
            if value.attrib["SEMANTIC"] == "SECURITY":

                suppressResponse = getSdgsDataItem(value, "PositiveResponseSuppressed")
                if suppressResponse == "no":
                    a = SecurityAccessMethodFactory.create_requestFunction(value, xmlElements)
                    b = SecurityAccessMethodFactory.create_checkPositiveResponseFunction(value, xmlElements)
                    c = SecurityAccessMethodFactory.create_checkNegativeResponseFunction(value, xmlElements)
                pass
