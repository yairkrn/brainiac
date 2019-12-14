import datetime as dt

from .thought import Thought
from .reader import Reader
from .utils import Connection
from .protocol import HelloMessage, ConfigMessage, SnapshotMessage


def upload_thought(address, user_id, thought):
    """
    Send a Thought object to a given server address.

    Args:
        address ((str, int)): host/ip server address and port.
        user_id (int): the user sending the data.
        thought (Thought): the Thought object to send to server.
    """
    thought_obj = Thought(user_id=user_id,
                          timestamp=dt.datetime.now(),
                          thought=thought)
    with Connection.connect(host=address[0], port=address[1]) as connection:
        connection.send(thought_obj.serialize())


def run_client(address, sample_path, sample_num):
    """
    Send a Thought object to a given server address.

    Args:
        address ((str, int)): host/ip server address and port.
        sample_path (Path): a snapshot to process and upload to server.
        sample_num (int): number of samples to read.
    """
    reader = Reader(sample_path)

    for i, sample in enumerate(reader):
        if sample_num is not None and i >= sample_num:
            return

        connection = Connection.connect(host=address[0], port=address[1])

        with connection:
            # Follow the protocol:

            # i.    Send an Hello message
            hello = HelloMessage(user_id=reader.user.user_id,
                                 username=reader.user.username,
                                 birthday=reader.user.birthday,
                                 gender=reader.user.gender)
            connection.send_message(hello.serialize())

            # ii.   Receive a Config message
            config = ConfigMessage.deserialize(connection.receive_message())

            # ii.   Send a Snapshot message
            snapshot = SnapshotMessage.from_sample(
                sample, config.supported_fields)
            connection.send_message(snapshot.serialize())
