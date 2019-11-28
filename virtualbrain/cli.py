import functools
import inspect
import sys


class CommandLineInterface:

    def __init__(self):
        self._functions = {}

    def command(self, f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            return f(*args, **kwargs)
        self._functions[f.__name__] = f
        return wrapper

    @staticmethod
    def _print_usage():
        print(f'USAGE: python {sys.argv[0]} <command> [<key>=<value>]*')

    @staticmethod
    def _inspect_function(f):
        args_spec = inspect.getfullargspec(f)

        args = args_spec.args
        defaults = args_spec.defaults
        required_args = set(args[:-len(defaults)] if defaults else args)
        optional_args = set(args[-len(defaults):] if defaults else [])

        kwonlyargs = set(args_spec.kwonlyargs)
        kwonlydefaults = set(args_spec.kwonlydefaults) if args_spec.kwonlydefaults else set()
        required_args.update(kwonlyargs - kwonlydefaults)
        optional_args.update(kwonlydefaults)

        kwargs_exists = args_spec.varkw is not None

        return required_args, optional_args, kwargs_exists

    @staticmethod
    def _validate_call(f, input_args):
        required_args, optional_args, kwargs_exists = CommandLineInterface._inspect_function(f)

        # Check for missing required arguments.
        if not required_args.issubset(input_args):
            missing_required_args = required_args - input_args
            raise ValueError(f'Missing required arguments: {", ".join(sorted(missing_required_args))}')

        # Check for unexpected arguments.
        extra_input_args = input_args - required_args
        if not extra_input_args.issubset(optional_args) and not kwargs_exists:
            unexpected_input_args = extra_input_args - optional_args
            raise ValueError(f'Unexpected arguments: {", ".join(sorted(unexpected_input_args))}')

    def main(self):
        try:
            command_name, *input_args_str = sys.argv[1:]
            input_args_values = dict(item.split("=") for item in input_args_str)

            command_function = self._functions[command_name]
            self._validate_call(command_function, input_args_values.keys())
            command_function(**input_args_values)

        except BaseException as e:
            print('ERROR:', e, file=sys.stderr)
            self._print_usage()
            sys.exit(1)

        sys.exit(0)