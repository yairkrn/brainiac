import importlib
import inspect
import pathlib


class Parser:
    _PARSERS_DIR = 'parsers'
    _PARSERS_SUBPACKAGE = f'.{_PARSERS_DIR}'
    _PARSER_FUNCTION_PREFIX = 'parse'
    _PARSER_CLASS_SUFFIX = 'Parser'
    _PARSER_FIELD_ATTRIBUTE = 'field'

    def __init__(self):
        self._function_parsers = []
        self._class_parsers = []
        self._collect_parsers()

    def _collect_parsers(self):
        # Iterate all modules in the parsers subpackage
        current_path = pathlib.Path(__file__).parent
        parsers_path = current_path / self._PARSERS_DIR
        for module_path in parsers_path.glob('[!_]*.py'):
            parser_module = self._import_parser_module(module_path.stem)

            # Collect function and class parsers in module
            self._function_parsers.extend(self._get_function_parsers(parser_module))
            self._class_parsers.extend(self._get_class_parsers(parser_module))

    def _import_parser_module(self, module_name):
        # Remove this module's name to obtain the package
        current_package = '.'.join(__name__.split('.')[:-1])
        return importlib.import_module(f'{self._PARSERS_SUBPACKAGE}.'
                                       f'{module_name}',
                                       package=current_package)

    def _get_function_parsers(self, module):
        parsers = []
        for name, item in module.__dict__.items():
            if not inspect.isfunction(item):
                continue
            if not name.startswith(self._PARSER_FUNCTION_PREFIX):
                continue
            if self._PARSER_FIELD_ATTRIBUTE not in item.__dict__:
                continue
            parsers.append(item)
        return parsers

    def _get_class_parsers(self, module):
        parsers = []
        for name, item in module.__dict__.items():
            if not inspect.isclass(item):
                continue
            if not name.endswith(self._PARSER_CLASS_SUFFIX):
                continue
            if self._PARSER_FIELD_ATTRIBUTE not in item.__dict__:
                continue
            parsers.append(item())
        return parsers

    @property
    def supported_fields(self):
        return [_parser.field for _parser in
                self._function_parsers + self._class_parsers]

    def parse(self, context, snapshot):
        for function_parser in self._function_parsers:
            function_parser(context, snapshot)
        for class_parser in self._class_parsers:
            class_parser.parse(context, snapshot)


parser = Parser()
