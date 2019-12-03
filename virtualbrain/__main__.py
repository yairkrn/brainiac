import click

from . import run_server as _run_server
from . import upload_thought as _upload_thought
from . import run_webserver as _run_webserver


@click.group()
def cli():
    pass


@cli.command()
@click.option('-a', '--address', required=True)
@click.option('-u', '--user-id', type=int, required=True)
@click.argument('thought')
def upload_thought(address, user_id, thought):
    ip, port_str = address.split(':')
    address = (ip, int(port_str))
    _upload_thought(address, user_id, thought)
    print('done')


@cli.command()
@click.option('-a', '--address', required=True)
@click.argument('data')
def run_server(address, data):
    ip, port_str = address.split(':')
    address = (ip, int(port_str))
    _run_server(address, data)
    print('done')


@cli.command()
@click.option('-a', '--address', required=True)
@click.argument('data')
def run_webserver(address, data):
    ip, port_str = address.split(':')
    address = (ip, int(port_str))
    _run_webserver(address, data)
    print('done')


if __name__ == '__main__':
    cli()
