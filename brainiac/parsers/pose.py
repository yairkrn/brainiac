import json


def parse_translation(context, snapshot):
    with open(context.directory / 'translation.json', 'w') as writer:
        translation_dict = dict(
            x=snapshot.translation.x,
            y=snapshot.translation.y,
            z=snapshot.translation.z)
        json.dump(translation_dict, writer)


parse_translation.field = 'translation'


def parse_rotation(context, snapshot):
    with open(context.directory / 'rotation.json', 'w') as writer:
        rotation_dict = dict(
            x=snapshot.rotation.x,
            y=snapshot.rotation.y,
            z=snapshot.rotation.z,
            w=snapshot.rotation.w)
        json.dump(rotation_dict, writer)


parse_rotation.field = 'rotation'


def parse_pose(context, snapshot):
    parse_translation(context, snapshot)
    parse_rotation(context, snapshot)


parse_pose.field = 'pose'
