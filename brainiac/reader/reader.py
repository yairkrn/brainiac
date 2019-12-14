from .driver_binary import BinaryDriver
from .driver_proto import ProtoDriver

class Reader:
    # TODO: automatically collect drivers.
    drivers = {
        BinaryDriver.SCHEME: BinaryDriver,
        ProtoDriver.SCHEME: ProtoDriver
    }

    def __init__(self, url):
        self.driver = self.find_driver(url)

    def find_driver(self, url):
        for scheme, cls in self.drivers.items():
            if url.startswith(scheme):
                return cls(url)
        raise ValueError(f'Url ({url}) does not match supported schemes: {list(self.drivers.keys())}')

    @property
    def user(self):
        return self.driver.user

    def __iter__(self):
        yield from self.driver
