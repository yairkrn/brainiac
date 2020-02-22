import construct as cs

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


# FIXME: rename
def snapshot_message_to_products(sample, fields):
    res = {}
    if 'translation' in fields:
        res['translation'] = \
            Translation.build(dict(x=sample.translation.x,
                                   y=sample.translation.y,
                                   z=sample.translation.z))
    if 'rotation' in fields:
        res['rotation'] = \
            Rotation.build(dict(x=sample.rotation.x,
                                y=sample.rotation.y,
                                z=sample.rotation.z,
                                w=sample.rotation.w))
    if 'color_image' in fields:
        res['color_image'] = \
            ColorImage.build(dict(h=sample.color_image.h,
                                  w=sample.color_image.w,
                                  colors=sample.color_image.colors))
    if 'depth_image' in fields:
        res['depth_image'] = \
            DepthImage.build(dict(h=sample.depth_image.h,
                                  w=sample.depth_image.w,
                                  depths=sample.depth_image.depths))
    if 'feelings' in fields:
        res['feelings'] = \
            Feelings.build(dict(hunger=sample.feelings.hunger,
                                thirst=sample.feelings.thirst,
                                exhaustion=sample.feelings.exhaustion,
                                happiness=sample.feelings.happiness))
    return res
