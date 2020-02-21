import click

from .reader.reader import Reader
from .server import run_server as _run_server
from .client import upload_sample as _upload_sample
from .web import run_webserver as _run_weserver


@click.group()
def cli():
    pass


@cli.group(help='Client related utilities')
def client():
    pass


@client.command(help='Print sample metadata')
@click.argument('sample-path')
def read_sample(sample_path):
    reader = Reader(sample_path)
    print(reader.user)
    for sample in reader:
        print(sample)


@client.command(help='Upload sample to server')
@click.option('-h', '--host', type=str, default="127.0.0.1",
              help='Server\'s host address')
@click.option('-p', '--port', type=int, default=1337, help='Server\'s listening port')
@click.argument('sample-path')
def upload_sample(host, port, sample_path):
    _upload_sample(host, port, sample_path)


@cli.group(help='Server related utilities.')
def server():
    pass


@server.command(help='Run the thought server, which accepts and stores thoughts.')
@click.option('-a', '--address', type=(str, int), default=('127.0.0.1', 1337),
              help='The server\'s address, in format <ip>:<port>')
@click.argument('data-dir')
def run(address, data_dir):
    _run_server(address, data_dir)


@server.command(help='Run the web server, which keeps track of stored thoughts.')
@click.option('-a', '--address', type=(str, int), default=('127.0.0.1', 1337),
              help='The server\'s address, in format <ip>:<port>')
@click.argument('data-dir')
def webserver(address, data_dir):
    _run_webserver(address, data_dir)


if __name__ == '__main__':
    cli()
