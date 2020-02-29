import logging
import inspect
import sys


_FORMAT = ("[%(asctime)s] [%(levelname)-8s] --- %(message)s (%(package)s)", "%Y-%m-%d %H:%M:%S")


class LogFilter(logging.Filter):
    @classmethod
    def _get_caller_package(cls):
        # determine name based on caller module
        for frm in inspect.stack():
            mod = inspect.getmodule(frm[0])
            if mod.__package__ not in [logging.__package__, __package__]:
                return mod.__package__

    def filter(self, record):
        record.package = self._get_caller_package()
        return True


def _get_logger():
    # create console handler with a higher log level
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)

    # create formatter and add it to the handlers
    formatter = logging.Formatter(*_FORMAT)
    ch.setFormatter(formatter)

    _logger = logging.getLogger()
    _logger.setLevel(logging.DEBUG)
    _logger.addFilter(LogFilter())
    _logger.addHandler(ch)
    return _logger


logger = _get_logger()

