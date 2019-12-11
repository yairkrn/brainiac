import datetime as dt
import os

import construct as cs


def struct(cs_struct):
    def wrapper(cls):
        class Adapter(cs.Adapter):
            def _decode(self, obj, context, path):
                values = {}
                for subcon in cs_struct.subcons:
                    key = subcon.name
                    if not key.startswith('_'):
                        values[key] = obj[key]
                return cls(**values)

            def _encode(self, obj, context, path):
                return cs_struct.build(obj.__dict__)

            def __call__(self, *args, **kwargs):
                print(args, kwargs)
                return cls(*args, **kwargs)
        return Adapter(cs_struct)
    return wrapper


class DateAdapter(cs.Adapter):
    def _decode(self, obj, context, path):
        return dt.datetime.fromtimestamp(obj)

    def _encode(self, obj, context, path):
        return obj.timestamp()


class DatetimeMillisecondsAdapter(cs.Adapter):
    _MILLISECONDS_IN_SECOND = 1000

    def _decode(self, obj, context, path):
        return dt.datetime.fromtimestamp(obj / self._MILLISECONDS_IN_SECOND)

    def _encode(self, obj, context, path):
        return obj.timestamp() * self._MILLISECONDS_IN_SECOND


@struct(cs.Struct('gender' / cs.Byte))
class Gender:
    _TO_STRING = {
        ord('m'): 'male',
        ord('f'): 'female',
        ord('o'): 'other'
    }

    def __init__(self, gender):
        self.gender = gender
        # TODO: check if does not exist.
        self._gender_str = self._TO_STRING[gender]

    def __str__(self):
        return self._gender_str


@struct(cs.Struct(
    'user_id' / cs.Int64ul,
    'username' / cs.PascalString(cs.Int32ul, "ascii"),
    'birthday' / DateAdapter(cs.Int32ul),
    'gender' / Gender))
class UserInformation:
    def __init__(self, user_id, username, birthday, gender):
        self.user_id = user_id
        self.username = username
        self.birthday = birthday
        self.gender = gender

    def __str__(self):
        return f'user {self.user_id}: {self.username}, born {self.birthday}' +\
               f' ({self.gender})'


@struct(cs.Struct(
    'h' / cs.Int32ul,
    'w' / cs.Int32ul,
    'colors' / cs.Array(lambda ctx: ctx.w * ctx.h * 3, cs.Byte)))
class ColorImage:
    def __init__(self, h, w, colors):
        self.h = h
        self.w = w
        self.colors = colors


@struct(cs.Struct(
    'h' / cs.Int32ul,
    'w' / cs.Int32ul,
    'depths' / cs.Array(lambda ctx: ctx.w * ctx.h, cs.Float32l)))
class DepthImage:
    def __init__(self, h, w, depths):
        self.h = h
        self.w = w
        self.depths = depths


@struct(cs.Struct(
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


@struct(cs.Struct(
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


@struct(cs.Struct(
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


@struct(cs.Struct(
    'timestamp' / DatetimeMillisecondsAdapter(cs.Int64ul),
    'translation' / Translation,
    'rotation' / Rotation,
    'color_image' / ColorImage,
    'depth_image' / DepthImage,
    'feelings' / Feelings))
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
        self.userinfo = UserInformation.parse_stream(
                            self._sample_stream)
        self._file_size = os.fstat(self._sample_stream.fileno()).st_size

    def _is_eof(self):
        return self._sample_stream.tell() == self._file_size

    def __iter__(self):
        while not self._is_eof():
            yield Snapshot.parse_stream(self._sample_stream)
