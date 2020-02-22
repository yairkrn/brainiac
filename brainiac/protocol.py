import construct as cs

from .utils.serializable import ByteAdapter, DateAdapter, \
    DatetimeMillisecondsAdapter

HelloMessage = cs.Struct(
    'user_id' / cs.Int64ul,
    'username' / cs.PascalString(cs.Int32ul, "ascii"),
    'birthday' / DateAdapter(cs.Int32ul),
    'gender' / cs.Bytes(1)
)

ColorImage = cs.Struct(
    'h' / cs.Int32ul,
    'w' / cs.Int32ul,
    'colors' / cs.Bytes(lambda ctx: ctx.w * ctx.h * 3)
)

DepthImage = cs.Struct(
    'h' / cs.Int32ul,
    'w' / cs.Int32ul,
    'depths' / cs.Array(lambda ctx: ctx.w * ctx.h, cs.Float32l)
)

Translation = cs.Struct(
    'x' / cs.Float64l,
    'y' / cs.Float64l,
    'z' / cs.Float64l
)

Rotation = cs.Struct(
    'x' / cs.Float64l,
    'y' / cs.Float64l,
    'z' / cs.Float64l,
    'w' / cs.Float64l
)

Feelings = cs.Struct(
    'hunger' / cs.Float32l,
    'thirst' / cs.Float32l,
    'exhaustion' / cs.Float32l,
    'happiness' / cs.Float32l
)

SnapshotMessage = cs.Struct(
    'timestamp' / DatetimeMillisecondsAdapter(cs.Int64ul),
    'translation' / Translation,
    'rotation' / Rotation,
    'color_image' / ColorImage,
    'depth_image' / DepthImage,
    'feelings' / Feelings
)

ConfigMessage = cs.Struct(
    'supported_fields_number' / cs.Int32ul,
    'supported_fields' / cs.Array(lambda ctx: ctx.supported_fields_number,
                                  cs.PascalString(cs.Int32ul, "ascii"))
)


def snapshot_to_snapshot_message(snapshot, fields):
    field_values = {'timestamp': snapshot.timestamp}
    if 'translation' in fields:
        field_values['translation'] = \
            dict(x=snapshot.translation.x,
                 y=snapshot.translation.y,
                 z=snapshot.translation.z)
    if 'rotation' in fields:
        field_values['rotation'] = \
            dict(x=snapshot.rotation.x,
                 y=snapshot.rotation.y,
                 z=snapshot.rotation.z,
                 w=snapshot.rotation.w)
    if 'color_image' in fields:
        field_values['color_image'] = \
            dict(h=snapshot.color_image.h,
                 w=snapshot.color_image.w,
                 colors=snapshot.color_image.colors)
    if 'depth_image' in fields:
        field_values['depth_image'] = \
            dict(h=snapshot.depth_image.h,
                 w=snapshot.depth_image.w,
                 depths=snapshot.depth_image.depths)
    if 'feelings' in fields:
        field_values['feelings'] = \
            dict(hunger=snapshot.feelings.hunger,
                 thirst=snapshot.feelings.thirst,
                 exhaustion=snapshot.feelings.exhaustion,
                 happiness=snapshot.feelings.happiness)
    return SnapshotMessage.build(field_values)
