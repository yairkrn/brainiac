import datetime as dt
import struct

from .proto import sample_pb2 as proto
from .data_types import *


class ProtoDriver:
    SCHEME = 'proto'
    _SIZE_STRUCT = '<I'
    _MILLISECONDS_IN_SECOND = 1000
    _GENDER_INT_TO_STR = {
        0: 'male',
        1: 'female',
        2: 'other'
    }

    def __init__(self, url, open_function):
        path = url.host
        self._sample_stream = open_function(path, 'rb')
        user_proto = self._read_obj(proto.User)
        self.user = ReaderUserInformation(
            user_proto.user_id,
            user_proto.username,
            dt.datetime.fromtimestamp(user_proto.birthday),
            self._GENDER_INT_TO_STR[user_proto.gender]
        )

    def _read_size(self):
        size_bytes = \
            self._sample_stream.read(struct.calcsize(self._SIZE_STRUCT))
        return struct.unpack(self._SIZE_STRUCT, size_bytes)[0]

    def _read_obj(self, obj_cls):
        obj_size = self._read_size()
        obj = obj_cls()
        obj_str = self._sample_stream.read(obj_size)
        obj.ParseFromString(obj_str)
        return obj

    def _is_eof(self):
        is_eof = not self._sample_stream.read(1)
        self._sample_stream.seek(-1, 1)
        return is_eof

    @classmethod
    def _reader_snapshot_from_proto(cls, snapshot):
        timestamp = dt.datetime.fromtimestamp(snapshot.datetime / cls._MILLISECONDS_IN_SECOND)
        translation = ReaderTranslation(
            snapshot.pose.translation.x,
            snapshot.pose.translation.y,
            snapshot.pose.translation.z
        )
        rotation = ReaderRotation(
            snapshot.pose.rotation.x,
            snapshot.pose.rotation.y,
            snapshot.pose.rotation.z,
            snapshot.pose.rotation.w
        )
        color_image = ReaderColorImage(
            snapshot.color_image.height,
            snapshot.color_image.width,
            snapshot.color_image.data
        )
        depth_image = ReaderDepthimage(
            snapshot.depth_image.height,
            snapshot.depth_image.width,
            snapshot.depth_image.data
        )
        feelings = ReaderFeelings(
            snapshot.feelings.hunger,
            snapshot.feelings.thirst,
            snapshot.feelings.exhaustion,
            snapshot.feelings.happiness
        )
        return ReaderSnapshot(
            timestamp,
            translation,
            rotation,
            color_image,
            depth_image,
            feelings
        )

    def __iter__(self):
        while not self._is_eof():
            yield self._reader_snapshot_from_proto(self._read_obj(proto.Snapshot))
