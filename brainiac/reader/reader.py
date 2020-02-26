import gzip

from furl import furl

from .driver_proto import ProtoDriver
from ..utils import imports


class Reader:
    _SUFFIX_TO_OPEN_FUNCTION = {
        '.gz': gzip.open
    }

    def __init__(self, url):
        self._url = furl(url)
        open_function = self._find_open()
        self._driver = self._find_driver(open_function)

    def _find_open(self):
        for suffix, open_function in self._SUFFIX_TO_OPEN_FUNCTION.items():
            if str(self._url.host).endswith(suffix):
                return open_function
        return open

    def _find_driver(self, open_function):
        modules = imports.import_by_glob(__package__, 'driver_*.py')  # TODO: move to consts
        for module in modules:
            classes = imports.get_class_by_regex(module, '[A-Za-z]+Driver')  # TODO: move to consts
            for cls in classes:
                if cls.SCHEME == self._url.scheme:
                    return cls(self._url, open_function)
        # no driver found, take proto as default
        return ProtoDriver(self._url, open_function)

    @property
    def user(self):
        return self._driver.user

    def __iter__(self):
        yield from self._driver
