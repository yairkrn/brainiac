from furl import furl
from ..utils import imports


class MessageQueue:
    def __init__(self, url):
        self._url = furl(url)
        self._driver = self._find_driver()

    def _find_driver(self):
        modules = imports.import_by_glob(__package__, 'driver_*.py')
        for module in modules:
            classes = imports.get_class_by_regex(module, '[a-z]+Driver')
            for cls in classes:
                if cls.SCHEME == self._url.scheme:
                    return cls(self._url)
        raise RuntimeError(f'No MessageQueue driver found for {self._url}')
