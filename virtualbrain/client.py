import socket
import struct
import datetime

from .thought import Thought
from .cli import CommandLineInterface
from .utils import Connection


cli = CommandLineInterface()


def upload_thought(address, user_id, thought):
    thought_obj = Thought(user_id=user_id, timestamp=datetime.datetime.now(), thought=thought)
    with Connection.connect(host=address[0], port=address[1]) as connection:
        connection.send(thought_obj.serialize())


@cli.command
def upload(address, user, thought):
    user_id = int(user)
    ip, port_str = address.split(':')
    address = (ip, int(port_str))
    upload_thought(address, user_id, thought)
    print('done')
        

if __name__ == '__main__':
    cli.main()
