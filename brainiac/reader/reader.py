import collections
import gzip

from .driver_binary import BinaryDriver
from .driver_proto import ProtoDriver


class Reader:
    # TODO: automatically collect drivers.
    drivers = {
        BinaryDriver.SCHEME: BinaryDriver,
        ProtoDriver.SCHEME: ProtoDriver
    }

    suffix_openers = {
        '.gz': gzip.open
    }

    def __init__(self, url):
        open_function = self.find_open(url)
        self.driver = self.find_driver(url, open_function)

    def find_open(self, url):
        for suffix, open_function in self.suffix_openers.items():
            if url.endswith(suffix):
                return open_function
        return open

    def find_driver(self, url, open_function):
        for scheme, cls in self.drivers.items():
            if url.startswith(scheme):
                return cls(url, open_function)
        raise ValueError(f'Url ({url}) does not match supported schemes: {list(self.drivers.keys())}')

    @property
    def user(self):
        return self.driver.user

    def __iter__(self):
        yield from self.driver
