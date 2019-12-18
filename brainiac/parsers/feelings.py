import json


def parse_feelings(context, snapshot):
    with open(context.directory / 'feelings.json', 'w') as writer:
        feelings_dict = dict(
            hunger=snapshot.feelings.hunger,
            thirst=snapshot.feelings.thirst,
            exhaustion=snapshot.feelings.exhaustion,
            happiness=snapshot.feelings.happiness)
        json.dump(feelings_dict, writer)


parse_feelings.field = 'feelings'
