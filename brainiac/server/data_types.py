import construct as cs

from ..utils.serializable import DatetimeMillisecondsAdapter

ServerColorImage = cs.Struct(
    'h' / cs.Int32ul,
    'w' / cs.Int32ul,
    'colors' / cs.Bytes(lambda ctx: ctx.w * ctx.h * 3)
)

ServerDepthImage = cs.Struct(
    'h' / cs.Int32ul,
    'w' / cs.Int32ul,
    'depths' / cs.Array(lambda ctx: ctx.w * ctx.h, cs.Float32l)
)

ServerTranslation = cs.Struct(
    'x' / cs.Float64l,
    'y' / cs.Float64l,
    'z' / cs.Float64l
)

ServerRotation = cs.Struct(
    'x' / cs.Float64l,
    'y' / cs.Float64l,
    'z' / cs.Float64l,
    'w' / cs.Float64l
)

ServerFeelings = cs.Struct(
    'hunger' / cs.Float32l,
    'thirst' / cs.Float32l,
    'exhaustion' / cs.Float32l,
    'happiness' / cs.Float32l
)

ServerSnapshot = cs.Struct(
    'timestamp' / DatetimeMillisecondsAdapter(cs.Int64ul),
    'translation' / ServerTranslation,
    'rotation' / ServerRotation,
    'color_image' / ServerColorImage,
    'depth_image' / ServerDepthImage,
    'feelings' / ServerFeelings
)
