import json
import datetime as dt

import attr


@attr.s
class ServerParsersMessage:
    TAG = 'parsers'
    # TODO: force types?
    TIME_FORMAT = '%Y-%m-%d_%H-%M-%S-%f'
    user_id = attr.ib()
    timestamp = attr.ib()
    snapshot_path = attr.ib()

    def serialize(self):
        formatted_timestamp = self.timestamp.strftime(self.TIME_FORMAT)
        d = attr.asdict(self)
        d['timestamp'] = formatted_timestamp
        return json.dumps(d)

    @classmethod
    def deserialize(cls, raw_message):
        d = json.loads(raw_message)
        d['timestamp'] = dt.datetime.strptime(d['timestamp'], cls.TIME_FORMAT)
        return cls(**d)

    def __str__(self):
        return self.serialize()
