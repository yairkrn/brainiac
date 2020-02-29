from ..config import config
from ..message_queue.data_types import ServerParsersMessage
from ..message_queue import MessageQueue
from .parser import run_parser


def run_parser_service(parser_name, mq_url):
    message_queue = MessageQueue(mq_url,
                                 tag=config['message-queue-parsers-tag'],
                                 message_type=ServerParsersMessage)

    def _consume_callback(message):
        snapshot_path = message.snapshot_path
        raw_snapshot = open(snapshot_path, 'rb').read()
        print(run_parser(parser_name, raw_snapshot))

    message_queue.consume(_consume_callback)
