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
class HelloMessage:
    def __init__(self, user_id, username, birthday, gender):
        self.user_id = user_id
        self.username = username
        self.birthday = birthday
        self.gender = gender


@serializable(cs.Struct(
    'h' / cs.Int32ul,
    'w' / cs.Int32ul,
    'colors' / cs.Array(lambda ctx: ctx.w * ctx.h, cs.Float32l)))
class ColorImage:
    def __init__(self, h, w, colors):
        self.h = h
        self.w = w
        self.colors = colors


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
class SnapshotMessage:
    def __init__(self, timestamp, translation=None, rotation=None,
                 color_image=None, depth_image=None, feelings=None):
        self.timestamp = timestamp
        if translation is None:
            translation = Translation(0, 0, 0)
        if rotation is None:
            rotation = Rotation(0, 0, 0, 0)
        if color_image is None:
            color_image = ColorImage(0, 0, [])
        if depth_image is None:
            depth_image = DepthImage(0, 0, [])
        if feelings is None:
            feelings = Feelings(0, 0, 0, 0)

        self.translation = translation
        self.rotation = rotation
        self.color_image = color_image
        self.depth_image = depth_image
        self.feelings = feelings

    @classmethod
    def from_sample(cls, sample, fields):
        print(fields)
        timestamp = sample.timestamp
        translation = None
        if 'translation' in fields:
            translation = Translation(
                sample.translation.x,
                sample.translation.y,
                sample.translation.z)
        rotation = None
        if 'rotation' in fields:
            rotation = Rotation(
                sample.rotation.x,
                sample.rotation.y,
                sample.rotation.z,
                sample.rotation.w)
        color_image = None
        if 'color_image' in fields:
            color_image = ColorImage(
                sample.color_image.h,
                sample.color_image.w,
                sample.color_image.colors)
        depth_image = None
        if 'depth_image' in fields:
            depth_image = DepthImage(
                sample.depth_image.h,
                sample.depth_image.w,
                sample.depth_image.depth)
        feelings = None
        if 'feelings' in fields:
            feelings = Feelings(
                sample.feelings.hunger,
                sample.feelings.thirst,
                sample.feelings.exhaustion,
                sample.feelings.happiness)
        return cls(
            timestamp,
            translation,
            rotation,
            color_image,
            depth_image,
            feelings)


@serializable(cs.Struct(
    'supported_fields_number' / cs.Int32ul,
    'supported_fields' / cs.Array(lambda ctx: ctx.supported_fields_number,
                                  cs.PascalString(cs.Int32ul, "ascii"))
    ))
class ConfigMessage:
    def __init__(self, supported_fields_number, supported_fields):
        self.supported_fields_number = supported_fields_number
        self.supported_fields = supported_fields

