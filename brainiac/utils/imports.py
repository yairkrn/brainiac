import importlib
import inspect
import os
import pathlib
import re

FILE_SEP = os.path.sep
PACK_SEP = '.'


def _replace_separators(s, src, dst):
    return dst.join(s.split(src))


def import_by_glob(package, glob):
    package_path = pathlib.Path(_replace_separators(package, PACK_SEP, FILE_SEP))
    module_paths = package_path.glob(glob)
    modules = []
    for module_path in module_paths:
        module_relative_path = module_path.relative_to(package_path)
        module_relative_name = _replace_separators(str(module_relative_path.parent / module_relative_path.stem),
                                                   FILE_SEP, PACK_SEP)
        modules.append(importlib.import_module(PACK_SEP + module_relative_name, package))
    return modules


def get_class_by_regex(module, pattern, flags=0):
    classes = []
    for name, item in module.__dict__.items():
        if re.match(pattern, name, flags):
            if inspect.isclass(item):
                classes.append(item)
    return classes
