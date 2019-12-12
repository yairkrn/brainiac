import click

from . import Reader
from . import run_server as _run_server
from . import run_webserver as _run_webserver
from . import upload_thought as _upload_thought
from . import run_client as _run_client


@click.group()
def cli():
    pass


@cli.command(help='Upload a thought to the thought server.')
@click.option('-a', '--address', required=True,
              help='The server\'s address, in format <ip>:<port>')
@click.option('-u', '--user-id', type=int, required=True,
              help='The user\'s unique identifying number')
@click.argument('thought')
def upload_thought(address, user_id, thought):
    ip, port_str = address.split(':')
    address = (ip, int(port_str))
    _upload_thought(address, user_id, thought)
    print('done')


@cli.command(help='Run the thought server, which accepts and stores thoughts.')
@click.option('-a', '--address', required=True,
              help='The server\'s address, in format <ip>:<port>')
@click.argument('data-dir')
def run_server(address, data_dir):
    ip, port_str = address.split(':')
    address = (ip, int(port_str))
    _run_server(address, data_dir)
    print('done')


@cli.command(help='Run the web server, which keeps track of stored thoughts.')
@click.option('-a', '--address', required=True,
              help='The server\'s address, in format <ip>:<port>')
@click.argument('data-dir')
def run_webserver(address, data_dir):
    ip, port_str = address.split(':')
    address = (ip, int(port_str))
    _run_webserver(address, data_dir)
    print('done')


@cli.command(help='Print sample of user information and cognition snapshots.')
@click.option('-n', '--sample-number', required=False, default=3, type=int,
              help='Number of sample to print.')
@click.argument('sample-file')
def read(sample_file, sample_number):
    reader = Reader(sample_file)
    print(reader.userinfo)

    for snapshot in reader:
        print(snapshot)
        sample_number -= 1
        if sample_number <= 0:
            break

    print('done')


@cli.command(help='Print sample of user information and cognition snapshots.')
@click.option('-a', '--address', required=True,
              help='The server\'s address, in format <ip>:<port>')
@click.option('-n', '--sample-number', required=False, default=3, type=int,
              help='Number of sample to print.')
@click.argument('sample-file')
def run_client(address, sample_file, sample_number):
    ip, port_str = address.split(':')
    address = (ip, int(port_str))
    _run_client(address, sample_file, sample_number)
    print('done')


if __name__ == '__main__':
    cli()
