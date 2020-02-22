import json

import attr


@attr.s
class MessageQueueProduct:
    # TODO: force types?
    user_id = attr.ib()
    timestamp = attr.ib()
    path = attr.ib()

    def serialize(self):
        return json.dumps(attr.asdict(self))

    def __str__(self):
        return self.serialize()
