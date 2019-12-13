import contextlib
import pathlib
import threading

from .parser import parser
from .protocol import HelloMessage, ConfigMessage, SnapshotMessage
from .utils import Listener


BACKLOG = 1000


class ClientHandler(threading.Thread):
    TIME_FORMAT = '%Y-%m-%d_%H-%M-%S-%f'
    lock = threading.Lock()

    class Context:
        def __init__(self, directory):
            self.directory = directory

    def __init__(self, conn, data_dir):
        super().__init__()
        self._conn = conn
        self._data_dir = data_dir

    def _get_user_dir(self, user_id, timestamp):
        formatted_time = timestamp.strftime(self.TIME_FORMAT)
        user_dir = self._data_dir / str(user_id) / formatted_time
        user_dir.mkdir(parents=True, exist_ok=True)
        return user_dir

    def run(self):
        # Follow the protocol:

        # i.    Receive an Hello message
        hello = HelloMessage.deserialize(self._conn.receive_message())

        # ii.   Send back a Config message
        self._conn.send_message(ConfigMessage(
            supported_fields_number=len(parser.supported_fields),
            supported_fields=parser.supported_fields).serialize())

        # iii.  Receive a Snapshot message
        snapshot = SnapshotMessage.deserialize(self._conn.receive_message())

        # Parse the snapshot.
        context = self.Context(
            self._get_user_dir(hello.user_id, snapshot.timestamp))
        parser.parse(context, snapshot)


def run_server(address, data_dir):
    """
    Initiate a server, running at given address
        and handling incoming connecitons.

    Args:
        address ((str, int)): the ip address and port to listen on.
        data_dir (str): a directory path in which to save clients' data.
    """
    data_dir = pathlib.Path(data_dir)
    with Listener(host=address[0], port=address[1]) as listener:
        with contextlib.suppress(KeyboardInterrupt):
            while True:
                client_connection = listener.accept()
                ClientHandler(client_connection, data_dir).start()
