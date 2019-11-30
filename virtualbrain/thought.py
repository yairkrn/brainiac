import datetime as dt
import struct


class ThoughtHeader:
    TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
    HEADER_FORMAT = '<QQI'
    HEADER_SIZE = struct.calcsize(HEADER_FORMAT)

    def __init__(self, user_id, timestamp, thought_size):
        self._user_id = user_id
        self._timestamp = timestamp
        self._thought_size = thought_size

    @property
    def user_id(self):
        return self._user_id

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def thought_size(self):
        return self._thought_size

    def serialize(self):
        return struct.pack(self.HEADER_FORMAT,
                           self._user_id,
                           int(self._timestamp.timestamp()),
                           self._thought_size)

    @classmethod
    def deserialize(cls, header_bytes):
        user_id, timestamp, thought_size = struct.unpack(cls.HEADER_FORMAT,
                                                         header_bytes)
        return cls(user_id, dt.datetime.fromtimestamp(timestamp), thought_size)


class Thought:
    def __init__(self, user_id, timestamp, thought):
        self._header = ThoughtHeader(user_id, timestamp, len(thought))
        self._thought = thought

    @property
    def user_id(self):
        return self._header.user_id

    @property
    def timestamp(self):
        return self._header.timestamp

    @property
    def thought(self):
        return self._thought

    def __repr__(self):
        return f'{self.__class__.__name__}('        \
             + f'user_id={self.user_id}, '          \
             + f'timestamp={self.timestamp!r}, '    \
             + f'thought="{self._thought}")'

    def __str__(self):
        formatted_time = self.timestamp.strftime(ThoughtHeader.TIME_FORMAT)
        return f'[{formatted_time}] user {self.user_id}: {self._thought}'

    def __eq__(self, other):
        return isinstance(other, self.__class__) \
            and (self.user_id, self.timestamp, self._thought) == \
                (other.user_id, other.timestamp, other._thought)

    def serialize(self):
        return self._header.serialize() + self._thought.encode()

    @classmethod
    def deserialize(cls, thought_bytes):
        header_bytes = thought_bytes[:ThoughtHeader.HEADER_SIZE]
        header = ThoughtHeader.deserialize(header_bytes)
        thought = thought_bytes[header.HEADER_SIZE:]

        if len(thought) < header.thought_size:
            err = 'Incomplete thought:' \
                + f'{len(thought)}/{header.thought_size} bytes received.'
            raise ValueError(err)

        return cls(header.user_id, header.timestamp, thought.decode())
