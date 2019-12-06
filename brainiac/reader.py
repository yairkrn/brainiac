import datetime as dt
import os

import construct as cs


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


class DictInitializer:
    def __init__(self, **kwargs):
        """
        Initializes member for every named argument.

        Args:
            **kwargs: a dictionary of named arguments.
        """
        for k, v in kwargs.items():
            self.__dict__[k] = v


class UserInformation(DictInitializer):
    def __str__(self):
        return f'user {self.user_id}: {self.username}, born {self.birthday}' +\
               f' ({self.gender})'


UserInformationParser = cs.ExprAdapter(
    # Struct describing how to parse UserInformation:
    cs.Struct(
        'user_id' / cs.Int64ul,
        'username' / cs.PascalString(cs.Int32ul, "ascii"),
        'birthday' / DateAdapter(cs.Int32ul),
        'gender' / cs.ExprAdapter(cs.Byte, lambda obj, ctx: chr(obj),
                                  lambda obj, ctx: ord(obj))),

    # Lambda describing how to convert above struct to UserInformation:
    lambda obj, ctx: UserInformation(**obj),
    None
)


class ColorImage(DictInitializer):
    pass


ColorImageParser = cs.ExprAdapter(
    # Struct describing how to parse ColorImage:
    cs.Struct(
        'h' / cs.Int32ul,
        'w' / cs.Int32ul,
        'colors' / cs.Array(lambda ctx: ctx.w * ctx.h * 3, cs.Byte)),

    # Lambda describing how to convert above struct to ColorImage:
    lambda obj, ctx: ColorImage(**obj),
    None
)


class DepthImage(DictInitializer):
    pass


DepthImageParser = cs.ExprAdapter(
    # Struct describing how to parse ColorImage:
    cs.Struct(
        'h' / cs.Int32ul,
        'w' / cs.Int32ul,
        'depths' / cs.Array(lambda ctx: ctx.w * ctx.h, cs.Float32l)),

    # Lambda describing how to convert above struct to DepthImage:
    lambda obj, ctx: DepthImage(**obj),
    None
)


class Snapshot(DictInitializer):
    def __str__(self):
        return f'Snapshot from {self.timestamp} on {self.translation} / ' + \
               f'{self.rotation} with a {self.color_image.w}x' + \
               f'{self.color_image.h} color image and a ' + \
               f'{self.depth_image.w}x{self.depth_image.h} depth ' + \
               f'image.'


SnapshotStructParser = cs.ExprAdapter(
    # Struct describing how to parse Snapshot:
    cs.Struct(
        'timestamp' / DatetimeMillisecondsAdapter(cs.Int64ul),
        'translation' / cs.Struct(
                'x' / cs.Float64l,
                'y' / cs.Float64l,
                'z' / cs.Float64l),
        'rotation' / cs.Struct(
                'x' / cs.Float64l,
                'y' / cs.Float64l,
                'z' / cs.Float64l,
                'w' / cs.Float64l),
        'color_image' / ColorImageParser,
        'depth_image' / DepthImageParser,
        'feelings' / cs.Struct(
                'hunger' / cs.Float32l,
                'thirst' / cs.Float32l,
                'exhaustion' / cs.Float32l,
                'happiness' / cs.Float32l)),

    # Lambda describing how to convert above struct to Snapshot:
    lambda obj, ctx: Snapshot(**obj),
    None
)


class Reader:
    def __init__(self, path):
        self._sample_stream = open(path, 'rb')
        self.user_info = UserInformationParser.parse_stream(
                            self._sample_stream)
        self._file_size = os.fstat(self._sample_stream.fileno()).st_size

    def __getattr__(self, k):
        return getattr(self._user_info, k)

    def _is_eof(self):
        return self._sample_stream.tell() == self._file_size

    def __iter__(self):
        while not self._is_eof():
            yield SnapshotStructParser.parse_stream(self._sample_stream)
