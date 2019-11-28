import click

from . import run_server
from . import upload_thought


@click.group()
def cli():
    pass


@cli.command()
@click.argument('address')
@click.argument('data')
def run(address, data):
    ip, port_str = address.split(':')
    address = (ip, int(port_str))
    run_server(address, data)
    print('done')


@cli.command()
@click.argument('address')
@click.argument('user')
@click.argument('thought')
def upload(address, user, thought):
    user_id = int(user)
    ip, port_str = address.split(':')
    address = (ip, int(port_str))
    upload_thought(address, user_id, thought)
    print('done')


if __name__ == '__main__':
    cli()