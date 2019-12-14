import gzip
import os
import struct

from .proto import sample_pb2 as proto


class ProtoDriver:
    SCHEME = 'proto://'
    _SIZE_STRUCT = '<I'

    def __init__(self, url):
        path = url[len(self.SCHEME):]
        self._sample_stream = gzip.open(path, 'rb')
        self.user = self._read_obj(proto.User)
        self._file_size = os.fstat(self._sample_stream.fileno()).st_size

    def _read_size(self):
        size_bytes = \
            self._sample_stream.read(struct.calcsize(self._SIZE_STRUCT))
        return struct.unpack(self._SIZE_STRUCT, size_bytes)[0]

    def _read_obj(self, obj_cls):
        obj_size = self._read_size()
        obj = obj_cls()
        obj_str = self._sample_stream.read(obj_size)
        obj.ParseFromString(obj_str)
        return obj

    def _is_eof(self):
        return self._sample_stream.tell() == self._file_size

    def __iter__(self):
        while not self._is_eof():
            yield self._read_obj(proto.Snapshot)
