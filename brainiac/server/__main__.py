from . import run_server as _run_server

import click


@click.group()
def cli():
    pass


@cli.command(help='Run the server')
@click.option('-h', '--host', type=str, default="127.0.0.1",
              help='Server\'s host address')
@click.option('-p', '--port', type=int, default=1337, help='Server\'s listening port')
@click.argument('data-dir')
def run_server(host, port, data_dir):
    _run_server(host, port, data_dir)


if __name__ == '__main__':
    cli()
