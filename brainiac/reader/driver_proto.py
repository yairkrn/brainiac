import datetime as dt
import gzip
import os
import struct

from .proto import sample_pb2 as proto


class UserInformation:
    @staticmethod
    def __get_gender_string(value):
        return proto._USER_GENDER.values_by_number(value).name.lower()

    def __init__(self, user_information_proto):
        self.user_id = user_information_proto.user_id
        self.username = user_information_proto.username
        self.birthday = dt.datetime.fromtimestamp(user_information_proto.birthday)
        self.gender = user_information_proto.gender

    def __str__(self):
        return f'user {self.user_id}: {self.username}, born {self.birthday}' + \
               f' ({self.__get_gender_string(self.gender)})'


class ColorImage:
    def __init__(self, color_image_proto):
        self.h = color_image_proto.height
        self.w = color_image_proto.width
        self.colors = color_image_proto.data


class DepthImage:
    def __init__(self, depth_image_proto):
        self.h = depth_image_proto.height
        self.w = depth_image_proto.width
        self.depths = depth_image_proto.data


class Translation:
    def __init__(self, translation_proto):
        self.x = translation_proto.x
        self.y = translation_proto.y
        self.z = translation_proto.z

    def __str__(self):
        return repr((self.x, self.y, self.z))


class Rotation:
    def __init__(self, rotation_proto):
        self.x = rotation_proto.x
        self.y = rotation_proto.y
        self.z = rotation_proto.z
        self.w = rotation_proto.w

    def __str__(self):
        return repr((self.x, self.y, self.z, self.w))


class Feelings:
    def __init__(self, feelings_proto):
        self.hunger = feelings_proto.hunger
        self.thirst = feelings_proto.thirst
        self.exhaustion = feelings_proto.exhaustion
        self.happiness = feelings_proto.happiness


class Snapshot:
    _MILLISECONDS_IN_SECOND = 1000

    def __init__(self, snapshot_proto):
        self.timestamp = dt.datetime.fromtimestamp(snapshot_proto.datetime / self._MILLISECONDS_IN_SECOND)
        self.translation = Translation(snapshot_proto.pose.translation)
        self.rotation = Rotation(snapshot_proto.pose.rotation)
        self.color_image = ColorImage(snapshot_proto.color_image)
        self.depth_image = DepthImage(snapshot_proto.depth_image)
        self.feelings = Feelings(snapshot_proto.feelings)

    def __str__(self):
        return f'Snapshot from {self.timestamp} on {self.translation} / ' + \
               f'{self.rotation} with a {self.color_image.w}x' + \
               f'{self.color_image.h} color image and a ' + \
               f'{self.depth_image.w}x{self.depth_image.h} depth ' + \
               f'image.'


class ProtoDriver:
    SCHEME = 'proto://'
    _SIZE_STRUCT = '<I'

    def __init__(self, url):
        path = url[len(self.SCHEME):]
        self._sample_stream = gzip.open(path, 'rb')
        self.user = UserInformation(self._read_obj(proto.User))
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

    def __iter__(self):
        while not self._is_eof():
            yield Snapshot(self._read_obj(proto.Snapshot))
