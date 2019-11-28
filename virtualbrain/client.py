import socket
import struct
import datetime

from .thought import Thought
from .utils import Connection


def upload_thought(address, user_id, thought):
    thought_obj = Thought(user_id=user_id, timestamp=datetime.datetime.now(), thought=thought)
    with Connection.connect(host=address[0], port=address[1]) as connection:
        connection.send(thought_obj.serialize())
