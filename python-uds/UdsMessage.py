

class UdsMessage(object):

    """
        General constructor for the UdsMessage class
    """
    def __init__(self):
        self.__serviceId = None
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