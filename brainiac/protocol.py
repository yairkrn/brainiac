import datetime as dt

import construct as cs


class DateAdapter(cs.Adapter):
    def _decode(self, obj, context, path):
        return dt.datetime.fromtimestamp(obj)

    def _encode(self, obj, context, path):
        return int(obj.timestamp())


class DatetimeMillisecondsAdapter(cs.Adapter):
    _MILLISECONDS_IN_SECOND = 1000

    def _decode(self, obj, context, path):
        return dt.datetime.fromtimestamp(obj / self._MILLISECONDS_IN_SECOND)

    def _encode(self, obj, context, path):
        return obj.timestamp() * self._MILLISECONDS_IN_SECOND


GenderParser = cs.ExprAdapter(
        cs.Byte,
        lambda obj, ctx: chr(obj),
        lambda obj, ctx: ord(obj)
    )


HelloMessage = cs.Struct(
    'user_id' / cs.Int64ul,
    'username' / cs.PascalString(cs.Int32ul, "ascii"),
    'birthday' / DateAdapter(cs.Int32ul),
    'gender' / GenderParser)


ConfigMessage = cs.Struct(
    'supported_fields_number' / cs.Int32ul,
    'supported_fields' / cs.Array(lambda ctx: ctx.supported_fields_number,
                                  cs.PascalString(cs.Int32ul, "ascii"))
    )


SnapshotMessage = cs.Struct(
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
        'depths' / cs.Array(lambda ctx: ctx.w * ctx.h, cs.Float32l)),
    'feelings' / cs.Struct(
        'hunger' / cs.Float32l,
        'thirst' / cs.Float32l,
        'exhaustion' / cs.Float32l,
        'happiness' / cs.Float32l)
    )

