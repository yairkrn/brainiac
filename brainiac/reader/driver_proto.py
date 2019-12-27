import datetime as dt
import gzip
import os
import struct

from .proto import sample_pb2 as proto
from .types import *


class ProtoDriver:
    SCHEME = 'proto://'
    _SIZE_STRUCT = '<I'
    _MILLISECONDS_IN_SECOND = 1000
    _GENDER_INT_TO_BYTE = {
        0: b'm',
        1: b'f',
        2: b'o'
    }

    def __init__(self, url):
        path = url[len(self.SCHEME):]
        self._sample_stream = gzip.open(path, 'rb')
        user_proto = self._read_obj(proto.User)
        self.user = UserInformation(
            user_proto.user_id,
            user_proto.username,
            dt.datetime.fromtimestamp(user_proto.birthday),
            self._GENDER_INT_TO_BYTE[user_proto.gender]
        )
        self._file_size = os.fstat(self._sample_stream.fileno()).st_size

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
        return self._sample_stream.tell() == self._file_size

    def _proto_to_snapshot(self, proto_obj):
        timestamp = dt.datetime.fromtimestamp(proto_obj.datetime / self._MILLISECONDS_IN_SECOND)
        translation = Translation(
            proto_obj.pose.translation.x,
            proto_obj.pose.translation.y,
            proto_obj.pose.translation.z
        )
        rotation = Rotation(
            proto_obj.pose.rotation.x,
            proto_obj.pose.rotation.y,
            proto_obj.pose.rotation.z,
            proto_obj.pose.rotation.w
        )
        color_image = ColorImage(
            proto_obj.color_image.height,
            proto_obj.color_image.width,
            proto_obj.color_image.data
        )
        depth_image = DepthImage(
            proto_obj.depth_image.height,
            proto_obj.depth_image.width,
            proto_obj.depth_image.data
        )
        feelings = Feelings(
            proto_obj.feelings.hunger,
            proto_obj.feelings.thirst,
            proto_obj.feelings.exhaustion,
            proto_obj.feelings.happiness
        )
        return Snapshot(
            timestamp,
            translation,
            rotation,
            color_image,
            depth_image,
            feelings
        )

    def __iter__(self):
        while not self._is_eof():
            yield self._proto_to_snapshot(self._read_obj(proto.Snapshot))
