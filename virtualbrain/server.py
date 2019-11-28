import socket
import struct
import time
import datetime
import threading
import os
import contextlib

from .thought import Thought
from .thought import ThoughtHeader
from .utils import Listener


BACKLOG = 1000


class ClientHandler(threading.Thread):
    FILE_EXT = '.txt'
    TIME_FORMAT =  '%Y-%m-%d_%H-%M-%S'
    lock = threading.Lock()

    def __init__(self, conn, data_dir):
        super().__init__()
        self._conn = conn
        self._data_dir = data_dir

    def _get_thought_path(self, user_id, timestamp):
        formatted_time = timestamp.strftime(self.TIME_FORMAT)
        
        output_dir = os.path.join(self._data_dir, str(user_id))
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, formatted_time + self.FILE_EXT)

        return output_path

    def _handle_thought(self, thought_obj):
        output_path = self._get_thought_path(thought_obj.user_id, thought_obj.timestamp)

        self.lock.acquire()

        with open(output_path, "ab") as output_file:
            # Start new line if file not empty.
            if os.path.getsize(output_path) > 0:
                output_file.write(os.linesep.encode())
            output_file.write(thought_obj.thought.encode())

        self.lock.release()

    def _receive_thought(self):
        with self._conn as connection:
            header_bytes = connection.receive(ThoughtHeader.HEADER_SIZE)
            header = ThoughtHeader.deserialize(header_bytes)
            thought_bytes = connection.receive(header.thought_size)
            return Thought.deserialize(header_bytes + thought_bytes)

    def run(self):
        thought_obj = self._receive_thought()
        self._handle_thought(thought_obj)


def run_server(address, data_dir):
    with Listener(host=address[0], port=address[1]) as listener:
        with contextlib.suppress(KeyboardInterrupt):
            while True:
                client_connection = listener.accept()
                ClientHandler(client_connection, data_dir).start()

