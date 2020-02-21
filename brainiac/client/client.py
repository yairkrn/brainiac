from brainiac import protocol
from brainiac.protocol import HelloMessage, ConfigMessage
from brainiac.reader import Reader
from brainiac.utils import Connection


def upload_sample(host, port, path):
    reader = Reader(path)

    for i, sample in enumerate(reader):
        connection = Connection.connect(host=host, port=port)

        with connection:
            # Follow the protocol:

            # i.    Send an Hello message
            hello = HelloMessage.build(
                dict(user_id=reader.user.user_id,
                     username=reader.user.username,
                     birthday=reader.user.birthday,
                     gender=reader.user.gender)
            )
            connection.send_message(hello)

            # ii.   Receive a Config message
            config = ConfigMessage.parse(connection.receive_message())

            # ii.   Send a Snapshot message
            supported_fields = config.supported_fields
            snapshot = protocol.build_snapshot_message_from_sample(sample, supported_fields)
            connection.send_message(snapshot)
