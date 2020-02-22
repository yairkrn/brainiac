import json

import attr


@attr.s
class MQSnapshotMessage:
    # TODO: force types?
    user_id = attr.ib()
    snapshot_path = attr.ib()
    fields = attr.ib()  # TODO: remove

    def serialize(self):
        return json.dumps(attr.asdict(self))

    def __str__(self):
        return self.serialize()

