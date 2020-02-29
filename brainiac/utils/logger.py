import logging
import inspect
import sys


_FORMAT = ("[%(asctime)s] [%(levelname)-8s] --- %(message)s (%(name)s)", "%Y-%m-%d %H:%M:%S")


def _get_caller_package():
    # determine name based on caller module
    for frm in inspect.stack():
        mod = inspect.getmodule(frm[0])
        if mod.__package__ not in [logging.__package__, __package__]:
            return mod.__package__


def get_logger(name=None):
    if name is None:
        name = _get_caller_package()

    # create console handler with a higher log level
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)

    # create formatter and add it to the handlers
    formatter = logging.Formatter(*_FORMAT)
    ch.setFormatter(formatter)

    _logger = logging.getLogger(name)
    _logger.setLevel(logging.DEBUG)
    _logger.addHandler(ch)
    return _logger
