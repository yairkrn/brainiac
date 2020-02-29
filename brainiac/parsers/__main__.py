import click

from . import run_parser, run_parser_service


@click.group()
def cli():
    pass


@cli.command(help='Parse raw snapshot')
@click.argument('parser-name')
@click.argument('snapshot-path')
def parse(parser_name, snapshot_path):
    data = open(snapshot_path).read()
    parse_result = run_parser(parser_name, data)
    print(parse_result)


@cli.command(help='Run parser as a service with message queue')
@click.argument('parser-name')
@click.argument('mq-url')
def run_parser(parser_name, mq_url):
    run_parser_service(parser_name, mq_url)


if __name__ == '__main__':
    cli()
