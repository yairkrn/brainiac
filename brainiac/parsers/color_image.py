from PIL import Image


class ColorImageParser:
    field = 'color_image'

    def parse(self, context, snapshot):
        width = snapshot.color_image.w
        height = snapshot.color_image.h
        image = Image.new('RGB', (width, height))
        image.putdata(snapshot.color_image.rgb_colors)
        image.save(context.directory / 'color_image.png')
