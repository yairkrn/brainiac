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
    _GENDER_BYTE_TO_STR = {
        b'm': 'male',
        b'f': 'female',
        b'o': 'other'
    }

    def __init__(self, url, open_function):
        path = url.host
        self._sample_stream = open_function(path, 'rb')
        user_info_struct = UserInformationStruct.parse_stream(self._sample_stream)
        self.user_info = ReaderUserInformation(
            user_info_struct.user_id,
            user_info_struct.username,
            user_info_struct.birthday,
            self._GENDER_BYTE_TO_STR[user_info_struct.gender]
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
    def _reader_snapshot_from_binary(cls, snapshot):
        timestamp = snapshot.timestamp
        translation = ReaderTranslation(
            snapshot.translation.x,
            snapshot.translation.y,
            snapshot.translation.z
        )
        rotation = ReaderRotation(
            snapshot.rotation.x,
            snapshot.rotation.y,
            snapshot.rotation.z,
            snapshot.rotation.w
        )
        color_image = ReaderColorImage(
            snapshot.color_image.h,
            snapshot.color_image.w,
            cls._bgr_to_rgb(snapshot.color_image.colors)
        )
        depth_image = ReaderDepthimage(
            snapshot.depth_image.h,
            snapshot.depth_image.w,
            snapshot.depth_image.depths
        )
        feelings = ReaderFeelings(
            snapshot.feelings.hunger,
            snapshot.feelings.thirst,
            snapshot.feelings.exhaustion,
            snapshot.feelings.happiness
        )
        return ReaderSnapshot(
            timestamp,
            translation,
            rotation,
            color_image,
            depth_image,
            feelings
        )

    def __iter__(self):
        while not self._is_eof():
            yield self._reader_snapshot_from_binary(
                SnapshotStruct.parse_stream(self._sample_stream)
            )
