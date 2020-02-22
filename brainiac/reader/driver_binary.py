import construct as cs

from .data_types import *
from ..utils.serializable import DateAdapter, \
    DatetimeMillisecondsAdapter

UserInformationStruct = cs.Struct(
    'user_id' / cs.Int64ul,
    'username' / cs.PascalString(cs.Int32ul, "ascii"),
    'birthday' / DateAdapter(cs.Int32ul),
    'gender' / cs.Bytes(1)
)

ColorImageStruct = cs.Struct(
    'h' / cs.Int32ul,
    'w' / cs.Int32ul,
    'colors' / cs.Bytes(lambda ctx: ctx.w * ctx.h * 3)
)

DepthImageStruct = cs.Struct(
    'h' / cs.Int32ul,
    'w' / cs.Int32ul,
    'depths' / cs.Array(lambda ctx: ctx.w * ctx.h, cs.Float32l)
)

TranslationStruct = cs.Struct(
    'x' / cs.Float64l,
    'y' / cs.Float64l,
    'z' / cs.Float64l
)

RotationStruct = cs.Struct(
    'x' / cs.Float64l,
    'y' / cs.Float64l,
    'z' / cs.Float64l,
    'w' / cs.Float64l
)

FeelingsStruct = cs.Struct(
    'hunger' / cs.Float32l,
    'thirst' / cs.Float32l,
    'exhaustion' / cs.Float32l,
    'happiness' / cs.Float32l
)

SnapshotStruct = cs.Struct(
    'timestamp' / DatetimeMillisecondsAdapter(cs.Int64ul),
    'translation' / TranslationStruct,
    'rotation' / RotationStruct,
    'color_image' / ColorImageStruct,
    'depth_image' / DepthImageStruct,
    'feelings' / FeelingsStruct
)


class BinaryDriver:
    SCHEME = 'binary'

    def __init__(self, url, open_function):
        path = url.host
        self._sample_stream = open_function(path, 'rb')
        user_info_struct = UserInformationStruct.parse_stream(self._sample_stream)
        self.user_info = UserInformation(
            user_info_struct.user_id,
            user_info_struct.username,
            user_info_struct.birthday,
            user_info_struct.gender
        )

    @property
    def user(self):
        return self.user_info

    def _is_eof(self):
        is_eof = not self._sample_stream.read(1)
        self._sample_stream.seek(-1, 1)
        return is_eof

    @classmethod
    def _bgr_to_rgb(cls, colors):
        rgb_colors = []
        for i in range(0, len(colors), 3):
            b, g, r = colors[i:i + 3]
            rgb_colors.extend([r, g, b])
        return b''.join(c.to_bytes(1, 'little') for c in rgb_colors)

    @classmethod
    def _struct_to_snapshot(cls, struct_obj):
        timestamp = struct_obj.timestamp
        translation = Translation(
            struct_obj.translation.x,
            struct_obj.translation.y,
            struct_obj.translation.z
        )
        rotation = Rotation(
            struct_obj.rotation.x,
            struct_obj.rotation.y,
            struct_obj.rotation.z,
            struct_obj.rotation.w
        )
        color_image = ColorImage(
            struct_obj.color_image.h,
            struct_obj.color_image.w,
            cls._bgr_to_rgb(struct_obj.color_image.colors)
        )
        depth_image = DepthImage(
            struct_obj.depth_image.h,
            struct_obj.depth_image.w,
            struct_obj.depth_image.depths
        )
        feelings = Feelings(
            struct_obj.feelings.hunger,
            struct_obj.feelings.thirst,
            struct_obj.feelings.exhaustion,
            struct_obj.feelings.happiness
        )
        return Snapshot(
            timestamp,
            translation,
            rotation,
            color_image,
            depth_image,
            feelings
        )

    def __iter__(self):
        while not self._is_eof():
            yield self._struct_to_snapshot(
                SnapshotStruct.parse_stream(self._sample_stream)
            )
