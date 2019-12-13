import json

from PIL import Image


class Parser:
    def __init__(self):
        self.field_functions = {}

    @property
    def supported_fields(self):
        return self.field_functions.keys()

    def __call__(self, field):
        def decorator(func):
            # Register this function as a parser for these fields.
            self.field_functions[field] = func

            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            return wrapper
        return decorator

    def parse(self, context, snapshot):
        for field, func in self.field_functions.items():
            func(context, snapshot)


parser = Parser()


@parser('translation')
def parse_translation(context, snapshot):
    with open(context.directory / 'translation.json', 'w') as writer:
        translation_dict = dict(
            x=snapshot.translation.x,
            y=snapshot.translation.y,
            z=snapshot.translation.z)
        json.dump(translation_dict, writer)


@parser('color_image')
def parse_translation(context, snapshot):
    width = snapshot.color_image.w
    height = snapshot.color_image.h
    image = Image.new('RGB', (width, height))
    image.putdata(snapshot.color_image.rgb_colors)
    image.save(context.directory / 'color_image.png')
