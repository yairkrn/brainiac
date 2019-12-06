import datetime as dt
import os

import construct as cs


"""
Construct Definitions:
"""


class DatetimeAdapter(cs.Adapter):
    def _decode(self, obj, context, path):
        return dt.datetime.fromtimestamp(obj)

    def _encode(self, obj, context, path):
        return obj.timestamp()


class DatetimeMillisecondsAdapter(cs.Adapter):
    _MILLISECONDS_IN_SECOND = 100

    def _decode(self, obj, context, path):
        print(dt.datetime.fromtimestamp(obj / self._MILLISECONDS_IN_SECOND))
        return dt.datetime.fromtimestamp(obj / self._MILLISECONDS_IN_SECOND)

    def _encode(self, obj, context, path):
        return obj.timestamp() * self._MILLISECONDS_IN_SECOND


class CharAdapter(cs.Adapter):
    def _decode(self, obj, context, path):
        return chr(obj)

    def _encode(self, obj, context, path):
        return ord(obj)


UserInformation = cs.Struct(
        'user_id' / cs.Int64ul,
        'username' / cs.PascalString(cs.Int32ul, "ascii"),
        'birthday' / DatetimeAdapter(cs.Int32ul),
        'gender' / CharAdapter(cs.Byte)
    )


Snapshot = cs.Struct(
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
        'color_image' / cs.Struct(
                'h' / cs.Int32ul,
                'w' / cs.Int32ul,
                'colors' / cs.Array(lambda ctx: ctx.w * ctx.h * 3, cs.Byte)),
        'depth_image' / cs.Struct(
                'h' / cs.Int32ul,
                'w' / cs.Int32ul,
                'depths' / cs.Array(lambda ctx: ctx.w * ctx.h,
                                    cs.Float32l)),
        'feelings' / cs.Struct(
                'hunger' / cs.Float32l,
                'thirst' / cs.Float32l,
                'exhaustion' / cs.Float32l,
                'happiness' / cs.Float32l)
)


"""
Classes:
"""


class Reader:
    def __init__(self, path):
        self._sample_stream = open(path, 'rb')
        self._user_info = UserInformation.parse_stream(
            self._sample_stream)
        self._file_size = os.fstat(self._sample_stream.fileno()).st_size

    def __getattr__(self, k):
        return self._user_info[k]

    def _is_eof(self):
        return self._sample_stream.tell() == self._file_size

    def __iter__(self):
        while not self._is_eof():
            yield Snapshot.parse_stream(self._sample_stream)
