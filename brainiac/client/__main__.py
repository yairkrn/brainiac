from . import upload_sample as _upload_sample
from .. import Reader
from ..utils import logger
import click


@click.group()
def cli():
    pass


@cli.command(help='Print sample metadata')
@click.argument('sample-path')
def read_sample(sample_path):
    logger.info(f'reading sample at: {sample_path}')
    reader = Reader(sample_path)
    logger.info(reader.user)
    for sample in reader:
        logger.info(sample)


@cli.command(help='Upload sample to server')
@click.option('-h', '--host', type=str, default="127.0.0.1",
              help='Server\'s host address')
@click.option('-p', '--port', type=int, default=1337, help='Server\'s listening port')
@click.argument('sample-path')
def upload_sample(host, port, sample_path):
    logger.info(f'uploading sample at "{sample_path}" to "{host}:{port}"')
    _upload_sample(host, port, sample_path)


if __name__ == '__main__':
    cli()
