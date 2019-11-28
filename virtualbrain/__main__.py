from . import run_server
from . import upload_thought
from .cli import CommandLineInterface


cli = CommandLineInterface()


@cli.command
def run(address, data):
    ip, port_str = address.split(':')
    address = (ip, int(port_str))
    run_server(address, data)
    print('done')


@cli.command
def upload(address, user, thought):
    user_id = int(user)
    ip, port_str = address.split(':')
    address = (ip, int(port_str))
    upload_thought(address, user_id, thought)
    print('done')


if __name__ == '__main__':
    cli.main()
