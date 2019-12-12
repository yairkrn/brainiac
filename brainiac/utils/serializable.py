import datetime as dt

import construct as cs


class ByteAdapter(cs.Adapter):
    def _decode(self, obj, context, path):
        return chr(obj)

    def _encode(self, obj, context, path):
        return ord(obj)


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
        return int(obj.timestamp() * self._MILLISECONDS_IN_SECOND)


def serializable(cs_struct):
    def wrapper(cls):
        class Adapter(cs.Adapter):
            def _decode(self, obj, context, path):
                values = {}
                for subcon in cs_struct.subcons:
                    key = subcon.name
                    if not key.startswith('_'):
                        values[key] = obj[key]
                return cls(**values)

            def _encode(self, obj, context, path):
                return obj.__dict__

            def __call__(self, *args, **kwargs):
                print(args, kwargs)
                return cls(*args, **kwargs)
        setattr(cls, 'struct', Adapter(cs_struct))

        def serialize(self):
            return self.struct.build(self)
        setattr(cls, 'serialize', serialize)

        @classmethod
        def deserialize(cls, _bytes):
            return cls.struct.parse(_bytes)
        setattr(cls, 'deserialize', deserialize)

        @classmethod
        def deserialize_stream(cls, stream):
            return cls.struct.parse_stream(stream)
        setattr(cls, 'deserialize_stream', deserialize_stream)

        return cls
    return wrapper
