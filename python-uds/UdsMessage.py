

class UdsMessage(object):

    """
        General constructor for the UdsMessage class
    """
    def __init__(self, servId=None, payload=None):
        self.__serviceId = servId
        self.__payload = payload
        pass

    """
        @return an integer, the serviceId
    """
    @property
    def serviceId(self):
        if(self.__serviceId == None):
            raise TypeError("ServiceId not initialised")
        return self.__serviceId

    """
    
    """
    @serviceId.setter
    def serviceId(self, val):
        if type(val) == int:
            self.__serviceId = val
        else:
            raise TypeError("Attempt to enter non-integer value to serviceId")

    """
        @return a list
        @throws TypeError if the payload is not initialised with a value
    """
    @property
    def payload(self):
        if(self.__payload == None):
            raise TypeError("Payload not initialised")
        return self.__payload

    """
        @param val - a list
        @throws TypeError if the val is not a list
    """
    @payload.setter
    def payload(self, val):
        if type(val) == list:
            self.__payload = val
        else:
            raise TypeError("Attempt to enter non-list value to payload")


if __name__ == "__main__":

    test = UdsMessage()

    try:
        print(test.serviceId)
    except TypeError:
        print("Check Passed")
    except:
        print("Check Fail")

    test.serviceId = 0x10
    assert(test.serviceId == 0x10)

    try:
        test.serviceId = "int"
    except TypeError:
        print("Check passed")
    except:
        print("Check Failed")

