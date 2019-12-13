import os

import construct as cs

from .utils import serializable
from .utils.serializable import ByteAdapter, DateAdapter, \
                                DatetimeMillisecondsAdapter


@serializable(cs.Struct('gender' / ByteAdapter(cs.Byte)))
class Gender:
    _TO_STRING = {
        'm': 'male',
        'f': 'female',
        'o': 'other'
    }

    def __init__(self, gender):
        self.gender = gender
        # TODO: check if does not exist.
        self._gender_str = self._TO_STRING[gender]

    def __str__(self):
        return self._gender_str


@serializable(cs.Struct(
    'user_id' / cs.Int64ul,
    'username' / cs.PascalString(cs.Int32ul, "ascii"),
    'birthday' / DateAdapter(cs.Int32ul),
    'gender' / Gender.struct))
class UserInformation:
    def __init__(self, user_id, username, birthday, gender):
        self.user_id = user_id
        self.username = username
        self.birthday = birthday
        self.gender = gender

    def __str__(self):
        return f'user {self.user_id}: {self.username}, born {self.birthday}' +\
               f' ({self.gender})'


@serializable(cs.Struct(
    'h' / cs.Int32ul,
    'w' / cs.Int32ul,
    'colors' / cs.Array(lambda ctx: ctx.w * ctx.h * 3, cs.Byte)))
class ColorImage:
    def __init__(self, h, w, colors):
        self.h = h
        self.w = w
        rgb_colors = []
        for i in range(0, len(colors), 3):
            b, g, r = colors[i:i+3]
            rgb_colors.extend([r, g, b])
        self.colors = rgb_colors


@serializable(cs.Struct(
    'h' / cs.Int32ul,
    'w' / cs.Int32ul,
    'depths' / cs.Array(lambda ctx: ctx.w * ctx.h, cs.Float32l)))
class DepthImage:
    def __init__(self, h, w, depths):
        self.h = h
        self.w = w
        self.depths = depths


@serializable(cs.Struct(
    'x' / cs.Float64l,
    'y' / cs.Float64l,
    'z' / cs.Float64l))
class Translation:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return repr((self.x, self.y, self.z))


@serializable(cs.Struct(
    'x' / cs.Float64l,
    'y' / cs.Float64l,
    'z' / cs.Float64l,
    'w' / cs.Float64l))
class Rotation:
    def __init__(self, x, y, z, w):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def __str__(self):
        return repr((self.x, self.y, self.z, self.w))


@serializable(cs.Struct(
    'hunger' / cs.Float32l,
    'thirst' / cs.Float32l,
    'exhaustion' / cs.Float32l,
    'happiness' / cs.Float32l))
class Feelings:
    def __init__(self, hunger, thirst, exhaustion, happiness):
        self.hunger = hunger
        self.thirst = thirst
        self.exhaustion = exhaustion
        self.happiness = happiness


@serializable(cs.Struct(
    'timestamp' / DatetimeMillisecondsAdapter(cs.Int64ul),
    'translation' / Translation.struct,
    'rotation' / Rotation.struct,
    'color_image' / ColorImage.struct,
    'depth_image' / DepthImage.struct,
    'feelings' / Feelings.struct))
class Snapshot:
    def __init__(self, timestamp, translation, rotation, color_image,
                 depth_image, feelings):
        self.timestamp = timestamp
        self.translation = translation
        self.rotation = rotation
        self.color_image = color_image
        self.depth_image = depth_image
        self.feelings = feelings

    def __str__(self):
        return f'Snapshot from {self.timestamp} on {self.translation} / ' + \
               f'{self.rotation} with a {self.color_image.w}x' + \
               f'{self.color_image.h} color image and a ' + \
               f'{self.depth_image.w}x{self.depth_image.h} depth ' + \
               f'image.'


class Reader:
    def __init__(self, path):
        self._sample_stream = open(path, 'rb')
        self.userinfo = UserInformation.deserialize_stream(
                            self._sample_stream)
        self._file_size = os.fstat(self._sample_stream.fileno()).st_size

    def _is_eof(self):
        return self._sample_stream.tell() == self._file_size

    def __iter__(self):
        while not self._is_eof():
            yield Snapshot.deserialize_stream(self._sample_stream)
