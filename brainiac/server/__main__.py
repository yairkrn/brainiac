from . import run_server as _run_server
from ..config import config
from ..message_queue import MessageQueue

import click


@click.group()
def cli():
    pass


@cli.command(help='Run the server')
@click.option('-h', '--host', type=str, default="127.0.0.1",
              help='Server\'s host address')
@click.option('-p', '--port', type=int, default=1337, help='Server\'s listening port')
@click.argument('url')
def run_server(host, port, url):
    def publish(message):
        MessageQueue(url).publish(message, config['parsers-message-queue'])
    _run_server(host, port, publish)


if __name__ == '__main__':
    cli()
