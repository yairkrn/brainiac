from furl import furl

from .data_types import ServerParsersMessage
from ..utils import imports
from ..config import config


class MessageQueue:
    def __init__(self, url):
        self._url = furl(url)
        self._driver = self._find_driver()

    def _find_driver(self):
        modules = imports.import_by_glob(__package__, 'driver_*.py')  # TODO: move to consts
        for module in modules:
            classes = imports.get_class_by_regex(module, '[A-Za-z]+Driver')  # TODO: move to consts
            for cls in classes:
                if cls.SCHEME == self._url.scheme:
                    return cls(self._url)
        raise RuntimeError(f'No MessageQueue driver found for {self._url}')

    def publish(self, tag, message):
        self._driver.publish(tag, message.serialize())

    def consume(self, tag, message_type, callback):
        def _consumer_callback(message):
            message = message_type.deserialize(message)
            callback(message)
        self._driver.register_consumer(tag, _consumer_callback)
        self._driver.start_consuming()
