import contextlib
import pathlib
import threading

from ..server import data_types
from ..message_queue.data_types import MessageQueueSnapshot
from ..config import config
from ..parser import parser
from ..protocol.data_types import ProtocolHello, ProtocolConfig, ProtocolSnapshot
from ..utils import Listener


class ClientHandler(threading.Thread):
    TIME_FORMAT = '%Y-%m-%d_%H-%M-%S-%f'
    SNAPSHOT_FILENAME = config['server-snapshot-filename']
    lock = threading.Lock()

    class Context:
        def __init__(self, directory):
            self.directory = directory

    def __init__(self, conn, publish):
        super().__init__()
        self._conn = conn
        self._publish = publish
        self._data_dir = pathlib.Path(config['server-local-dir'])

    def _get_user_dir(self, user_id, timestamp):
        formatted_time = timestamp.strftime(self.TIME_FORMAT)
        user_dir = self._data_dir / str(user_id) / formatted_time
        user_dir.mkdir(parents=True, exist_ok=True)
        return user_dir

    def _save_snapshot(self, hello_message, snapshot_message, fields):
        user_dir = self._get_user_dir(hello_message.user_id, snapshot_message.timestamp)
        snapshot_file = user_dir / self.SNAPSHOT_FILENAME
        snapshot = data_types.snapshot_message_to_snapshot(snapshot_message, fields)
        snapshot_file.write_bytes(snapshot)
        return snapshot_file

    def _build_message(self, hello_message, snapshot_message, fields):
        snapshot_path = self._save_snapshot(hello_message, snapshot_message, fields)
        return MessageQueueSnapshot(
            user_id=hello_message.user_id,
            timestamp=snapshot_message.timestamp,
            snapshot_path=str(snapshot_path.absolute())
        )

    def run(self):
        # Follow the protocol:

        # i.    Receive an Hello message
        hello = ProtocolHello.parse(self._conn.receive_message())

        # ii.   Send back a Config message
        self._conn.send_message(
            ProtocolConfig.build(
                dict(supported_fields_number=len(parser.supported_fields),
                     supported_fields=parser.supported_fields)
            )
        )

        # iii.  Receive a Snapshot message
        snapshot_message = ProtocolSnapshot.parse(self._conn.receive_message())
        published_message = self._build_message(hello, snapshot_message, parser.supported_fields)

        # Publish the message
        self._publish(published_message.serialize())

        # TODO: move to parsers microservice
        # Parse the snapshot.
        context = self.Context(
            self._get_user_dir(hello.user_id, snapshot_message.timestamp))
        parser.parse(context, snapshot_message)


def run_server(host, port, publish):
    with Listener(host=host, port=port, backlog=config['server-backlog']) as listener:
        with contextlib.suppress(KeyboardInterrupt):
            while True:
                client_connection = listener.accept()
                ClientHandler(client_connection, publish).start()
