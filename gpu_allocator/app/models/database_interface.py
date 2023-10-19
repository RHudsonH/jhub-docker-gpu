import abc

class DatabaseInterface(abc.ABC):
    def __init__(self, oversubscribe_limit):
        self.oversubscribe_limit = oversubscribe_limit

    @abc.abstractmethod
    def update_devices(self, devices):
        pass

    @abc.abstractmethod
    def list_devices(self, devices):
        pass

    @abc.abstractmethod
    def get_device(self, devices):
        pass

    @abc.abstractmethod
    def allocate_device(self, devices):
        pass

    @abc.abstractmethod
    def release_device(self, devices):
        pass