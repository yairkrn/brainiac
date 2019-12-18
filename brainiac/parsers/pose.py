import json


def parse_translation(context, snapshot):
    with open(context.directory / 'translation.json', 'w') as writer:
        translation_dict = dict(
            x=snapshot.translation.x,
            y=snapshot.translation.y,
            z=snapshot.translation.z)
        json.dump(translation_dict, writer)


parse_translation.field = 'translation'
