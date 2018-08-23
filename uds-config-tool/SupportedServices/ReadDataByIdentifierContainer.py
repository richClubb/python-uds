from SupportedServices.iContainer import iContainer
from types import MethodType
import UdsMessage

class ReadDataByIdentifierContainer(iContainer):

    def __init__(self):
        self.requestFunctions = {}
        self.checkFunctions = {}
        self.negativeResponseFunctions = {}
        self.positiveResponseFunctions = {}

    @staticmethod
    def __readDataByIdentifier(self, parameter):
        requestFunction = self.readDataByIdentifierContainer.requestFunctions[parameter]
        checkFunction = self.readDataByIdentifierContainer.checkFunctions[parameter]
        negativeResponseFunction = self.readDataByIdentifierContainer.negativeResponseFunctions[parameter]
        positiveResponseFunction = self.readDataByIdentifierContainer.positiveResponseFunctions[parameter]

        udsMsg = UdsMessage.UdsMessage()
        udsMsg.request = requestFunction()

        a = self.send(udsMsg)

        checkFunction(udsMsg.response_raw)
        negativeResponseFunction(udsMsg.response_raw)
        return positiveResponseFunction(udsMsg.response_raw)

    def bind_readDataByIdentifierFunction(self, bindObject):
        bindObject.readDataByIdentifier = MethodType(self.__readDataByIdentifier, bindObject)

    def add_requestFunction(self, aFunction, dictionaryEntry):
        self.requestFunctions[dictionaryEntry] = aFunction

    def add_checkFunction(self, aFunction, dictionaryEntry):
        self.checkFunctions[dictionaryEntry] = aFunction

    def add_negativeResponseFunction(self, aFunction, dictionaryEntry):
        self.negativeResponseFunctions[dictionaryEntry] = aFunction

    def add_positiveResponseFunction(self, aFunction, dictionaryEntry):
        self.positiveResponseFunctions[dictionaryEntry] = aFunction


if __name__ == "__main__":

    pass




