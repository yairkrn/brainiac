import construct as cs

from ..utils.serializable import DateAdapter, DatetimeMillisecondsAdapter


ProtocolHello = cs.Struct(
    'user_id' / cs.Int64ul,
    'username' / cs.PascalString(cs.Int32ul, "ascii"),
    'birthday' / DateAdapter(cs.Int32ul),
    'gender' / cs.Bytes(1)
)

ProtocolColorImage = cs.Struct(
    'h' / cs.Int32ul,
    'w' / cs.Int32ul,
    'colors' / cs.Bytes(lambda ctx: ctx.w * ctx.h * 3)
)

ProtocolDepthImage = cs.Struct(
    'h' / cs.Int32ul,
    'w' / cs.Int32ul,
    'depths' / cs.Array(lambda ctx: ctx.w * ctx.h, cs.Float32l)
)

ProtocolTranslation = cs.Struct(
    'x' / cs.Float64l,
    'y' / cs.Float64l,
    'z' / cs.Float64l
)

ProtocolRotation = cs.Struct(
    'x' / cs.Float64l,
    'y' / cs.Float64l,
    'z' / cs.Float64l,
    'w' / cs.Float64l
)

ProtocolFeelings = cs.Struct(
    'hunger' / cs.Float32l,
    'thirst' / cs.Float32l,
    'exhaustion' / cs.Float32l,
    'happiness' / cs.Float32l
)

ProtocolSnapshot = cs.Struct(
    'timestamp' / DatetimeMillisecondsAdapter(cs.Int64ul),
    'translation' / ProtocolTranslation,
    'rotation' / ProtocolRotation,
    'color_image' / ProtocolColorImage,
    'depth_image' / ProtocolDepthImage,
    'feelings' / ProtocolFeelings
)

ProtocolConfig = cs.Struct(
    'supported_fields_number' / cs.Int32ul,
    'supported_fields' / cs.Array(lambda ctx: ctx.supported_fields_number,
                                  cs.PascalString(cs.Int32ul, "ascii"))
)
