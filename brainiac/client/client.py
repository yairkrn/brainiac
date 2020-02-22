from ..protocol.data_types import ProtocolHello, ProtocolConfig, ProtocolSnapshot
from ..reader import Reader
from ..utils import Connection

_GENDER_STR_TO_BYTE = {
    'male': b'm',
    'female': b'f',
    'other': b'o'
}


def _protocol_hello_from_reader_user(user):
    return ProtocolHello.build(
        dict(user_id=user.user_id,
             username=user.username,
             birthday=user.birthday,
             gender=_GENDER_STR_TO_BYTE[user.gender])
    )


def _protocol_snapshot_from_reader_snapshot(snapshot, fields):
    field_values = {'timestamp': snapshot.timestamp}
    if 'translation' in fields:
        field_values['translation'] = \
            dict(x=snapshot.translation.x,
                 y=snapshot.translation.y,
                 z=snapshot.translation.z)
    if 'rotation' in fields:
        field_values['rotation'] = \
            dict(x=snapshot.rotation.x,
                 y=snapshot.rotation.y,
                 z=snapshot.rotation.z,
                 w=snapshot.rotation.w)
    if 'color_image' in fields:
        field_values['color_image'] = \
            dict(h=snapshot.color_image.h,
                 w=snapshot.color_image.w,
                 colors=snapshot.color_image.colors)
    if 'depth_image' in fields:
        field_values['depth_image'] = \
            dict(h=snapshot.depth_image.h,
                 w=snapshot.depth_image.w,
                 depths=snapshot.depth_image.depths)
    if 'feelings' in fields:
        field_values['feelings'] = \
            dict(hunger=snapshot.feelings.hunger,
                 thirst=snapshot.feelings.thirst,
                 exhaustion=snapshot.feelings.exhaustion,
                 happiness=snapshot.feelings.happiness)
    return ProtocolSnapshot.build(field_values)


def upload_sample(host, port, path):
    reader = Reader(path)

    for reader_snapshot in reader:
        connection = Connection.connect(host=host, port=port)

        with connection:
            # send Hello message
            hello = _protocol_hello_from_reader_user(reader.user)
            connection.send_message(hello)

            # receive config message
            config = ProtocolConfig.parse(connection.receive_message())

            # send snapshot message
            supported_fields = config.supported_fields
            protocol_snapshot = _protocol_snapshot_from_reader_snapshot(reader_snapshot, supported_fields)
            connection.send_message(protocol_snapshot)
