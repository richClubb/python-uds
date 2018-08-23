import abc

class iResettableTimer(object):
    __metaclass__ = abc.ABCMeta

    @property
    @abc.abstractmethod
    def timeoutTime(self):
        raise NotImplementedError("class has not implemented this method")

    @timeoutTime.setter
    @abc.abstractmethod
    def timeoutTime(self, val):
        raise NotImplementedError("class has not implemented this method")

    @property
    @abc.abstractmethod
    def state(self):
        raise NotImplementedError("class has not implemented this method")

    @abc.abstractmethod
    def start(self):
        raise NotImplementedError("class has not implemented this method")

    @abc.abstractmethod
    def reset(self):
        raise NotImplementedError("class has not implemented this method")

    @abc.abstractmethod
    def stop(self):
        raise NotImplementedError("class has not implemented this method")

    @abc.abstractmethod
    def isRunning(self):
        raise NotImplementedError("class has not implemented this method")

    @abc.abstractmethod
    def expired(self):
        raise NotImplementedError("class has not implemented this method")